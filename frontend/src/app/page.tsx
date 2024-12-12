import { Box, Heading, Container, Text, Button, Stack } from '@chakra-ui/react'

export default function Home() {
  return (
    <Container maxW={'3xl'}>
      <Stack
        as={Box}
        textAlign={'center'}
        spacing={{ base: 8, md: 14 }}
        py={{ base: 20, md: 36 }}>
        <Heading
          fontWeight={600}
          fontSize={{ base: '2xl', sm: '4xl', md: '6xl' }}
          lineHeight={'110%'}>
          Welcome to <br />
          <Text as={'span'} color={'green.400'}>
            Our SaaS Platform
          </Text>
        </Heading>
        <Text color={'gray.500'}>
          Explore our services: Agricultural Insights, Public Participation,
          Civil Services Bot, and Tech Blog
        </Text>
        <Stack
          direction={'column'}
          spacing={3}
          align={'center'}
          alignSelf={'center'}
          position={'relative'}>
          <Button
            colorScheme={'green'}
            bg={'green.400'}
            rounded={'full'}
            px={6}
            _hover={{
              bg: 'green.500',
            }}>
            Get Started
          </Button>
        </Stack>
      </Stack>
    </Container>
  )
} 