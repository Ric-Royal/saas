'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Card,
  CardContent,
  IconButton,
  TextField,
  InputAdornment
} from '@mui/material';
import {
  Notifications,
  Search as SearchIcon,
  TrendingUp,
  Description,
  Category
} from '@mui/icons-material';
import DashboardLayout from '../../components/layout/DashboardLayout';

interface Bill {
  id: string;
  title: string;
  status: string;
  category: string;
  lastUpdated: string;
  progress: number;
  subscribers: number;
}

interface BillStats {
  totalBills: number;
  activeBills: number;
  subscribedBills: number;
  recentUpdates: number;
  categoryDistribution: Array<{ category: string; count: number }>;
}

const BillBotPage = () => {
  const [bills, setBills] = useState<Bill[]>([]);
  const [stats, setStats] = useState<BillStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [billsResponse, statsResponse] = await Promise.all([
          fetch('/api/billbot/bills'),
          fetch('/api/billbot/stats')
        ]);

        const billsData = await billsResponse.json();
        const statsData = await statsResponse.json();

        setBills(billsData);
        setStats(statsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSubscribe = async (billId: string) => {
    try {
      await fetch(`/api/billbot/bills/${billId}/subscribe`, {
        method: 'POST'
      });
      // Refresh bills data after subscription
      const response = await fetch('/api/billbot/bills');
      const data = await response.json();
      setBills(data);
    } catch (error) {
      console.error('Error subscribing to bill:', error);
    }
  };

  const filteredBills = bills.filter(bill =>
    bill.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bill.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <DashboardLayout>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Total Bills
                  </Typography>
                  <Typography variant="h4">
                    {stats?.totalBills || 0}
                  </Typography>
                  <Description color="primary" />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Active Bills
                  </Typography>
                  <Typography variant="h4">
                    {stats?.activeBills || 0}
                  </Typography>
                  <TrendingUp color="success" />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Your Subscriptions
                  </Typography>
                  <Typography variant="h4">
                    {stats?.subscribedBills || 0}
                  </Typography>
                  <Notifications color="secondary" />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Recent Updates
                  </Typography>
                  <Typography variant="h4">
                    {stats?.recentUpdates || 0}
                  </Typography>
                  <Category color="info" />
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>

        {/* Bills Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                Bills Tracking
              </Typography>
              <TextField
                size="small"
                placeholder="Search bills..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Box>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Progress</TableCell>
                    <TableCell>Last Updated</TableCell>
                    <TableCell>Subscribers</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredBills.map((bill) => (
                    <TableRow key={bill.id}>
                      <TableCell>{bill.title}</TableCell>
                      <TableCell>
                        <Chip label={bill.category} size="small" />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={bill.status}
                          color={bill.status === 'Active' ? 'success' : 'default'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{bill.progress}%</TableCell>
                      <TableCell>{new Date(bill.lastUpdated).toLocaleDateString()}</TableCell>
                      <TableCell>{bill.subscribers}</TableCell>
                      <TableCell>
                        <IconButton
                          color="primary"
                          onClick={() => handleSubscribe(bill.id)}
                          title="Subscribe to updates"
                        >
                          <Notifications />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Category Distribution */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Category Distribution
            </Typography>
            <Grid container spacing={2}>
              {stats?.categoryDistribution.map((category) => (
                <Grid item xs={12} sm={6} md={4} key={category.category}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1">
                        {category.category}
                      </Typography>
                      <Typography variant="h6">
                        {category.count} bills
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </DashboardLayout>
  );
};

export default BillBotPage; 