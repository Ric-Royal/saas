'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Avatar,
  useToast,
  Heading,
  Text,
  Skeleton,
  SkeletonCircle,
  useBreakpointValue,
  Alert,
  AlertIcon,
  Grid,
  GridItem,
} from '@chakra-ui/react';

export default function ProfilePage() {
  const { user, updateProfile } = useAuth();
  const router = useRouter();
  const toast = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isPageLoading, setIsPageLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    avatar: user?.avatar || '',
  });

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        avatar: user.avatar || '',
      });
      setIsPageLoading(false);
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await updateProfile(formData);
      toast({
        title: 'Success',
        description: 'Profile updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update profile',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('avatar', file);

    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/profile/avatar`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload avatar');

      const data = await response.json();
      setFormData(prev => ({ ...prev, avatar: data.avatar }));
      
      toast({
        title: 'Success',
        description: 'Avatar updated successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to upload avatar',
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
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const padding = useBreakpointValue({ base: 4, md: 10 });
  const maxWidth = useBreakpointValue({ base: '100%', md: 'container.md' });
  const avatarSize = useBreakpointValue({ base: 'xl', md: '2xl' });

  if (!user) {
    router.push('/login');
    return null;
  }

  if (isPageLoading) {
    return (
      <Container maxW={maxWidth} py={padding}>
        <VStack spacing={8}>
          <Skeleton height="40px" width="200px" />
          <SkeletonCircle size="100px" />
          <Box w="100%">
            <VStack spacing={4}>
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
        <Heading size={{ base: 'lg', md: 'xl' }}>Edit Profile</Heading>
        <Box w="100%" as="form" onSubmit={handleSubmit}>
          <VStack spacing={6}>
            <Box textAlign="center">
              <Avatar
                size={avatarSize}
                src={formData.avatar || undefined}
                name={formData.name}
                cursor="pointer"
                onClick={handleAvatarClick}
                mb={4}
              />
              <input
                type="file"
                ref={fileInputRef}
                hidden
                accept="image/*"
                onChange={handleFileChange}
              />
              <Button
                size={{ base: 'sm', md: 'md' }}
                onClick={handleAvatarClick}
                isDisabled={isLoading}
              >
                Change Avatar
              </Button>
            </Box>

            <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={6} width="100%">
              <GridItem>
                <FormControl isDisabled={isLoading}>
                  <FormLabel>Name</FormLabel>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter your name"
                    size={{ base: 'md', md: 'lg' }}
                  />
                </FormControl>
              </GridItem>

              <GridItem>
                <FormControl isReadOnly>
                  <FormLabel>Email</FormLabel>
                  <Input
                    value={user.email}
                    disabled
                    size={{ base: 'md', md: 'lg' }}
                  />
                </FormControl>
              </GridItem>
            </Grid>

            {!user.isEmailVerified && (
              <Alert status="warning" borderRadius="md">
                <AlertIcon />
                <Text fontSize={{ base: 'sm', md: 'md' }}>
                  Your email is not verified.{' '}
                  <Button
                    variant="link"
                    colorScheme="blue"
                    size="sm"
                    onClick={() => router.push('/resend-verification')}
                  >
                    Verify now
                  </Button>
                </Text>
              </Alert>
            )}

            <Button
              type="submit"
              colorScheme="blue"
              width="100%"
              isLoading={isLoading}
              loadingText="Saving..."
              size={{ base: 'md', md: 'lg' }}
            >
              Save Changes
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
} 