/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/AssetCache.hpp"

#include <QIcon>
#include <QModelIndex>
#include <QVariant>

#include <functional>
#include <optional>
#include <ranges>
#include <vector>

namespace iprm {

class APIItem {
 public:
  using opt_ref_t = std::optional<std::reference_wrapper<APIItem>>;

  explicit APIItem(QString name,
                   TypeFlags flags,
                   const opt_ref_t parent = std::nullopt)
      : name_(std::move(name)), flags_(flags), parent_(parent) {}

  void append_child(std::unique_ptr<APIItem> child) {
    children_.push_back(std::move(child));
  }

  [[nodiscard]] opt_ref_t child(const int row) const {
    if (row < 0 || row >= children_.size()) {
      return std::nullopt;
    }
    return *children_.at(row);
  }

  [[nodiscard]] int child_count() const {
    return static_cast<int>(children_.size());
  }

  [[nodiscard]] opt_ref_t parent() const { return parent_; }

  [[nodiscard]] int row() const {
    if (!parent_.has_value()) {
      return 0;
    }

    const auto& children = parent_.value().get().children_;
    const auto child_itr = std::ranges::find_if(
        children, [this](const std::unique_ptr<APIItem>& child) {
          return this == child.get();
        });
    if (child_itr == children.end()) {
      return 0;
    }
    return static_cast<int>(std::distance(children.begin(), child_itr));
  }

  [[nodiscard]] QVariant data(const QModelIndex& index, const int role) const {
    if (index.column() != 0) {
      return QVariant{};
    }

    switch (role) {
      case Qt::DisplayRole: {
        return name_;
      }
      case Qt::DecorationRole: {
        if (index.parent().data().toString() == "Utilities") {
          if (name_.endsWith("Builder")) {
            return AssetCache::builder_icon();
          } else if (name_ == "Env") {
            return AssetCache::env_icon();
          } else if (name_.endsWith("Dir")) {
            return AssetCache::folder_icon();
          }
        } else {
          return AssetCache::object_type_icon(flags_);
        }
      }
      default:
        break;
    }
    return QVariant{};
  }

 private:
  QString name_;
  TypeFlags flags_;
  opt_ref_t parent_;
  std::vector<std::unique_ptr<APIItem>> children_;
};

}  // namespace iprm
