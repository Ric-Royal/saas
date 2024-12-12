import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Card,
  CardContent,
  Container,
  Grid,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Pagination,
  Button,
} from '@mui/material';
import { useAuth } from '@/contexts/AuthContext';
import axios from 'axios';
import Link from 'next/link';

interface Bill {
  id: number;
  title: string;
  description: string;
  status: string;
  created_at: string;
}

export default function BillsPage() {
  const { user } = useAuth();
  const [page, setPage] = useState(1);
  const [status, setStatus] = useState<string>('');
  const limit = 10;

  const { data, isLoading } = useQuery(
    ['bills', page, status],
    async () => {
      const params = new URLSearchParams({
        skip: ((page - 1) * limit).toString(),
        limit: limit.toString(),
        ...(status && { status }),
      });
      const response = await axios.get(`/api/v1/bills?${params}`);
      return response.data;
    }
  );

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Legislative Bills
        </Typography>
        {user?.is_superuser && (
          <Button
            variant="contained"
            color="primary"
            component={Link}
            href="/bills/new"
          >
            Create New Bill
          </Button>
        )}
      </Box>

      <Box sx={{ mb: 3 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Filter by Status</InputLabel>
          <Select
            value={status}
            label="Filter by Status"
            onChange={(e) => setStatus(e.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="draft">Draft</MenuItem>
            <MenuItem value="published">Published</MenuItem>
            <MenuItem value="under_review">Under Review</MenuItem>
            <MenuItem value="approved">Approved</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {data?.map((bill: Bill) => (
          <Grid item xs={12} key={bill.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component={Link} href={`/bills/${bill.id}`}>
                  {bill.title}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Status: {bill.status}
                </Typography>
                <Typography variant="body2" component="p">
                  {bill.description}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Created: {new Date(bill.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
        <Pagination
          count={Math.ceil((data?.length || 0) / limit)}
          page={page}
          onChange={(_, value) => setPage(value)}
          color="primary"
        />
      </Box>
    </Container>
  );
} 