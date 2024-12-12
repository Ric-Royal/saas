import React from 'react';
import { PostCard } from '../components/PostCard';
import { CategoryList } from '../components/CategoryList';
import { TagCloud } from '../components/TagCloud';
import { useQuery } from '@tanstack/react-query';
import { fetchPosts, fetchCategories, fetchTags } from '../lib/api';
import type { Post, Category, Tag } from '../types';

export default function HomePage() {
  const { data: postsData, isLoading: postsLoading } = useQuery<{ data: Post[] }>({
    queryKey: ['posts'],
    queryFn: () => fetchPosts()
  });

  const { data: categories = [], isLoading: categoriesLoading } = useQuery<Category[]>({
    queryKey: ['categories'],
    queryFn: () => fetchCategories()
  });

  const { data: tags = [], isLoading: tagsLoading } = useQuery<Tag[]>({
    queryKey: ['tags'],
    queryFn: () => fetchTags()
  });

  if (postsLoading || categoriesLoading || tagsLoading) {
    return <div>Loading...</div>;
  }

  const posts = postsData?.data || [];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
        {/* Main content */}
        <main className="md:col-span-8">
          <h1 className="text-4xl font-bold mb-8">Latest Posts</h1>
          <div className="space-y-8">
            {posts.map((post: Post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        </main>

        {/* Sidebar */}
        <aside className="md:col-span-4 space-y-8">
          <CategoryList categories={categories} />
          <TagCloud tags={tags} />
        </aside>
      </div>
    </div>
  );
} 