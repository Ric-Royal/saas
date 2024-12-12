'use client';

import { ReactNode, useEffect, useState } from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { ThemeProvider, StyledEngineProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from '../../theme/theme';
import { AuthProvider } from '../../contexts/AuthContext';
import { LoadingProvider } from './LoadingProvider';

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <StyledEngineProvider injectFirst>
      <ChakraProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AuthProvider>
            <LoadingProvider>
              {children}
            </LoadingProvider>
          </AuthProvider>
        </ThemeProvider>
      </ChakraProvider>
    </StyledEngineProvider>
  );
} 