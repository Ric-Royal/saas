'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Chip,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  TextField,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot
} from '@mui/lab';
import {
  Notifications,
  NotificationsOff,
  Comment as CommentIcon,
  Update as UpdateIcon,
  Assignment as AssignmentIcon
} from '@mui/icons-material';
import DashboardLayout from '../../../../components/layout/DashboardLayout';

interface BillDetail {
  id: string;
  title: string;
  description: string;
  status: string;
  category: string;
  progress: number;
  subscribers: number;
  isSubscribed: boolean;
  proposedDate: string;
  lastUpdated: string;
  timeline: Array<{
    id: string;
    date: string;
    title: string;
    description: string;
  }>;
  comments: Array<{
    id: string;
    user: {
      name: string;
      avatar: string;
    };
    content: string;
    timestamp: string;
  }>;
}

const BillDetailPage = () => {
  const params = useParams();
  const billId = params?.id as string;
  const [bill, setBill] = useState<BillDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [comment, setComment] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBillDetails = async () => {
      try {
        const response = await fetch(`/api/billbot/bills/${billId}`);
        if (!response.ok) throw new Error('Failed to fetch bill details');
        const data = await response.json();
        setBill(data);
      } catch (error) {
        setError('Error loading bill details');
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    if (billId) {
      fetchBillDetails();
    }
  }, [billId]);

  const handleSubscribe = async () => {
    try {
      const response = await fetch(`/api/billbot/bills/${billId}/subscribe`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Failed to update subscription');
      const data = await response.json();
      setBill(prev => prev ? { ...prev, isSubscribed: !prev.isSubscribed } : null);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment.trim()) return;

    try {
      const response = await fetch(`/api/billbot/bills/${billId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: comment })
      });

      if (!response.ok) throw new Error('Failed to post comment');
      const newComment = await response.json();
      
      setBill(prev => prev ? {
        ...prev,
        comments: [...prev.comments, newComment]
      } : null);
      
      setComment('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </DashboardLayout>
    );
  }

  if (error || !bill) {
    return (
      <DashboardLayout>
        <Alert severity="error">{error || 'Bill not found'}</Alert>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Grid container spacing={3}>
        {/* Bill Header */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="flex-start">
              <Box>
                <Typography variant="h4" gutterBottom>
                  {bill.title}
                </Typography>
                <Box display="flex" gap={1} mb={2}>
                  <Chip label={bill.category} color="primary" />
                  <Chip label={bill.status} color={bill.status === 'Active' ? 'success' : 'default'} />
                </Box>
              </Box>
              <Button
                variant="outlined"
                startIcon={bill.isSubscribed ? <NotificationsOff /> : <Notifications />}
                onClick={handleSubscribe}
              >
                {bill.isSubscribed ? 'Unsubscribe' : 'Subscribe'}
              </Button>
            </Box>
            <Typography variant="body1" paragraph>
              {bill.description}
            </Typography>
            <Box mt={2}>
              <Typography variant="subtitle2" gutterBottom>
                Progress
              </Typography>
              <LinearProgress
                variant="determinate"
                value={bill.progress}
                sx={{ height: 10, borderRadius: 5 }}
              />
              <Typography variant="caption" color="text.secondary">
                {bill.progress}% Complete
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Timeline */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Bill Timeline
            </Typography>
            <Timeline>
              {bill.timeline.map((event, index) => (
                <TimelineItem key={event.id}>
                  <TimelineSeparator>
                    <TimelineDot color="primary">
                      <UpdateIcon />
                    </TimelineDot>
                    {index < bill.timeline.length - 1 && <TimelineConnector />}
                  </TimelineSeparator>
                  <TimelineContent>
                    <Typography variant="subtitle2">
                      {event.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {new Date(event.date).toLocaleDateString()}
                    </Typography>
                    <Typography variant="body2">
                      {event.description}
                    </Typography>
                  </TimelineContent>
                </TimelineItem>
              ))}
            </Timeline>
          </Paper>
        </Grid>

        {/* Comments Section */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Comments
            </Typography>
            <Box component="form" onSubmit={handleCommentSubmit} sx={{ mb: 3 }}>
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
                disabled={!comment.trim()}
              >
                Post Comment
              </Button>
            </Box>
            <Divider sx={{ my: 2 }} />
            <List>
              {bill.comments.map((comment) => (
                <ListItem key={comment.id} alignItems="flex-start">
                  <ListItemAvatar>
                    <Avatar src={comment.user.avatar}>
                      {comment.user.name[0]}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={comment.user.name}
                    secondary={
                      <>
                        <Typography
                          component="span"
                          variant="body2"
                          color="text.primary"
                        >
                          {comment.content}
                        </Typography>
                        <br />
                        <Typography
                          component="span"
                          variant="caption"
                          color="text.secondary"
                        >
                          {new Date(comment.timestamp).toLocaleString()}
                        </Typography>
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </DashboardLayout>
  );
};

export default BillDetailPage; 