import { Box, Heading, Container, Text, Stack } from '@chakra-ui/react'

export default function Home() {
  return (
    <Container maxW={'4xl'}>
      <Stack
        as={Box}
        textAlign={'center'}
        spacing={{ base: 8, md: 14 }}
        py={{ base: 20, md: 36 }}>
        <Heading
          fontWeight={600}
          fontSize={{ base: '2xl', sm: '4xl', md: '6xl' }}
          lineHeight={'110%'}>
          Tech Blog
        </Heading>
        <Text color={'gray.500'}>
          Stay updated with the latest technology trends and insights
        </Text>
      </Stack>
    </Container>
  )
} 