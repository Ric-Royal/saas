'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Divider,
  Avatar,
  CircularProgress,
  Chip,
  Grid
} from '@mui/material';
import DashboardLayout from '../../../../components/layout/DashboardLayout';
import { ThumbUp, ThumbDown, Comment as CommentIcon } from '@mui/icons-material';

interface Comment {
  id: string;
  user: {
    name: string;
    avatar: string;
  };
  content: string;
  timestamp: string;
  votes: number;
}

interface Bill {
  id: string;
  title: string;
  description: string;
  status: string;
  proposedDate: string;
  lastUpdated: string;
  votes: {
    up: number;
    down: number;
  };
  comments: Comment[];
}

const BillView = () => {
  const params = useParams();
  const billId = params?.id as string;
  const [bill, setBill] = useState<Bill | null>(null);
  const [loading, setLoading] = useState(true);
  const [comment, setComment] = useState('');

  useEffect(() => {
    const fetchBill = async () => {
      try {
        const response = await fetch(`/api/public-participation/bills/${billId}`);
        const data = await response.json();
        setBill(data);
      } catch (error) {
        console.error('Error fetching bill:', error);
      } finally {
        setLoading(false);
      }
    };

    if (billId) {
      fetchBill();
    }
  }, [billId]);

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Implementation for submitting comments
    console.log('Submitting comment:', comment);
    setComment('');
  };

  if (loading) {
    return (
      <DashboardLayout>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
          <CircularProgress />
        </Box>
      </DashboardLayout>
    );
  }

  if (!bill) {
    return (
      <DashboardLayout>
        <Typography variant="h6">Bill not found</Typography>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box>
            <Typography variant="h4" gutterBottom>
              {bill.title}
            </Typography>
            <Chip
              label={bill.status}
              color={bill.status === 'Open' ? 'success' : 'default'}
              sx={{ mb: 2 }}
            />
          </Box>
          <Box>
            <Button
              startIcon={<ThumbUp />}
              variant="outlined"
              color="success"
              sx={{ mr: 1 }}
            >
              Support ({bill.votes.up})
            </Button>
            <Button
              startIcon={<ThumbDown />}
              variant="outlined"
              color="error"
            >
              Oppose ({bill.votes.down})
            </Button>
          </Box>
        </Box>

        <Typography variant="body1" paragraph>
          {bill.description}
        </Typography>

        <Box display="flex" gap={2} color="text.secondary">
          <Typography variant="body2">
            Proposed: {new Date(bill.proposedDate).toLocaleDateString()}
          </Typography>
          <Typography variant="body2">
            Last Updated: {new Date(bill.lastUpdated).toLocaleDateString()}
          </Typography>
        </Box>
      </Paper>

      {/* Comments Section */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Comments
        </Typography>

        <Box component="form" onSubmit={handleCommentSubmit} sx={{ mb: 4 }}>
          <TextField
            fullWidth
            multiline
            rows={3}
            placeholder="Add your comment..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            startIcon={<CommentIcon />}
          >
            Submit Comment
          </Button>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* Comments List */}
        <Grid container spacing={2}>
          {bill.comments.map((comment) => (
            <Grid item xs={12} key={comment.id}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Avatar src={comment.user.avatar} sx={{ mr: 2 }}>
                    {comment.user.name[0]}
                  </Avatar>
                  <Box>
                    <Typography variant="subtitle2">
                      {comment.user.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(comment.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body1">
                  {comment.content}
                </Typography>
                <Box display="flex" alignItems="center" mt={1}>
                  <Button
                    size="small"
                    startIcon={<ThumbUp />}
                    sx={{ mr: 1 }}
                  >
                    {comment.votes}
                  </Button>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </DashboardLayout>
  );
};

export default BillView; 