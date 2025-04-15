/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "MainWindow.hpp"
#include "util/APIBridge.hpp"
#include "util/AppTheme.hpp"
#include "util/SplashScreen.hpp"

#include <QApplication>
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QDir>

int main(int argc, char** argv) {
  QApplication app(argc, argv);
  QApplication::setApplicationName("IPRM Studio");
  QApplication::setApplicationVersion("0.1.0-rc3");
  QApplication::setWindowIcon(QIcon(":/logos/iprm.svg"));

  QCommandLineParser parser;
  parser.addHelpOption();
  parser.addVersionOption();

  QCommandLineOption projdir_option(
      QStringList() << "p" << "projdir",
      QApplication::tr("Path to project directory"), QApplication::tr("path"));
  parser.addOption(projdir_option);

  QCommandLineOption plugindir_option(
      QStringList() << "plugindir",
      QApplication::tr("Path to plugins directory"), QApplication::tr("path"));
  parser.addOption(plugindir_option);

  parser.process(app);

  const QString project_dir = [&parser, &projdir_option]() {
    if (parser.isSet(projdir_option)) {
      return parser.value(projdir_option);
    }
    return QString{};
  }();

  const QString plugin_dir = [&parser, &plugindir_option]() {
    if (parser.isSet(plugindir_option)) {
      return parser.value(plugindir_option);
    }
    return QString{};
  }();

  iprm::APIBridgeThread api_bridge;
  if (!project_dir.isEmpty()) {
    const auto iprm_project_dir = QDir(QDir::toNativeSeparators(
        QDir::current().absoluteFilePath(QDir(project_dir).absolutePath())));
    api_bridge.set_root_dir(iprm_project_dir);
  }

  QApplication::connect(&api_bridge, &iprm::APIBridgeThread::error, &app,
                        [](const iprm::APIError&) {
                          // TODO: Log this somewhere? Main Window doesn't
                          //  exist yet and we may fail, so best place to put
                          //  it is to disk to help debug if project load
                          //  fails on startup
                        });

  iprm::SplashScreen splash;
  splash.show();
  QApplication::processEvents();

  api_bridge.load_builtin_backends();
  if (!plugin_dir.isEmpty()) {
    const auto iprm_plugin_dir = QDir(QDir::toNativeSeparators(
        QDir::current().absoluteFilePath(QDir(plugin_dir).absolutePath())));
    api_bridge.load_plugin_backends(iprm_plugin_dir);
  }

  auto set_light_theme = [&app]() {
    QFile ss(":/styles/light_theme_stylesheet.qss");
    ss.open(QFile::ReadOnly);
    app.setStyleSheet(QString::fromUtf8(ss.readAll()));
  };

  auto set_dark_theme = [&app]() {
    QFile ss(":/styles/dark_theme_stylesheet.qss");
    ss.open(QFile::ReadOnly);
    app.setStyleSheet(QString::fromUtf8(ss.readAll()));
  };

  auto& app_theme = iprm::AppTheme::instance();
  iprm::MainWindow window(api_bridge);
  QApplication::connect(
      &app_theme, &iprm::AppTheme::scheme_changed, &app,
      [&set_light_theme, &set_dark_theme](iprm::AppTheme::Scheme scheme) {
        switch (scheme) {
          case iprm::AppTheme::Scheme::Dark: {
            set_dark_theme();
            break;
          }
          case iprm::AppTheme::Scheme::Light:
          default: {
            set_light_theme();
            break;
          }
        }
      });
  app_theme.update_scheme(app_theme.os_scheme());
  if (!project_dir.isEmpty()) {
    QApplication::connect(&api_bridge, &iprm::APIBridgeThread::print_stdout,
                          &app, [](const QString&) {
                            // TODO: Log this somewhere? Main Window doesn't
                            //  exist yet and we may fail, so best place to put
                            //  it is to disk to help debug if project load
                            //  fails on startup
                          });
    QApplication::connect(
        &api_bridge, &iprm::APIBridgeThread::error, &app,
        [&app, &splash, &window, &api_bridge](const iprm::APIError& error) {
          QApplication::disconnect(&api_bridge, nullptr, &app, nullptr);
          splash.finish(nullptr);
          window.on_project_load_failed(error);
          window.show();
        });
    QApplication::connect(
        &api_bridge, &iprm::APIBridgeThread::project_load_success, &app,
        [project_dir, &app, &window, &splash, &api_bridge]() {
          QApplication::disconnect(&api_bridge, nullptr, &app, nullptr);
          splash.finish(nullptr);
          window.init();
          window.set_project(project_dir);
          window.on_project_loaded();
          window.show();
        });

    QMetaObject::invokeMethod(&api_bridge, &iprm::APIBridgeThread::load_project,
                              Qt::QueuedConnection);
  } else {
    splash.finish(nullptr);
    window.init();
    window.show();
  }

  return QApplication::exec();
}
