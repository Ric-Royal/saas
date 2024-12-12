'use client';

import {
  Box,
  Flex,
  Text,
  Button,
  Stack,
  Link,
  useColorModeValue,
} from '@chakra-ui/react';
import NextLink from 'next/link';

export default function Navbar() {
  return (
    <Box>
      <Flex
        bg={useColorModeValue('white', 'gray.800')}
        color={useColorModeValue('gray.600', 'white')}
        minH={'60px'}
        py={{ base: 2 }}
        px={{ base: 4 }}
        borderBottom={1}
        borderStyle={'solid'}
        borderColor={useColorModeValue('gray.200', 'gray.900')}
        align={'center'}>
        <Flex flex={{ base: 1 }} justify={{ base: 'center', md: 'start' }}>
          <Text
            textAlign={useColorModeValue('left', 'center')}
            fontFamily={'heading'}
            color={useColorModeValue('gray.800', 'white')}>
            SaaS Platform
          </Text>

          <Stack
            flex={{ base: 1, md: 0 }}
            justify={'flex-end'}
            direction={'row'}
            spacing={6}>
            <Link as={NextLink} href="/agri" px={2} py={1} rounded={'md'}>
              Agri-Insights
            </Link>
            <Link as={NextLink} href="/participation" px={2} py={1} rounded={'md'}>
              Public Participation
            </Link>
            <Link as={NextLink} href="/civilbot" px={2} py={1} rounded={'md'}>
              CivilBot
            </Link>
            <Link as={NextLink} href="/blog" px={2} py={1} rounded={'md'}>
              Tech Blog
            </Link>
          </Stack>
        </Flex>
      </Flex>
    </Box>
  );
} 