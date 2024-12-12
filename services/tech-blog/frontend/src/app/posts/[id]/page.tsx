'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Post } from '../../../types';
import { getPost, subscribeToPost, unsubscribeFromPost } from '../../../lib/api';
import Link from 'next/link';

export default function PostPage() {
  const params = useParams();
  const id = params?.id as string;
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const data = await getPost(id as string);
        setPost(data);
      } catch (err) {
        setError('Failed to fetch post');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();

    // Subscribe to real-time updates
    subscribeToPost(id as string, (updatedPost) => {
      setPost(updatedPost);
    });

    return () => {
      unsubscribeFromPost(id as string);
    };
  }, [id]);

  if (loading) return <div className="animate-pulse">Loading post...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!post) return <div>Post not found</div>;

  return (
    <article className="max-w-4xl mx-auto px-4 py-8">
      <Link
        href="/posts"
        className="inline-block mb-8 text-blue-500 hover:text-blue-600"
      >
        ← Back to Posts
      </Link>
      
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
        <div className="flex items-center justify-between text-gray-600">
          <div className="flex items-center">
            {post.author.avatar && (
              <img
                src={post.author.avatar}
                alt={post.author.name}
                className="w-8 h-8 rounded-full mr-3"
              />
            )}
            <span className="mr-4">{post.author.name}</span>
            <time dateTime={post.createdAt}>
              {new Date(post.createdAt).toLocaleDateString()}
            </time>
          </div>
          <div className="flex gap-2">
            {post.categories.map((category) => (
              <span
                key={category.id}
                className="px-3 py-1 rounded-full text-sm"
                style={{ backgroundColor: category.color + '20', color: category.color }}
              >
                {category.name}
              </span>
            ))}
          </div>
        </div>
      </header>

      <div className="prose prose-lg max-w-none">
        {post.content}
      </div>

      <footer className="mt-8 pt-8 border-t border-gray-200">
        <div className="flex flex-wrap gap-2">
          {post.tags.map((tag) => (
            <span
              key={tag.id}
              className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm"
            >
              #{tag.name}
            </span>
          ))}
        </div>
      </footer>
    </article>
  );
} 