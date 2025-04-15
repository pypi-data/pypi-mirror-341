/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/graphviz.hpp"
#include "../util/APIBridge.hpp"

#include <lemon/list_graph.h>
#include <QGraphicsScene>

namespace iprm {

class DependencyGraphItemFactory;

class DependencyGraphicsScene : public QGraphicsScene {
  Q_OBJECT
 public:
  explicit DependencyGraphicsScene(QObject* parent = nullptr);

  void build_graph(const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

  DependencyGraphItemFactory* item_factory() const { return item_factory_; }

 Q_SIGNALS:
  void layout_failed();

 private:
  gv::ctx_ptr_t gvc_{nullptr};
  DependencyGraphItemFactory* item_factory_;
};

}  // namespace iprm
