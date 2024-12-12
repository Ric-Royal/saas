'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  Box,
  Container,
  Heading,
  Text,
  Avatar,
  Flex,
  Tag,
  IconButton,
  useColorModeValue,
  Divider,
  Button,
  HStack,
} from '@chakra-ui/react';
import { FaTwitter, FaLinkedin, FaFacebook, FaBookmark, FaHeart } from 'react-icons/fa';

interface BlogPost {
  id: string;
  title: string;
  content: string;
  author: string;
  date: string;
  category: string;
  readTime: string;
  imageUrl?: string;
}

// Mock data - will be replaced with API call
const mockPost: BlogPost = {
  id: "1",
  title: "The Evolution of Microservices Architecture",
  content: `
# The Evolution of Microservices Architecture

In recent years, microservices architecture has revolutionized how we build and deploy applications. This architectural style has become increasingly popular among organizations of all sizes, from startups to enterprise-level companies. Let's explore why this shift occurred and what it means for the future of software development.

## The Monolithic Past

Traditional monolithic applications were built as single, autonomous units. This meant that:

- All functionality was packaged into a single application
- Updates required deploying the entire application
- Scaling meant scaling everything, even if only one component needed it

## Enter Microservices

Microservices architecture breaks down applications into smaller, independent services that:

- Can be deployed independently
- Are organized around business capabilities
- Can be written in different programming languages
- Can scale independently

### Key Benefits

1. **Improved Scalability**
   - Services can be scaled independently
   - Resources can be allocated more efficiently

2. **Better Fault Isolation**
   - Issues in one service don't necessarily affect others
   - Easier to identify and fix problems

3. **Faster Development**
   - Teams can work independently
   - Smaller codebases are easier to understand
   - Faster deployment cycles

## Best Practices

When implementing microservices, consider:

1. Service Independence
2. Data Management
3. Communication Patterns
4. Monitoring and Logging
5. Security Considerations

## Looking Ahead

The future of microservices architecture looks promising with:

- Increased adoption of serverless architectures
- Better tooling and frameworks
- Improved monitoring solutions
- Enhanced security patterns

## Conclusion

Microservices architecture continues to evolve, and staying updated with best practices and patterns is crucial for success in modern software development.
`,
  author: "Sarah Johnson",
  date: "2023-12-10",
  category: "Architecture",
  readTime: "7 min read",
  imageUrl: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80"
};

export default function BlogPost() {
  const params = useParams();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [isLiked, setIsLiked] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    if (!params?.id) return;
    setPost(mockPost);
  }, [params?.id]);

  if (!post) {
    return (
      <Container maxW="4xl" py={8}>
        <Text>Loading...</Text>
      </Container>
    );
  }

  const shareUrl = typeof window !== 'undefined' ? window.location.href : '';

  return (
    <Container maxW="4xl" py={8}>
      <Box
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
        bg={bgColor}
        borderColor={borderColor}
      >
        {post.imageUrl && (
          <Box h="400px" overflow="hidden">
            <img
              src={post.imageUrl}
              alt={post.title}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </Box>
        )}

        <Box p={8}>
          <Tag size="md" colorScheme="blue" mb={4}>
            {post.category}
          </Tag>

          <Heading size="xl" mb={4}>
            {post.title}
          </Heading>

          <Flex align="center" mb={8}>
            <Avatar size="md" name={post.author} mr={4} />
            <Box>
              <Text fontWeight="bold">{post.author}</Text>
              <Text fontSize="sm" color="gray.500">
                {new Date(post.date).toLocaleDateString()} · {post.readTime}
              </Text>
            </Box>
          </Flex>

          <Divider mb={8} />

          <Box className="prose lg:prose-xl" dangerouslySetInnerHTML={{ __html: post.content }} />

          <Divider my={8} />

          <Flex justify="space-between" align="center">
            <HStack spacing={2}>
              <IconButton
                aria-label="Like post"
                icon={<FaHeart />}
                colorScheme={isLiked ? 'red' : 'gray'}
                variant="ghost"
                onClick={() => setIsLiked(!isLiked)}
              />
              <IconButton
                aria-label="Bookmark post"
                icon={<FaBookmark />}
                colorScheme={isBookmarked ? 'blue' : 'gray'}
                variant="ghost"
                onClick={() => setIsBookmarked(!isBookmarked)}
              />
            </HStack>

            <HStack spacing={2}>
              <IconButton
                as="a"
                href={`https://twitter.com/intent/tweet?url=${shareUrl}`}
                target="_blank"
                aria-label="Share on Twitter"
                icon={<FaTwitter />}
                colorScheme="twitter"
                variant="ghost"
              />
              <IconButton
                as="a"
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${shareUrl}`}
                target="_blank"
                aria-label="Share on LinkedIn"
                icon={<FaLinkedin />}
                colorScheme="linkedin"
                variant="ghost"
              />
              <IconButton
                as="a"
                href={`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`}
                target="_blank"
                aria-label="Share on Facebook"
                icon={<FaFacebook />}
                colorScheme="facebook"
                variant="ghost"
              />
            </HStack>
          </Flex>
        </Box>
      </Box>
    </Container>
  );
} 