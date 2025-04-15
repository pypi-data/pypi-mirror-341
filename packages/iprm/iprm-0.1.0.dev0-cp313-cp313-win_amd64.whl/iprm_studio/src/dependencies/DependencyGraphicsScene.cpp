/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "DependencyGraphicsScene.hpp"
#include "DependencyGraphItemFactory.hpp"

namespace iprm {

DependencyGraphicsScene::DependencyGraphicsScene(QObject* parent)
    : QGraphicsScene(parent),
      gvc_(gvContext()),
      item_factory_(new DependencyGraphItemFactory(this)) {
  setItemIndexMethod(NoIndex);
  assert(gvc_ != nullptr);
}

void DependencyGraphicsScene::build_graph(
    const lemon::ListDigraph& graph,
    const lemon::ListDigraph::NodeMap<ObjectNode>& node_data) {
  item_factory_->clear();
  clear();

  auto g = gv::create_graph("dependency_graph");

  std::unordered_map<int, Agnode_t*> gv_nodes;
  std::unordered_map<std::string, TypeFlags> gv_node_types;

  for (lemon::ListDigraph::NodeIt n(graph); n != lemon::INVALID; ++n) {
    const auto& data = node_data[n];
    const int node_id = graph.id(n);

    const auto name = data.name.toStdString();
    gv_node_types[name] = data.type;
    const auto target_type = data.type_name.toStdString();
    const auto shape_type = data.shape_type.toStdString();
    const auto hex_colour = data.hex_colour.toStdString();
    const auto obj_project_rel_dir_path =
        data.project_rel_dir_path.toStdString();
    gv_nodes[node_id] = add_node(g, node_id, name, target_type, shape_type,
                                 hex_colour, obj_project_rel_dir_path);
  }

  for (lemon::ListDigraph::ArcIt a(graph); a != lemon::INVALID; ++a) {
    auto source_id = graph.id(graph.source(a));
    auto target_id = graph.id(graph.target(a));

    add_edge(g, gv_nodes[source_id], gv_nodes[target_id]);
  }

  if (auto layout_res = gv::apply_layout(gvc_, g, "dot")) {
    for (auto& node : layout_res.value().nodes) {
      node.type = gv_node_types[node.name];
    }
    item_factory_->create(layout_res.value());
  } else {
    Q_EMIT layout_failed();
  }
}

}  // namespace iprm
