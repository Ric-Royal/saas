import { Providers } from '@/components/providers/Providers';
import Navigation from '@/components/layout/Navigation';
import { Box } from '@mui/material';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navigation />
            <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
              {children}
            </Box>
          </Box>
        </Providers>
      </body>
    </html>
  );
} 