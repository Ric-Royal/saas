'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Box, Button, Container, Typography } from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';

export default function UnauthorizedPage() {
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 3,
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Access Denied
        </Typography>
        <Typography variant="body1" color="text.secondary" align="center">
          You don't have permission to access this page. Please contact your administrator if you believe this is a mistake.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => router.push('/')}
        >
          Return to Home
        </Button>
      </Box>
    </Container>
  );
} 