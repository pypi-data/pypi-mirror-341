/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "APIModel.hpp"
#include "APIItem.hpp"

namespace iprm {

APIModel::APIModel(QObject* parent)
    : QAbstractItemModel(parent),
      root_(std::make_unique<APIItem>("NAMESPACE", TypeFlags::NONE)) {}

APIModel::~APIModel() = default;

void APIModel::load(
    const QHash<QString, QList<QPair<QString, TypeFlags>>>& public_api) {
  beginResetModel();
  QHashIterator public_api_itr(public_api);
  while (public_api_itr.hasNext()) {
    public_api_itr.next();
    const auto& category = public_api_itr.key();
    auto category_item =
        std::make_unique<APIItem>(category, TypeFlags::NONE, *root_);
    for (const auto& types = public_api_itr.value();
         const auto& [name, flags] : types) {
      // TODO: For the known third party types that derive form the main one,
      //  make them children of the CppThirdParty item instead of being its
      //  sibling
      category_item->append_child(
          std::make_unique<APIItem>(name, flags, *category_item));
    }
    root_->append_child(std::move(category_item));
  }
  endResetModel();
}

QVariant APIModel::data(const QModelIndex& index, const int role) const {
  if (!index.isValid()) {
    return QVariant{};
  }
  const auto item = static_cast<APIItem*>(index.internalPointer());
  return item->data(index, role);
}

Qt::ItemFlags APIModel::flags(const QModelIndex& index) const {
  if (!index.isValid()) {
    return Qt::NoItemFlags;
  }

  return QAbstractItemModel::flags(index);
}

QVariant APIModel::headerData(int, Qt::Orientation, int) const {
  return QVariant();
}

QModelIndex APIModel::index(const int row,
                            const int column,
                            const QModelIndex& parent) const {
  if (!hasIndex(row, column, parent)) {
    return QModelIndex();
  }

  APIItem::opt_ref_t parent_item;
  if (!parent.isValid()) {
    parent_item = *root_;
  } else {
    parent_item = *static_cast<APIItem*>(parent.internalPointer());
  }

  if (const APIItem::opt_ref_t child_item =
          parent_item.value().get().child(row)) {
    return createIndex(row, column, &child_item.value().get());
  }
  return QModelIndex();
}

QModelIndex APIModel::parent(const QModelIndex& index) const {
  if (!index.isValid()) {
    return QModelIndex();
  }

  const auto child_item = static_cast<APIItem*>(index.internalPointer());
  const auto parent_item = child_item->parent();
  if (!parent_item.has_value()) {
    return QModelIndex();
  }

  const auto& parent_item_ref = parent_item.value().get();
  if (&parent_item_ref == root_.get()) {
    return QModelIndex();
  }
  return createIndex(parent_item_ref.row(), 0, &parent_item_ref);
}

int APIModel::rowCount(const QModelIndex& parent) const {
  APIItem::opt_ref_t parent_item;
  if (!parent.isValid()) {
    parent_item = *root_;
  } else {
    parent_item = *static_cast<APIItem*>(parent.internalPointer());
  }
  return parent_item.value().get().child_count();
}

int APIModel::columnCount(const QModelIndex& parent) const {
  return 1;
}

APISortFilterProxyModel::APISortFilterProxyModel(QObject* parent)
    : QSortFilterProxyModel(parent) {
  category_order_["C++"] = 0;
  category_order_["Rust"] = 1;
  category_order_["General"] = 2;
  category_order_["Utilities"] = 3;
  setSortRole(Qt::DisplayRole);
  setDynamicSortFilter(true);
}

bool APISortFilterProxyModel::lessThan(const QModelIndex& source_left,
                                       const QModelIndex& source_right) const {
  if (!source_left.parent().isValid() && !source_right.parent().isValid()) {
    const QString left_text =
        sourceModel()->data(source_left, Qt::DisplayRole).toString();
    const QString right_text =
        sourceModel()->data(source_right, Qt::DisplayRole).toString();

    const bool left_in_order = category_order_.contains(left_text);
    const bool right_in_order = category_order_.contains(right_text);

    if (left_in_order && right_in_order) {
      return category_order_[left_text] < category_order_[right_text];
    } else if (left_in_order) {
      return true;
    } else if (right_in_order) {
      return false;
    }
  }

  return QSortFilterProxyModel::lessThan(source_left, source_right);
}

}  // namespace iprm
