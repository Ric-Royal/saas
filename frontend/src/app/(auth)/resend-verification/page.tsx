'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
  Container,
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Text,
  Alert,
  AlertIcon,
  Box,
} from '@chakra-ui/react';

export default function ResendVerificationPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('idle');
    setMessage('');

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/resend-verification`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to resend verification email');
      }

      setStatus('success');
      setMessage('Verification email has been sent. Please check your inbox.');
    } catch (error) {
      setStatus('error');
      setMessage(
        error instanceof Error
          ? error.message
          : 'Failed to send verification email. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.sm" py={10}>
      <VStack spacing={8}>
        <Heading>Resend Verification Email</Heading>
        <Box w="100%" as="form" onSubmit={handleSubmit}>
          <VStack spacing={6}>
            {status !== 'idle' && (
              <Alert status={status} borderRadius="md">
                <AlertIcon />
                {message}
              </Alert>
            )}

            <Text textAlign="center" color="gray.600">
              Enter your email address and we'll send you a new verification link.
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
              Resend Verification Email
            </Button>

            <Text>
              Already verified?{' '}
              <Link href="/login" style={{ color: 'blue' }}>
                Sign In
              </Link>
            </Text>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
} 