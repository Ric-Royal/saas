import React from 'react';
import Link from 'next/link';
import { FaFolder } from 'react-icons/fa';

interface Category {
  id: string;
  name: string;
  slug: string;
  postCount: number;
  color: string;
}

interface CategoryListProps {
  categories: Category[];
}

export function CategoryList({ categories }: CategoryListProps) {
  return (
    <div className="category-list">
      {categories.map((category) => (
        <Link
          key={category.id}
          href={`/categories/${category.slug}`}
          className="category-item"
          style={{ '--category-color': category.color } as React.CSSProperties}
        >
          <div className="category-icon">
            <FaFolder />
          </div>
          <div className="category-info">
            <span className="category-name">{category.name}</span>
            <span className="category-count">({category.postCount})</span>
          </div>
        </Link>
      ))}
    </div>
  );
} 