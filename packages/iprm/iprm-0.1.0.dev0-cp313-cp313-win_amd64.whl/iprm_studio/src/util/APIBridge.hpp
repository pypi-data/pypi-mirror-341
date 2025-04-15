/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../iprm/core/src/TypeFlags.hpp"
#include "APIError.hpp"

#include <lemon/list_graph.h>
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <QDir>
#include <QHash>
#include <QIcon>
#include <QObject>
#include <QPair>
#include <QString>
#include <QThread>
#include <QVariant>

#include <functional>
#include <optional>
#include <tuple>
#include <variant>

namespace py = pybind11;

namespace iprm {

struct ObjectNode {
  ObjectNode() = default;

  ObjectNode(const std::string& obj_name,
             const std::string& obj_type_name,
             const TypeFlags obj_type,
             const std::vector<std::string>& obj_dependencies,
             const std::string& obj_hex_color,
             const std::string& obj_shape_type,
             const QString& obj_project_rel_dir_path)
      : name(QString::fromStdString(obj_name)),
        type_name(QString::fromStdString(obj_type_name)),
        type(obj_type),
        hex_colour(QString::fromStdString(obj_hex_color)),
        shape_type(QString::fromStdString(obj_shape_type)),
        project_rel_dir_path(obj_project_rel_dir_path) {
    dependencies.reserve(static_cast<qsizetype>(obj_dependencies.size()));
    for (const auto& dependency : obj_dependencies) {
      dependencies.push_back(QString::fromStdString(dependency));
    }
  }

  void set_property(const QString& property, const QVariant& value) {
    properties.emplace(property, value);
  }

  QString name;
  QString type_name;
  TypeFlags type;
  QStringList dependencies;
  QString hex_colour;
  QString shape_type;
  QString project_rel_dir_path;
  QHash<QString, QVariant> properties;
};

struct PlatformFile {
  QList<ObjectNode> objects_;
  QIcon icon_;
};

struct PlatformProject {
  QHash<QString, PlatformFile> files_;
};

struct BackendGenerate {
};
struct BackendConfigure {
  QStringList args_;
};
struct BackendBuild {
  QStringList args_;
};
struct BackendTest {
  QStringList args_;
};
struct BackendInstall {
  QStringList args_;
};

using BackendCommand = std::variant<BackendGenerate,
                                    BackendConfigure,
                                    BackendBuild,
                                    BackendTest,
                                    BackendInstall>;

enum class BackendType { Builtin, Plugin };

struct SystemBackend {
  py::object klass_;
  std::vector<std::string> file_exts_;
  QString name_;
  QIcon icon_;
  BackendType type_{BackendType::Builtin};
  std::vector<BackendCommand> commands_;
};

class APIBridge : public QObject {
  Q_OBJECT

  friend class APIBridgeThread;

 public:
  explicit APIBridge(QObject* parent = nullptr);
  ~APIBridge();

  APIBridge(const APIBridge&) = delete;
  APIBridge& operator=(const APIBridge&) = delete;

  void set_root_dir(const QDir& root_dir);

  QStringList platforms() const;

  const QList<SystemBackend>& builtin_backends() const {
    return builtin_backends_;
  }

  const QList<SystemBackend>& plugin_backends() const {
    return plugin_backends_;
  }

  const QDir& plugins_dir() const { return plugins_dir_; }

  const QIcon& icon(const QString& platform) const;

  const QString& display(const QString& platform) const;

  QString host_platform_display_name() const {
    return host_platform_display_name_;
  }

  const std::vector<std::filesystem::path>& file_paths() const {
    return file_paths_;
  }

  const QString& version() const { return version_; }

  const QString& copyright() const { return copyright_; }

  const std::string& native_file_name() const { return native_file_name_; }

  std::tuple<
      std::reference_wrapper<const lemon::ListDigraph>,
      std::reference_wrapper<const lemon::ListDigraph::NodeMap<ObjectNode>>>
  dependency_graph(const QString& platform) const;

  const QHash<QString, QList<ObjectNode>>& objects(
      const QString& platform) const;

  static const QHash<QString, QString>& platform_names() {
    return platform_names_;
  }

  static const QStringList& supported_platform_names() {
    return supported_platform_names_;
  }

  static const QHash<QString, QList<QPair<QString, TypeFlags>>>& public_api() {
    return public_api_;
  }

  static const QHash<QString, QList<QPair<QString, TypeFlags>>>&
  public_objects_api() {
    return public_objects_api_;
  }

