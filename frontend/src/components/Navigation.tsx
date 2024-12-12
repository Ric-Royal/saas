'use client';

import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import Link from 'next/link';

export function Navigation() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link href="/" style={{ color: 'white', textDecoration: 'none' }}>
            SaaS Platform
          </Link>
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Link href="/agri-insights" style={{ color: 'white', textDecoration: 'none' }}>
            <Button color="inherit">Agri Insights</Button>
          </Link>
          <Link href="/public-participation" style={{ color: 'white', textDecoration: 'none' }}>
            <Button color="inherit">Public Participation</Button>
          </Link>
          <Link href="/civilbot" style={{ color: 'white', textDecoration: 'none' }}>
            <Button color="inherit">CivilBot</Button>
          </Link>
          <Link href="/tech-blog" style={{ color: 'white', textDecoration: 'none' }}>
            <Button color="inherit">Tech Blog</Button>
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
} 