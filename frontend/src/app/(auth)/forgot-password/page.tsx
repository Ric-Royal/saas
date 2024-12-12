'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Container,
  Box,
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Text,
  useToast,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const toast = useToast();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        throw new Error('Failed to send reset email');
      }

      setIsSuccess(true);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to send password reset email. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.sm" py={10}>
      <VStack spacing={8}>
        <Heading>Reset Password</Heading>
        {isSuccess ? (
          <Alert status="success" borderRadius="md">
            <AlertIcon />
            Password reset instructions have been sent to your email.
            Please check your inbox and follow the instructions.
          </Alert>
        ) : (
          <Box w="100%" as="form" onSubmit={handleSubmit}>
            <VStack spacing={4}>
              <Text textAlign="center" color="gray.600">
                Enter your email address and we'll send you instructions to reset your password.
              </Text>
              <FormControl isRequired>
                <FormLabel>Email</FormLabel>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                />
              </FormControl>

              <Button
                type="submit"
                colorScheme="blue"
                width="100%"
                isLoading={isLoading}
                loadingText="Sending..."
              >
                Send Reset Instructions
              </Button>

              <Text>
                Remember your password?{' '}
                <Link href="/login" style={{ color: 'blue' }}>
                  Sign In
                </Link>
              </Text>
            </VStack>
          </Box>
        )}
      </VStack>
    </Container>
  );
} 