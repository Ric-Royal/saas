import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

interface Tag {
  id: string;
  name: string;
  slug: string;
  postCount: number;
  color: string;
}

interface TagCloudProps {
  tags: Tag[];
}

export function TagCloud({ tags }: TagCloudProps) {
  // Sort tags by post count
  const sortedTags = [...tags].sort((a, b) => b.postCount - a.postCount);

  // Calculate font size based on post count
  const maxCount = Math.max(...tags.map(t => t.postCount));
  const minCount = Math.min(...tags.map(t => t.postCount));
  const getFontSize = (count: number) => {
    const minSize = 0.8;
    const maxSize = 1.5;
    const size = minSize + (count - minCount) * (maxSize - minSize) / (maxCount - minCount);
    return `${size}rem`;
  };

  return (
    <div className="tag-cloud">
      {sortedTags.map((tag, index) => (
        <motion.div
          key={tag.id}
          className="tag-item-wrapper"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.3,
            delay: index * 0.1,
            type: 'spring',
            stiffness: 100
          }}
        >
          <Link
            href={`/tags/${tag.slug}`}
            className="tag-item glitch-effect"
            style={{
              fontSize: getFontSize(tag.postCount),
              '--tag-color': tag.color
            } as React.CSSProperties}
          >
            <span className="tag-name">{tag.name}</span>
            <span className="tag-count">({tag.postCount})</span>
          </Link>
        </motion.div>
      ))}

      {/* Retro decoration */}
      <div className="tag-cloud-decoration">
        <pre className="ascii-art">
          {`
          [TAGS.SYS]
          =========
          `}
        </pre>
      </div>
    </div>
  );
} 