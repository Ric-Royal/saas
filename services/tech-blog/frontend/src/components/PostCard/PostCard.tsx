import Link from 'next/link';
import { format } from 'date-fns';
import type { Post } from '@/types';

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  return (
    <article className="retro-box p-6">
      <h2 className="text-2xl font-bold mb-4">
        <Link href={`/posts/${post.slug}`} className="hover:text-primary">
          {post.title}
        </Link>
      </h2>
      <div className="text-sm text-gray-600 mb-4">
        <span>By {post.author.name}</span>
        <span className="mx-2">•</span>
        <span>{format(new Date(post.createdAt), 'MMM d, yyyy')}</span>
        <span className="mx-2">•</span>
        <span>{post.likes} likes</span>
      </div>
      <p className="text-gray-700 mb-4">{post.excerpt}</p>
      <div className="flex flex-wrap gap-2">
        {post.categories.map((category) => (
          <Link
            key={category.id}
            href={`/categories/${category.slug}`}
            className="text-sm bg-primary text-white px-2 py-1 rounded hover:bg-primary-dark"
          >
            {category.name}
          </Link>
        ))}
        {post.tags.map((tag) => (
          <Link
            key={tag.id}
            href={`/tags/${tag.slug}`}
            className="text-sm border border-gray-300 px-2 py-1 rounded hover:bg-gray-100"
          >
            #{tag.name}
          </Link>
        ))}
      </div>
    </article>
  );
} 