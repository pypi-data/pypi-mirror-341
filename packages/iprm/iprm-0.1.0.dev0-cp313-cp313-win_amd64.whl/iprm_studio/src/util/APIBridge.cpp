/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "APIBridge.hpp"
#include "AssetCache.hpp"

#include <pybind11/embed.h>
#include <QList>
#include <QString>

#include <ranges>

namespace iprm {

APIError make_error(const QString& err_msg,
                    const pybind11::error_already_set& e) {
  const char* py_err_details = e.what();
  const QString err_details =
      QByteArray::fromRawData(py_err_details, std::strlen(py_err_details));
  return APIError(QString("%0: %1").arg(err_msg, err_details));
}

APIBridge::APIBridge(QObject* parent) : QObject(parent) {
  qRegisterMetaType<APIError>();
  qRegisterMetaType<PlatformFile>();
}

APIBridge::~APIBridge() {
  if (iprm_.has_value()) {
    iprm_.value().release();
  }
}

void APIBridge::set_root_dir(const QDir& root_dir) {
  root_dir_ = root_dir;
}

QStringList APIBridge::platforms() const {
  QStringList platforms;
  platforms.reserve(platforms_.size());
  for (const auto& platform : platforms_) {
    platforms.push_back(platform.first);
  }
  return platforms;
}

const QIcon& APIBridge::icon(const QString& platform) const {
  static const QIcon s_no_platform;
  const auto platform_icon_itr =
      AssetCache::platform_icon_lookup_.find(platform);
  if (platform_icon_itr == AssetCache::platform_icon_lookup_.end()) {
    return s_no_platform;
  }
  const auto& platform_icon = platform_icon_itr->second;
  assert(platform_icon.has_value());
  return platform_icon.value().get();
}

const QString& APIBridge::display(const QString& platform) const {
  static const QString s_no_platform;
  const auto platform_display_itr = platform_names_.find(platform);
  if (platform_display_itr == platform_names_.end()) {
    return s_no_platform;
  }

  return platform_display_itr.value();
}

const QHash<QString, QList<ObjectNode>>& APIBridge::objects(
    const QString& platform) const {
  static const QHash<QString, QList<ObjectNode>> s_no_platform;

  const auto platform_itr = platforms_.find(platform);
  if (platform_itr == platforms_.end()) {
    return s_no_platform;
  }
  return platform_itr->second.objs_;
}

std::tuple<
    std::reference_wrapper<const lemon::ListDigraph>,
    std::reference_wrapper<const lemon::ListDigraph::NodeMap<ObjectNode>>>
APIBridge::dependency_graph(const QString& platform) const {
  static const lemon::ListDigraph s_no_dep_graph;
  static const lemon::ListDigraph::NodeMap<ObjectNode> s_no_dep_data(
      s_no_dep_graph);

  const auto platform_itr = platforms_.find(platform);
  if (platform_itr == platforms_.end()) {
    return std::make_tuple(std::cref(s_no_dep_graph), std::cref(s_no_dep_data));
  }
  auto& dep_graph = platform_itr->second.dep_graph_;
  assert(dep_graph.has_value());
  return std::make_tuple(std::cref(dep_graph.value().graph_),
                         std::cref(dep_graph.value().node_data_));
}

void APIBridge::capture_io() {
  auto sys = py::module::import("sys");
  if (!sys) {
    Q_EMIT error(APIError("Failed to import sys module"));
    return;
  }

  py::module io = py::module::import("io");
  if (!io) {
    Q_EMIT error(APIError("Failed to import io module"));
    return;
  }

  py::module builtins = py::module::import("builtins");
  if (!builtins) {
    Q_EMIT error(APIError("Failed to import builtins module"));
    return;
  }

  py::cpp_function print([this, sys](py::args args, py::kwargs kwargs) {
    // TODO: Handle stderr so we log it as an error
    if (args.size() == 1) {
      Q_EMIT print_stdout(QString::fromStdString(args[0].cast<std::string>()));
    }
  });
  builtins.attr("print") = print;
}

bool APIBridge::append_iprm_path() {
  if (iprm_.has_value()) {
    return true;
  }

  auto sys = py::module::import("sys");
  if (!sys) {
    Q_EMIT error(APIError("Failed to import sys module"));
    return false;
  }

  std::filesystem::path iprm_root(__FILE__);
  for (int i = 0; i < 4 && !iprm_root.parent_path().empty(); i++) {
    iprm_root = iprm_root.parent_path();
  }
  auto path_list = sys.attr("path").cast<py::list>();
  path_list.append(iprm_root.string());

  auto iprm = py::module::import("iprm");
  if (!iprm) {
    Q_EMIT error(APIError("Failed to append iprm to python interpreter path"));
  }
  iprm_ = iprm;
  return true;
}

std::vector<std::string> get_file_extensions(const py::list& py_file_exts) {
  std::vector<std::string> file_exts;
  file_exts.reserve(py_file_exts.size());
  for (const auto& file_ext : py_file_exts) {
    file_exts.push_back(file_ext.cast<std::string>());
  }
  return file_exts;
}

void APIBridge::load_builtin_backends() {
  if (!append_iprm_path()) {
    return;
  }

  // TODO: Query the commands the builtin backend supports and don't hardcode
  //  these arguments, get them from settings if the project and the backend
  //  has them saved, otherwise use these as defaults

  // TODO: Simply this by putting each builtin backend information into a
  //  structure we can loop over to add to our backends list
  const QString src_dir = root_dir_.absolutePath();
  {
    auto cmake_backend = py::module::import("iprm.backend.cmake").attr("CMake");
    const auto cmake_name = QString::fromStdString(
        cmake_backend.attr("name")().cast<std::string>());

    const auto cmake_file_exts =
        get_file_extensions(cmake_backend.attr("generate_file_exts")());

    const QString cmake_bin_dir = root_dir_.absoluteFilePath("build/cmake");

    SystemBackend backend{
        .klass_ = cmake_backend,
        .file_exts_ = cmake_file_exts,
        .name_ = cmake_name,
        .icon_ = AssetCache::cmake_icon(),
        .type_ = BackendType::Builtin,
        .commands_ = {
            BackendGenerate{},
         BackendConfigure{QStringList{} << "--ninja"
                                        << "--srcdir" << src_dir << "--bindir"
                                        << cmake_bin_dir << "--release"},
         BackendBuild{QStringList{} << "--bindir" << cmake_bin_dir
                                    << "--release"},
         BackendTest{QStringList{} << "--bindir" << cmake_bin_dir
                                   << "--release"}}};
    builtin_backends_.append(backend);
  }

  {
    auto meson_backend = py::module::import("iprm.backend.meson").attr("Meson");
    const auto meson_name = QString::fromStdString(
        meson_backend.attr("name")().cast<std::string>());

    const auto meson_file_exts =
        get_file_extensions(meson_backend.attr("generate_file_exts")());

    const QString meson_bin_dir = root_dir_.absoluteFilePath("build/meson");

    SystemBackend backend{
      .klass_ = meson_backend,
      .file_exts_ = meson_file_exts,
      .name_ = meson_name,
      .icon_ = QIcon(":/logos/meson.png"),
      .type_ = BackendType::Builtin,
      .commands_ = {
        BackendGenerate{},
     BackendConfigure{QStringList{} << "--ninja"
                                    << "--srcdir" << src_dir << "--bindir"
                                    << meson_bin_dir << "--release"},
     BackendBuild{QStringList{} << "--bindir" << meson_bin_dir
                                << "--release"},
     BackendTest{QStringList{} << "--bindir" << meson_bin_dir
                               << "--release"}}};
    builtin_backends_.append(backend);
  }

  {
    auto scons_backend = py::module::import("iprm.backend.scons").attr("SCons");
    const auto scons_name = QString::fromStdString(
        scons_backend.attr("name")().cast<std::string>());

    const auto scons_file_exts =
        get_file_extensions(scons_backend.attr("generate_file_exts")());

    const QString scons_bin_dir = root_dir_.absoluteFilePath("build/scons");

    SystemBackend backend{
        .klass_ = scons_backend,
        .file_exts_ = scons_file_exts,
        .name_ = scons_name,
        .icon_ = QIcon(":/logos/scons.png"),
        .type_ = BackendType::Builtin,
        .commands_ = {BackendGenerate{},
                      BackendBuild{QStringList{} << "--bindir" << scons_bin_dir
                                                 << "--release"}}};
    builtin_backends_.append(backend);
  }

#ifdef Q_OS_WIN
  {
    auto msbuild_backend = py::module::import("iprm.backend.msbuild").attr("MSBuild");
    const auto msbuild_name = QString::fromStdString(
        msbuild_backend.attr("name")().cast<std::string>());

    const auto msbuild_file_exts =
        get_file_extensions(msbuild_backend.attr("generate_file_exts")());

    // TODO: Remove hardcoded solution here by providing the actual dialog and
    //  allow users to setup the command arguments
    SystemBackend backend{
      .klass_ = msbuild_backend,
        .file_exts_ = msbuild_file_exts,
        .name_ = msbuild_name,
        .icon_ = AssetCache::msbuild_icon(),
        .type_ = BackendType::Builtin,
        .commands_ = {
            BackendGenerate{},
            BackendBuild{QStringList{} << "--bindir" << "build/msbuild"
                                       << "--release" << "--solution"
                                       << "iprm_cli_test"}}};
    builtin_backends_.append(backend);
  }
#endif
}

void APIBridge::load_plugin_backends(const QDir& plugin_dir) {
  if (!append_iprm_path()) {
    return;
  }
  plugins_dir_ = plugin_dir;
  auto iprm_util_plugins = py::module::import("iprm.util.plugins");
  const std::string dir = plugin_dir.absolutePath().toStdString();
  py::dict loaded_plugins = iprm_util_plugins.attr("load_backends")(dir);
  for (const auto& [plugin_name, plugin_klass] : loaded_plugins) {
    const auto name = QString::fromStdString(plugin_name.cast<std::string>());
    py::object klass = plugin_klass.cast<py::object>();
    py::object icon_path = klass.attr("icon")();
    const auto icon_path_str =
        QString::fromStdString(icon_path.attr("__str__")().cast<std::string>());
    // TODO: Query the commands the plugin backend supports and add the
    //  supported commands
    plugin_backends_.append(SystemBackend{
        .klass_ = klass,
        .file_exts_ = get_file_extensions(klass.attr("generate_file_exts")()),
        .name_ = name,
        .icon_ = QIcon(icon_path_str),
        .type_ = BackendType::Plugin,
        .commands_ = {BackendGenerate{}}});
  }
}

void APIBridge::init_sess() {
  destroy_sess();
  if (!append_iprm_path()) {
    return;
  }

  auto& iprm = iprm_.value();

  try {

    version_ =
        QString::fromStdString(iprm.attr("__version__").cast<std::string>());
    copyright_ =
        QString::fromStdString(iprm.attr("__copyright__").cast<std::string>());
    native_file_name_ = iprm.attr("FILE_NAME").cast<std::string>();

    auto iprm_core_session = py::module::import("iprm.core.session");
    if (!iprm_core_session) {
      Q_EMIT error(APIError("Failed to import iprm.core.session module"));
      return;
    }

    const std::string dir = root_dir_.absolutePath().toStdString();
    // Create kwargs dict with default values matching CLI
    // py::dict kwargs;
    // kwargs["use_cache"] = true;  // Match CLI default behavior

    try {
      auto session_class = iprm_core_session.attr("Session");
      session_class.attr("create")(dir);

      py::list loadable_file_paths =
          session_class.attr("retrieve_loadable_files")();

      for (const auto& file_path : loadable_file_paths) {
        file_paths_.emplace_back(file_path.cast<std::string>());
      }

      sess_ = session_class;
    } catch (const py::error_already_set& e) {
      Q_EMIT error(make_error("Failed to create Session", e));
    }
  } catch (const py::error_already_set& e) {
    Q_EMIT error(make_error("Error during initialization", e));
  }
}

void APIBridge::destroy_sess() {
  if (!sess_.has_value()) {
    return;
  }
  for (auto& platform : platforms_ | std::views::values) {
    if (platform.native_loader_.has_value()) {
      platform.native_loader_.value().release();
    }
  }
  (void)sess_.value().attr("destroy")();
  sess_.value().release();
  sess_.reset();
}

void APIBridge::load_project() {
  init_sess();
  if (!sess_.has_value()) {
    Q_EMIT error(APIError("APIBridge not initialized"));
    return;
  }

  const auto iprm_util_platform = py::module::import("iprm.util.platform");
  if (!iprm_util_platform) {
    Q_EMIT error(APIError("Failed to import iprm.util.env module"));
    return;
  }

  const auto iprm_load_native = py::module::import("iprm.util.loader");
  if (!iprm_load_native) {
    Q_EMIT error(APIError("Failed to import iprm.util.loader module"));
    return;
  }

  const py::dict platform_display_lookup =
      iprm_util_platform.attr("PLAT_DISPLAY_NAME");
  for (const auto& [key, value] : platform_display_lookup) {
    const auto name = key.cast<std::string>();
    const auto display_name = value.cast<std::string>();
    platform_names_[QString::fromStdString(name)] =
        QString::fromStdString(display_name);
  }

  for (const py::list supported_platforms =
           iprm_util_platform.attr("PLATFORMS");
       const auto& supported_platform : supported_platforms) {
    const auto plat = supported_platform.cast<std::string>();
    const auto platform_name = QString::fromStdString(plat);
    Platform& platform = platforms_[platform_name];

    const std::string dir = root_dir_.absolutePath().toStdString();
    platform.native_loader_ =
        iprm_load_native.attr("Loader")(dir, plat.data());
    if (!platform.native_loader_) {
      Q_EMIT error(APIError("Failed to create Loader instance"));
      return;
    }

    try {
      platform.objs_.clear();
      py::handle py_objects =
          platform.native_loader_.value().attr("load_project")();
      if (!py_objects.is_none()) {
        process_objects(platform, py_objects.cast<py::dict>());
      } else {
        platforms_.erase(platform_name);
      }
    } catch (const py::error_already_set& e) {
      Q_EMIT error(make_error(QString("Error loading project for platform '%0'")
                                  .arg(platform_names_[platform_name]),
                              e));
    }
  }

  supported_platform_names_.clear();
  for (const auto& platform : platforms_ | std::views::keys) {
    supported_platform_names_.append(platform);
  }

  const auto windows_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("WINDOWS_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[windows_plat_name] =
      AssetCache::windows_icon();

  const auto macos_plat_name = QString::fromStdString(
      iprm_util_platform.attr("MACOS_PLAT_NAME").cast<std::string>());
  const auto macos_plat_display_name = display(macos_plat_name);
  AssetCache::platform_icon_lookup_[macos_plat_name] = AssetCache::macos_icon();
  AssetCache::platform_icon_lookup_[macos_plat_display_name] =
      AssetCache::macos_icon();

  const auto linux_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("LINUX_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[linux_plat_name] = AssetCache::linux_icon();

  const auto wasm_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("WASM_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[wasm_plat_name] = AssetCache::wasm_icon();

  const auto platform = py::module::import("platform");
  if (!platform) {
    Q_EMIT error(APIError("Failed to import platform module"));
    return;
  }
  const auto platform_system =
      QString::fromStdString(platform.attr("system")().cast<std::string>());
  const auto platform_display_itr = platform_names_.find(platform_system);
  const auto platform_icon_itr =
      AssetCache::platform_icon_lookup_.find(platform_system);
  if (platform_display_itr == platform_names_.end() ||
      platform_icon_itr == AssetCache::platform_icon_lookup_.end()) {
    Q_EMIT error(APIError(
        QString("Platform '%0' is not supported").arg(platform_system)));
    return;
  }
  host_platform_display_name_ = platform_display_itr.value();
  AssetCache::host_platform_icon_ = platform_icon_itr->second;

  const auto iprm_namespace = py::module::import("iprm.namespace");
  if (!iprm_namespace) {
    Q_EMIT error(APIError("Failed to import iprm.namespace module"));
    return;
  }

  auto populate_api =
      [](const py::dict& categories,
         QHash<QString, QList<QPair<QString, TypeFlags>>>& api) {
        for (const auto& [key, value] : categories) {
          const auto category = QString::fromStdString(key.cast<std::string>());
          const py::list py_types = value.cast<py::list>();
          QList<QPair<QString, TypeFlags>> types;
          for (const auto& py_type : py_types) {
            const auto py_type_dict = py_type.cast<py::dict>();
            for (const auto& [py_type_name, py_type_flags] : py_type_dict) {
              const auto type_name =
                  QString::fromStdString(py_type_name.cast<std::string>());
              const auto type_flags =
                  static_cast<TypeFlags>(py_type_flags.cast<std::int64_t>());
              types.append(QPair<QString, TypeFlags>{type_name, type_flags});
            }
            api.insert(category, types);
          }
        }
      };

  const py::dict public_objects_api =
      iprm_namespace.attr("OBJECT_CATEGORIES");
  populate_api(public_objects_api, public_objects_api_);

  const py::dict public_utility_api =
      iprm_namespace.attr("UTILITY_CATEGORY");
  populate_api(public_utility_api, public_utility_api_);

  public_api_.insert(public_objects_api_);
  public_api_.insert(public_utility_api_);

  Q_EMIT project_load_success();
}

void APIBridge::process_objects(Platform& platform,
                                const py::dict& py_objects) const {
  // TODO: setup data for gui/main thread more efficiently here
  for (const auto& [key, value] : py_objects) {
    const auto file_path = key.cast<std::string>();
    const auto normalized_file_path =
        QDir::toNativeSeparators(QString::fromStdString(file_path));
    py::list obj_list = value.cast<py::list>();
    QList<ObjectNode> objects;
    for (const auto& obj : obj_list) {
      objects.push_back(make_object_node(normalized_file_path, obj));
    }
    platform.objs_[normalized_file_path] = std::move(objects);
  }
  build_dependency_graph(platform);
}

ObjectNode APIBridge::make_object_node(const QString& file_path,
                                       const py::handle& py_obj) const {
  const auto cpp_obj_name = py_obj.attr("name").cast<std::string>();
  const auto cpp_obj_type_name =
      py_obj.get_type().attr("__name__").cast<std::string>();
  const auto cpp_obj_type_flags =
      static_cast<TypeFlags>(py_obj.attr("type_flags").cast<std::int64_t>());
  const py::list obj_dependencies = py_obj.attr("dependencies");
  std::vector<std::string> cpp_obj_dependencies;
  cpp_obj_dependencies.reserve(obj_dependencies.size());
  for (const auto& obj_dep : obj_dependencies) {
    cpp_obj_dependencies.push_back(py::cast<std::string>(obj_dep));
  }
  const auto obj_hex_colour = py_obj.attr("hex_colour").cast<std::string>();
  const auto cpp_obj_shape_type = py_obj.attr("shape_type").cast<std::string>();

  const auto obj_file_path = QDir::toNativeSeparators(file_path);
  const auto obj_file_dir_path = QFileInfo(obj_file_path).absolutePath();
  const QString proj_relative_dir_path =
      root_dir_.relativeFilePath(obj_file_dir_path);

  return ObjectNode{cpp_obj_name,          cpp_obj_type_name,
                    cpp_obj_type_flags,    cpp_obj_dependencies,
                    obj_hex_colour,        cpp_obj_shape_type,
                    proj_relative_dir_path};
}

void APIBridge::build_dependency_graph(Platform& platform_ctx) {
  platform_ctx.dep_graph_.emplace();
  auto& dep_graph = platform_ctx.dep_graph_.value();

  for (const auto& objects : platform_ctx.objs_) {
    for (const auto& obj : objects) {
      if (static_cast<bool>(obj.type & TypeFlags::TARGET)) {
        auto node = dep_graph.graph_.addNode();
        dep_graph.node_data_[node] = obj;
        dep_graph.target_map_[obj.name] = node;
      }
    }
  }

  // Second pass: add dependencies
  for (const auto& objects : platform_ctx.objs_) {
    for (const auto& obj : objects) {
      const auto is_target = static_cast<bool>(obj.type & TypeFlags::TARGET);
      if (auto deps = obj.dependencies; is_target) {
        for (const auto& dep : deps) {
          auto from_it = dep_graph.target_map_.find(obj.name);
          auto to_it = dep_graph.target_map_.find(dep);
          if (from_it != dep_graph.target_map_.end() &&
              to_it != dep_graph.target_map_.end()) {
            dep_graph.graph_.addArc(from_it->second, to_it->second);
          }
        }
      }
    }
  }
}

void APIBridge::load_project_file(const QString& file_path) {
  const auto normalized_file_path = QDir::toNativeSeparators(file_path);
  QHash<QString, PlatformFile> platform_file;
  for (auto& [platform_name, platform_ctx] : platforms_) {
    auto& objects = platform_ctx.objs_[normalized_file_path];
    objects.clear();
    try {
      py::list py_objects = platform_ctx.native_loader_.value().attr(
          "load_project_file")(file_path.toStdString());
      for (const auto& py_obj : py_objects) {
        objects.push_back(make_object_node(file_path, py_obj));
      }
      platform_file.insert(
          platform_name,
          PlatformFile{.objects_ = objects, .icon_ = icon(platform_name)});
    } catch (const py::error_already_set& e) {
      Q_EMIT project_file_load_failure(make_error(
          QString("Error loading project file '%0'").arg(file_path), e));
    }
    build_dependency_graph(platform_ctx);
  }
  Q_EMIT project_file_load_success(platform_file);
}

APIBridgeThread::APIBridgeThread() : QThread(nullptr), bridge_(), interp_() {
  bridge_.moveToThread(this);
  connect(&bridge_, &APIBridge::error, this, &APIBridgeThread::error);
  connect(&bridge_, &APIBridge::print_stdout, this,
          &APIBridgeThread::print_stdout);
  connect(&bridge_, &APIBridge::project_load_success, this,
          &APIBridgeThread::project_load_success);
  connect(&bridge_, &APIBridge::project_file_load_success, this,
          &APIBridgeThread::project_file_load_success);
  connect(&bridge_, &APIBridge::project_file_load_failure, this,
          &APIBridgeThread::project_file_load_failure);
}

void APIBridgeThread::set_root_dir(const QDir& root_dir) {
  bridge_.set_root_dir(root_dir);
}

void APIBridgeThread::capture_io() {
  py::gil_scoped_acquire acq;
  bridge_.capture_io();
}

void APIBridgeThread::destroy_sess() {
  py::gil_scoped_acquire acq;
  bridge_.destroy_sess();
}

void APIBridgeThread::load_builtin_backends() {
  py::gil_scoped_acquire acq;
  bridge_.load_builtin_backends();
}

void APIBridgeThread::load_plugin_backends(const QDir& plugin_dir) {
  py::gil_scoped_acquire acq;
  bridge_.load_plugin_backends(plugin_dir);
}

void APIBridgeThread::load_project() {
  py::gil_scoped_acquire acq;
  bridge_.load_project();
}

void APIBridgeThread::load_project_file(const QString& file_path) {
  py::gil_scoped_acquire acq;
  bridge_.load_project_file(file_path);
}


}  // namespace iprm