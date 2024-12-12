'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Text,
  useToast,
  Heading,
  Alert,
  AlertIcon,
  Skeleton,
  useBreakpointValue,
} from '@chakra-ui/react';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [isPageLoading, setIsPageLoading] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  // Simulate page load
  useState(() => {
    const timer = setTimeout(() => setIsPageLoading(false), 1000);
    return () => clearTimeout(timer);
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await login(formData.email, formData.password);
      const from = searchParams?.get('from') || '/';
      router.push(from);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Invalid email or password',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const padding = useBreakpointValue({ base: 4, md: 10 });
  const maxWidth = useBreakpointValue({ base: '100%', md: 'container.sm' });

  if (isPageLoading) {
    return (
      <Container maxW={maxWidth} py={padding}>
        <VStack spacing={8}>
          <Skeleton height="40px" width="200px" />
          <Box w="100%">
            <VStack spacing={4}>
              <Skeleton height="40px" width="100%" />
              <Skeleton height="40px" width="100%" />
              <Skeleton height="40px" width="100%" />
            </VStack>
          </Box>
        </VStack>
      </Container>
    );
  }

  return (
    <Container maxW={maxWidth} py={padding}>
      <VStack spacing={8}>
        <Heading>Sign In</Heading>
        <Box w="100%" as="form" onSubmit={handleSubmit}>
          <VStack spacing={4}>
            <FormControl isRequired isDisabled={isLoading}>
              <FormLabel>Email</FormLabel>
              <Input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
              />
            </FormControl>

            <FormControl isRequired isDisabled={isLoading}>
              <FormLabel>Password</FormLabel>
              <Input
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
              />
            </FormControl>

            <Button
              type="submit"
              colorScheme="blue"
              width="100%"
              isLoading={isLoading}
              loadingText="Signing in..."
            >
              Sign In
            </Button>

            <Text fontSize={{ base: 'sm', md: 'md' }}>
              Don't have an account?{' '}
              <Link href="/register" style={{ color: 'blue' }}>
                Sign Up
              </Link>
            </Text>

            <Link href="/forgot-password" style={{ color: 'blue', fontSize: '14px' }}>
              Forgot Password?
            </Link>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
} 