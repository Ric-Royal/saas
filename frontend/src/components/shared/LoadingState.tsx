'use client';

import {
  Box,
  Container,
  VStack,
  Skeleton,
  SkeletonCircle,
  SkeletonText,
  Spinner,
  useBreakpointValue,
} from '@chakra-ui/react';

interface LoadingStateProps {
  variant?: 'page' | 'section' | 'spinner' | 'card';
  count?: number;
  showImage?: boolean;
  containerWidth?: string;
}

export default function LoadingState({
  variant = 'page',
  count = 1,
  showImage = false,
  containerWidth = 'container.sm',
}: LoadingStateProps) {
  const padding = useBreakpointValue({ base: 4, md: 10 });
  const maxWidth = useBreakpointValue({ base: '100%', md: containerWidth });

  if (variant === 'spinner') {
    return (
      <Box
        height="100%"
        width="100%"
        display="flex"
        alignItems="center"
        justifyContent="center"
        py={10}
      >
        <Spinner
          thickness="4px"
          speed="0.65s"
          emptyColor="gray.200"
          color="blue.500"
          size="xl"
        />
      </Box>
    );
  }

  if (variant === 'card') {
    return (
      <Box
        padding="6"
        boxShadow="lg"
        bg="white"
        borderRadius="md"
        width="100%"
        animation="pulse 2s infinite"
      >
        {showImage && <SkeletonCircle size="10" />}
        <SkeletonText mt="4" noOfLines={4} spacing="4" skeletonHeight="2" />
      </Box>
    );
  }

  if (variant === 'section') {
    return (
      <VStack spacing={4} width="100%" py={4}>
        {Array(count)
          .fill(0)
          .map((_, i) => (
            <Skeleton key={i} height="40px" width="100%" />
          ))}
      </VStack>
    );
  }

  // Default page loading state
  return (
    <Container maxW={maxWidth} py={padding}>
      <VStack spacing={8}>
        <Skeleton height="40px" width="200px" />
        {showImage && <SkeletonCircle size="100px" />}
        <Box w="100%">
          <VStack spacing={4}>
            {Array(count)
              .fill(0)
              .map((_, i) => (
                <Skeleton key={i} height="40px" width="100%" />
              ))}
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
}

// Add keyframes for pulse animation
const style = document.createElement('style');
style.textContent = `
  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 1;
    }
  }
`;
document.head.appendChild(style); 