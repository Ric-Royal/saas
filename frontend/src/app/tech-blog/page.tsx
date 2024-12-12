'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Input, InputGroup, InputLeftElement, Box, Container, Heading, Text, Button, SimpleGrid, Flex, Tag, Avatar, useColorModeValue } from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  author: string;
  date: string;
  category: string;
  readTime: string;
  imageUrl?: string;
}

// Mock data - will be replaced with API calls
const mockPosts: BlogPost[] = [
  {
    id: "1",
    title: "The Evolution of Microservices Architecture",
    excerpt: "Explore how microservices architecture has transformed modern software development and what the future holds...",
    author: "Sarah Johnson",
    date: "2023-12-10",
    category: "Architecture",
    readTime: "7 min read",
    imageUrl: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
  },
  {
    id: "2",
    title: "AI in 2024: Trends and Predictions",
    excerpt: "A comprehensive look at artificial intelligence trends that will shape the technology landscape in 2024...",
    author: "Michael Chen",
    date: "2023-12-09",
    category: "Artificial Intelligence",
    readTime: "5 min read",
    imageUrl: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
  },
  {
    id: "3",
    title: "Securing Your Cloud Infrastructure",
    excerpt: "Best practices and essential tips for maintaining robust security in cloud environments...",
    author: "Alex Rivera",
    date: "2023-12-08",
    category: "Cloud Computing",
    readTime: "6 min read",
    imageUrl: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
  }
];

const categories = [
  "All",
  "Architecture",
  "Artificial Intelligence",
  "Cloud Computing",
  "DevOps",
  "Security",
  "Web Development"
];

export default function TechBlog() {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [posts, setPosts] = useState<BlogPost[]>(mockPosts);

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const filteredPosts = posts.filter(post => {
    const matchesCategory = selectedCategory === "All" || post.category === selectedCategory;
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <Container maxW="7xl" py={8}>
      <Flex justify="space-between" align="center" mb={8}>
        <Heading size="xl">Tech Blog</Heading>
        <Link href="/tech-blog/new" passHref>
          <Button colorScheme="blue">Write New Post</Button>
        </Link>
      </Flex>

      <Flex gap={4} mb={8} direction={{ base: 'column', md: 'row' }}>
        <Box flex={1}>
          <InputGroup size="lg">
            <InputLeftElement pointerEvents='none'>
              <SearchIcon color='gray.300' />
            </InputLeftElement>
            <Input
              placeholder="Search articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              size="lg"
            />
          </InputGroup>
        </Box>
        <Box overflowX="auto" whiteSpace="nowrap">
          <Flex gap={2}>
            {categories.map((category) => (
              <Button
                key={category}
                size="md"
                variant={selectedCategory === category ? 'solid' : 'outline'}
                colorScheme="blue"
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </Button>
            ))}
          </Flex>
        </Box>
      </Flex>

      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
        {filteredPosts.map((post) => (
          <Link href={`/tech-blog/posts/${post.id}`} key={post.id}>
            <Box
              borderWidth="1px"
              borderRadius="lg"
              overflow="hidden"
              bg={bgColor}
              borderColor={borderColor}
              transition="all 0.2s"
              _hover={{ transform: 'translateY(-4px)', shadow: 'lg' }}
            >
              {post.imageUrl && (
                <Box h="200px" overflow="hidden">
                  <img
                    src={post.imageUrl}
                    alt={post.title}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                </Box>
              )}
              <Box p={6}>
                <Tag size="sm" colorScheme="blue" mb={2}>
                  {post.category}
                </Tag>
                <Heading size="md" mb={2}>
                  {post.title}
                </Heading>
                <Text color="gray.600" noOfLines={2} mb={4}>
                  {post.excerpt}
                </Text>
                <Flex align="center" justify="space-between">
                  <Flex align="center">
                    <Avatar size="sm" name={post.author} mr={2} />
                    <Text fontSize="sm">{post.author}</Text>
                  </Flex>
                  <Text fontSize="sm" color="gray.500">
                    {post.readTime}
                  </Text>
                </Flex>
              </Box>
            </Box>
          </Link>
        ))}
      </SimpleGrid>

      {filteredPosts.length === 0 && (
        <Box textAlign="center" py={10}>
          <Text fontSize="lg" color="gray.600">
            No posts found matching your criteria
          </Text>
        </Box>
      )}
    </Container>
  );
} 