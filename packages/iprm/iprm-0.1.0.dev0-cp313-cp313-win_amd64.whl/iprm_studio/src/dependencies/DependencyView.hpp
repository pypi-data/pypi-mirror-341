/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"

#include <lemon/list_graph.h>
#include <QScrollArea>

class QStackedWidget;
class QTabWidget;

namespace iprm {

class LoadingWidget;
class DependencyGraphicsView;
class DependencyGraphicsScene;

class DependencyView final : public QScrollArea {
  Q_OBJECT
 public:
  explicit DependencyView(QWidget* parent = nullptr);

  void build_graph(const QString& platform_display_name,
                   const QIcon& platform_icon,
                   const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

  void load_graphs() const;

  void show_graphs(const QString& host_platform_display_name) const;

 Q_SIGNALS:
  void layout_failed(const QString& platform);

 private:
  QStackedWidget* stack_{nullptr};
  LoadingWidget* loading_page_{nullptr};
  QHash<QString, DependencyGraphicsView*> views_;
  QHash<QString, DependencyGraphicsScene*> scenes_;

  QTabWidget* platforms_{nullptr};
};

}  // namespace iprm
