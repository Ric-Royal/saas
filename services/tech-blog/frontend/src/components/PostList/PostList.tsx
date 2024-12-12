import React, { useEffect, useState } from 'react';
import { Post } from '../../types';
import { getPosts } from '../../lib/api';
import Link from 'next/link';

const PostList: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const data = await getPosts();
        setPosts(data);
      } catch (err) {
        setError('Failed to fetch posts');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) return <div className="animate-pulse">Loading posts...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {posts.map((post) => (
        <article
          key={post.id}
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
        >
          <Link href={`/posts/${post.id}`}>
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-2">{post.title}</h2>
              <p className="text-gray-600 mb-4">{post.excerpt}</p>
              <div className="flex items-center justify-between text-sm text-gray-500">
                <div className="flex items-center">
                  {post.author.avatar && (
                    <img
                      src={post.author.avatar}
                      alt={post.author.name}
                      className="w-6 h-6 rounded-full mr-2"
                    />
                  )}
                  <span>{post.author.name}</span>
                </div>
                <time dateTime={post.createdAt}>
                  {new Date(post.createdAt).toLocaleDateString()}
                </time>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {post.categories.map((category) => (
                  <span
                    key={category.id}
                    className="px-2 py-1 text-xs rounded-full"
                    style={{ backgroundColor: category.color + '20', color: category.color }}
                  >
                    {category.name}
                  </span>
                ))}
              </div>
            </div>
          </Link>
        </article>
      ))}
    </div>
  );
};

export default PostList; 