'use client';

import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Button, Box, CircularProgress } from '@mui/material';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { Comment, TrendingUp, HowToVote, Description } from '@mui/icons-material';

interface Bill {
  id: string;
  title: string;
  status: string;
  commentCount: number;
  voteCount: number;
  lastUpdated: string;
}

interface Stats {
  totalBills: number;
  activeBills: number;
  totalParticipants: number;
  totalComments: number;
}

const PublicParticipation = () => {
  const [bills, setBills] = useState<Bill[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // In a real app, these would be actual API calls
        const billsResponse = await fetch('/api/public-participation/bills');
        const statsResponse = await fetch('/api/public-participation/stats');
        
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

  if (loading) {
    return (
      <DashboardLayout>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
          <CircularProgress />
        </Box>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Typography variant="h4" gutterBottom>
        Public Participation Portal
      </Typography>

      {/* Stats Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {[
          { icon: <Description />, title: 'Total Bills', value: stats?.totalBills || 0 },
          { icon: <TrendingUp />, title: 'Active Bills', value: stats?.activeBills || 0 },
          { icon: <HowToVote />, title: 'Total Participants', value: stats?.totalParticipants || 0 },
          { icon: <Comment />, title: 'Total Comments', value: stats?.totalComments || 0 },
        ].map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                height: '100%',
              }}
            >
              <Box sx={{ p: 1, color: 'primary.main' }}>{stat.icon}</Box>
              <Typography variant="h6">{stat.value}</Typography>
              <Typography variant="body2" color="text.secondary">
                {stat.title}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Recent Bills */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Recent Bills
      </Typography>
      <Grid container spacing={3}>
        {bills.map((bill) => (
          <Grid item xs={12} md={6} key={bill.id}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {bill.title}
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Status: {bill.status}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Last Updated: {new Date(bill.lastUpdated).toLocaleDateString()}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Comment fontSize="small" />
                  <Typography variant="body2">{bill.commentCount}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <HowToVote fontSize="small" />
                  <Typography variant="body2">{bill.voteCount}</Typography>
                </Box>
              </Box>
              <Button
                variant="outlined"
                sx={{ mt: 2 }}
                onClick={() => window.location.href = `/public-participation/bills/${bill.id}`}
              >
                View Details
              </Button>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </DashboardLayout>
  );
};

export default PublicParticipation; 