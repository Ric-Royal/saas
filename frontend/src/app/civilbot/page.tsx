'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent
} from '@mui/material';
import { Send as SendIcon, Analytics as AnalyticsIcon } from '@mui/icons-material';
import DashboardLayout from '../../components/layout/DashboardLayout';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

interface Analytics {
  totalConversations: number;
  averageResponseTime: number;
  topIntents: Array<{ intent: string; count: number }>;
  userSatisfaction: number;
}

const CivilBotPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    // Fetch analytics data
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/civilbot/analytics');
        const data = await response.json();
        setAnalytics(data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      }
    };

    fetchAnalytics();
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, newMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/civilbot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      const botResponse: Message = {
        id: Date.now().toString(),
        content: data.response,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <Grid container spacing={3}>
        {/* Chat Interface */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '70vh', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              CivilBot Chat
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {/* Messages Area */}
            <Box sx={{ flexGrow: 1, overflow: 'auto', mb: 2 }}>
              <List>
                {messages.map((message) => (
                  <ListItem
                    key={message.id}
                    sx={{
                      justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                    }}
                  >
                    <Paper
                      sx={{
                        p: 2,
                        maxWidth: '70%',
                        bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                      }}
                    >
                      <ListItemText
                        primary={message.content}
                        secondary={new Date(message.timestamp).toLocaleTimeString()}
                      />
                    </Paper>
                  </ListItem>
                ))}
                {loading && (
                  <ListItem>
                    <CircularProgress size={20} />
                  </ListItem>
                )}
              </List>
            </Box>

            {/* Input Area */}
            <Box component="form" onSubmit={handleSendMessage}>
              <Grid container spacing={1}>
                <Grid item xs>
                  <TextField
                    fullWidth
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    variant="outlined"
                    disabled={loading}
                  />
                </Grid>
                <Grid item>
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={loading}
                    endIcon={<SendIcon />}
                  >
                    Send
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        </Grid>

        {/* Analytics Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <AnalyticsIcon sx={{ mr: 1 }} />
              Analytics
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {analytics ? (
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Total Conversations
                      </Typography>
                      <Typography variant="h4">
                        {analytics.totalConversations}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Average Response Time
                      </Typography>
                      <Typography variant="h4">
                        {analytics.averageResponseTime}ms
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        User Satisfaction
                      </Typography>
                      <Typography variant="h4">
                        {analytics.userSatisfaction}%
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Top Intents
                      </Typography>
                      <List dense>
                        {analytics.topIntents.map((intent) => (
                          <ListItem key={intent.intent}>
                            <ListItemText
                              primary={intent.intent}
                              secondary={`${intent.count} queries`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            ) : (
              <Box display="flex" justifyContent="center" p={3}>
                <CircularProgress />
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </DashboardLayout>
  );
};

export default CivilBotPage; 