'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import {
  Container,
  VStack,
  Heading,
  Text,
  Button,
  Alert,
  AlertIcon,
  Spinner,
  Box,
} from '@chakra-ui/react';

export default function VerifyEmailPage() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams?.get('token');

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link');
      return;
    }

    const verifyEmail = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/auth/verify-email/${token}`,
          {
            method: 'GET',
          }
        );

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || 'Verification failed');
        }

        setStatus('success');
        setMessage('Your email has been verified successfully!');
      } catch (error) {
        setStatus('error');
        setMessage(
          error instanceof Error
            ? error.message
            : 'Failed to verify email. The link may be invalid or expired.'
        );
      }
    };

    verifyEmail();
  }, [token]);

  const renderContent = () => {
    switch (status) {
      case 'loading':
        return (
          <VStack spacing={4}>
            <Spinner size="xl" color="blue.500" />
            <Text>Verifying your email...</Text>
          </VStack>
        );

      case 'success':
        return (
          <VStack spacing={6}>
            <Alert status="success" borderRadius="md">
              <AlertIcon />
              {message}
            </Alert>
            <Button colorScheme="blue" onClick={() => router.push('/login')}>
              Go to Login
            </Button>
          </VStack>
        );

      case 'error':
        return (
          <VStack spacing={6}>
            <Alert status="error" borderRadius="md">
              <AlertIcon />
              {message}
            </Alert>
            <Box textAlign="center">
              <Text mb={4}>
                If you're having trouble verifying your email, you can request a new
                verification link.
              </Text>
              <Link href="/resend-verification" style={{ color: 'blue' }}>
                Resend Verification Email
              </Link>
            </Box>
          </VStack>
        );
    }
  };

  return (
    <Container maxW="container.sm" py={10}>
      <VStack spacing={8}>
        <Heading>Email Verification</Heading>
        {renderContent()}
      </VStack>
    </Container>
  );
} 