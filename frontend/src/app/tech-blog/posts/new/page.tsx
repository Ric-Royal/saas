'use client';

import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Button,
  Select,
  HStack,
  useToast,
  Text,
  Image,
  IconButton,
  Tag,
  TagLabel,
  TagCloseButton,
  Flex,
} from '@chakra-ui/react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { FiUpload, FiX } from 'react-icons/fi';

const ReactMarkdown = dynamic(() => import('react-markdown').then(mod => mod.default), {
  ssr: false,
  loading: () => <p>Loading preview...</p>
});

interface Category {
  _id: string;
  name: string;
}

interface Tag {
  _id: string;
  name: string;
}

export default function NewPost() {
  const router = useRouter();
  const toast = useToast();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [excerpt, setExcerpt] = useState('');
  const [category, setCategory] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [featuredImage, setFeaturedImage] = useState('');
  const [imagePreview, setImagePreview] = useState('');
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Fetch categories and tags when component mounts
    const fetchData = async () => {
      try {
        const [categoriesRes, tagsRes] = await Promise.all([
          fetch('/api/tech-blog/categories'),
          fetch('/api/tech-blog/tags')
        ]);

        if (categoriesRes.ok && tagsRes.ok) {
          const categoriesData = await categoriesRes.json();
          const tagsData = await tagsRes.json();
          setCategories(categoriesData);
          setTags(tagsData);
        }
      } catch (error) {
        toast({
          title: 'Error fetching data',
          description: 'Unable to load categories and tags',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    fetchData();
  }, [toast]);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        const formData = new FormData();
        formData.append('image', file);

        const response = await fetch('/api/tech-blog/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setFeaturedImage(data.url);
          setImagePreview(data.url);
        }
      } catch (error) {
        toast({
          title: 'Error uploading image',
          description: 'Unable to upload the image',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('/api/tech-blog/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          content,
          excerpt,
          category,
          tags: selectedTags,
          featuredImage,
          status: 'draft', // Default to draft
        }),
      });

      if (response.ok) {
        toast({
          title: 'Success',
          description: 'Post created successfully',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        router.push('/tech-blog');
      } else {
        throw new Error('Failed to create post');
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create post',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={6} align="stretch">
        <Text fontSize="2xl" fontWeight="bold">Create New Post</Text>

        <form onSubmit={handleSubmit}>
          <VStack spacing={6} align="stretch">
            <FormControl isRequired>
              <FormLabel>Title</FormLabel>
              <Input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter post title"
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel>Excerpt</FormLabel>
              <Textarea
                value={excerpt}
                onChange={(e) => setExcerpt(e.target.value)}
                placeholder="Enter a brief excerpt"
                rows={3}
              />
            </FormControl>

            <FormControl mb={4}>
              <FormLabel>Content</FormLabel>
              <VStack align="stretch" spacing={4}>
                <Textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  minHeight="400px"
                  placeholder="Write your content in markdown..."
                />
                <Box p={4} borderWidth="1px" borderRadius="md">
                  <ReactMarkdown>{content}</ReactMarkdown>
                </Box>
              </VStack>
            </FormControl>

            <FormControl isRequired>
              <FormLabel>Category</FormLabel>
              <Select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Select category"
              >
                {categories.map((cat) => (
                  <option key={cat._id} value={cat._id}>
                    {cat.name}
                  </option>
                ))}
              </Select>
            </FormControl>

            <FormControl>
              <FormLabel>Tags</FormLabel>
              <Select
                placeholder="Select tags"
                onChange={(e) => {
                  if (!selectedTags.includes(e.target.value)) {
                    setSelectedTags([...selectedTags, e.target.value]);
                  }
                }}
              >
                {tags.map((tag) => (
                  <option key={tag._id} value={tag._id}>
                    {tag.name}
                  </option>
                ))}
              </Select>
              <Flex mt={2} flexWrap="wrap" gap={2}>
                {selectedTags.map((tagId) => {
                  const tag = tags.find((t) => t._id === tagId);
                  return tag ? (
                    <Tag
                      key={tag._id}
                      size="md"
                      borderRadius="full"
                      variant="solid"
                      colorScheme="blue"
                    >
                      <TagLabel>{tag.name}</TagLabel>
                      <TagCloseButton
                        onClick={() => setSelectedTags(selectedTags.filter(id => id !== tagId))}
                      />
                    </Tag>
                  ) : null;
                })}
              </Flex>
            </FormControl>

            <FormControl>
              <FormLabel>Featured Image</FormLabel>
              <HStack>
                <Button
                  as="label"
                  htmlFor="image-upload"
                  leftIcon={<FiUpload />}
                  cursor="pointer"
                >
                  Upload Image
                  <Input
                    id="image-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    display="none"
                  />
                </Button>
                {imagePreview && (
                  <IconButton
                    aria-label="Remove image"
                    icon={<FiX />}
                    onClick={() => {
                      setFeaturedImage('');
                      setImagePreview('');
                    }}
                  />
                )}
              </HStack>
              {imagePreview && (
                <Box mt={4}>
                  <Image
                    src={imagePreview}
                    alt="Preview"
                    maxH="200px"
                    objectFit="cover"
                    borderRadius="md"
                  />
                </Box>
              )}
            </FormControl>

            <HStack spacing={4} justify="flex-end">
              <Button
                onClick={() => router.back()}
                variant="outline"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                colorScheme="blue"
                isLoading={isLoading}
              >
                Create Post
              </Button>
            </HStack>
          </VStack>
        </form>
      </VStack>
    </Container>
  );
} 