 public Q_SLOTS:
  void capture_io();
  void load_builtin_backends();
  void load_plugin_backends(const QDir& plugin_dir);
  void init_sess();
  void destroy_sess();
  void load_project();
  void load_project_file(const QString& file_path);

 Q_SIGNALS:
  void error(const APIError& error);

  void print_stdout(const QString& message);
  // TODO: print_stderr

  void project_load_success();

  void project_file_load_success(
      const QHash<QString, PlatformFile>& platform_file);
  void project_file_load_failure(const APIError& error);

 private:
  struct Platform {
    std::optional<py::object> native_loader_;

    QHash<QString, QList<ObjectNode>> objs_;

    struct DepGraph {
      DepGraph() : node_data_(graph_) {}
      lemon::ListDigraph graph_;
      lemon::ListDigraph::NodeMap<ObjectNode> node_data_;
      std::unordered_map<QString, lemon::ListDigraph::Node> target_map_;
    };
    std::optional<DepGraph> dep_graph_;
  };

  void process_objects(Platform& platform, const py::dict& py_objects) const;

  ObjectNode make_object_node(const QString& file_path,
                              const py::handle& py_obj) const;

  static void build_dependency_graph(Platform& platform_ctx);

  void generate(const py::object& generator_class,
                const std::function<void()>& notify_success);

  bool append_iprm_path();

  std::optional<py::object> iprm_;

  // TODO: Qt-ify all member variables/APIs, remove use of C++ STL, that is only
  //  required for interop with pybind11

  QDir root_dir_;
  QDir plugins_dir_;
  std::optional<py::object> sess_;
  QString version_;
  QString copyright_;
  std::string native_file_name_;
  std::vector<std::filesystem::path> file_paths_;
  QString host_platform_display_name_;
  // TODO: Change this into a QHash
  std::unordered_map<QString, Platform> platforms_;

  QList<SystemBackend> builtin_backends_;
  QList<SystemBackend> plugin_backends_;

  inline static QHash<QString, QString> platform_names_;
  inline static QStringList supported_platform_names_;

  inline static QHash<QString, QList<QPair<QString, TypeFlags>>>
      public_objects_api_;
  inline static QHash<QString, QList<QPair<QString, TypeFlags>>>
      public_utility_api_;
  inline static QHash<QString, QList<QPair<QString, TypeFlags>>> public_api_;
};

class APIBridgeThread : public QThread {
  Q_OBJECT

 public:
  explicit APIBridgeThread();

  void set_root_dir(const QDir& root_dir);

  const QString& version() const { return bridge_.version(); }

  const QString& copyright() const { return bridge_.copyright(); }

  const std::string& native_file_name() const {
    return bridge_.native_file_name();
  }

  const std::vector<std::filesystem::path>& file_paths() const {
    return bridge_.file_paths();
  }

  QStringList platforms() const { return bridge_.platforms(); }

  const QList<SystemBackend>& builtin_backends() const {
    return bridge_.builtin_backends();
  }

  const QList<SystemBackend>& plugin_backends() const {
    return bridge_.plugin_backends();
  }

  const QDir& plugins_dir() const { return bridge_.plugins_dir(); }

  const QIcon& icon(const QString& platform) const {
    return bridge_.icon(platform);
  }

  const QString& display(const QString& platform) const {
    return bridge_.display(platform);
  }

  QString host_platform_display_name() const {
    return bridge_.host_platform_display_name();
  }

  std::tuple<
      std::reference_wrapper<const lemon::ListDigraph>,
      std::reference_wrapper<const lemon::ListDigraph::NodeMap<ObjectNode>>>
  dependency_graph(const QString& platform) const {
    return bridge_.dependency_graph(platform);
  }

  const QHash<QString, QList<ObjectNode>>& objects(
      const QString& platform) const {
    return bridge_.objects(platform);
  }

 public Q_SLOTS:
  void capture_io();
  void load_builtin_backends();
  void load_plugin_backends(const QDir& plugin_dir);
  void destroy_sess();
  void load_project();
  void load_project_file(const QString& file_path);

 Q_SIGNALS:
  void error(const APIError& error);

  void print_stdout(const QString& message);

  void project_load_success();

  void project_file_load_success(
      const QHash<QString, PlatformFile>& platform_file);
  void project_file_load_failure(const APIError& error);

 private:
  QDir root_dir_;
  APIBridge bridge_;
  py::scoped_interpreter interp_;
};

}  // namespace iprm

Q_DECLARE_METATYPE(iprm::PlatformFile)
