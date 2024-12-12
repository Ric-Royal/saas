import { useState, useRef, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Divider,
  Card,
  CardContent,
  Alert,
  IconButton,
} from '@mui/material';
import { useAuth } from '@/contexts/AuthContext';
import axios from 'axios';
import { useParams } from 'next/navigation';
import { ForceGraph2D } from 'react-force-graph';
import { ZoomInIcon, ZoomOutIcon } from '@mui/icons-material';

interface Bill {
  id: number;
  title: string;
  description: string;
  status: string;
  pdf_url: string;
  created_at: string;
  comments: Comment[];
}

interface Comment {
  id: number;
  text: string;
  user_id: number;
  created_at: string;
  user: {
    full_name: string;
  };
}

interface GraphData {
  nodes: Array<{
    id: string;
    label: string;
    group?: string;
    size?: number;
  }>;
  links: Array<{
    source: string;
    target: string;
    label?: string;
    value?: number;
  }>;
}

export default function BillDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [newComment, setNewComment] = useState('');
  const [error, setError] = useState('');
  const [graphConfig, setGraphConfig] = useState({
    nodeSize: 8,
    linkWidth: 2,
    highlightedNode: null as string | null,
    zoomLevel: 1,
  });
  const graphRef = useRef<any>();
  const queryClient = useQueryClient();

  const { data: bill, isLoading: isBillLoading } = useQuery<Bill>(
    ['bill', id],
    async () => {
      const response = await axios.get(`/api/v1/bills/${id}`);
      return response.data;
    }
  );

  const { data: graphData } = useQuery<GraphData>(
    ['bill-graph', id],
    async () => {
      const response = await axios.get(`/api/v1/bills/${id}/knowledge-graph`);
      return response.data;
    }
  );

  const createComment = useMutation(
    async () => {
      await axios.post('/api/v1/comments', {
        text: newComment,
        bill_id: id,
      });
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['bill', id]);
        setNewComment('');
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to post comment');
      },
    }
  );

  const handleNodeClick = useCallback((node: any) => {
    setGraphConfig(prev => ({
      ...prev,
      highlightedNode: node.id === prev.highlightedNode ? null : node.id
    }));
  }, []);

  const handleZoom = (delta: number) => {
    setGraphConfig(prev => ({
      ...prev,
      zoomLevel: Math.max(0.1, Math.min(2, prev.zoomLevel + delta))
    }));
    if (graphRef.current) {
      graphRef.current.zoom(graphConfig.zoomLevel);
    }
  };

  if (isBillLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (!bill) {
    return <Typography>Bill not found</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {bill.title}
        </Typography>
        <Typography color="textSecondary" gutterBottom>
          Status: {bill.status}
        </Typography>
        <Typography paragraph>{bill.description}</Typography>
        {bill.pdf_url && (
          <Button
            variant="outlined"
            href={bill.pdf_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            View PDF
          </Button>
        )}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Knowledge Graph
        </Typography>
        <Box sx={{ position: 'relative', height: '500px', border: '1px solid #eee' }}>
          <Box sx={{ position: 'absolute', right: 16, top: 16, zIndex: 1 }}>
            <IconButton onClick={() => handleZoom(0.1)} size="small">
              <ZoomInIcon />
            </IconButton>
            <IconButton onClick={() => handleZoom(-0.1)} size="small">
              <ZoomOutIcon />
            </IconButton>
          </Box>
          {graphData && (
            <ForceGraph2D
              ref={graphRef}
              graphData={graphData}
              nodeLabel="label"
              linkLabel="label"
              nodeColor={node => 
                graphConfig.highlightedNode === node.id
                  ? '#f50057'
                  : node.group === 'bill'
                  ? '#1976d2'
                  : '#4caf50'
              }
              nodeSize={node => 
                graphConfig.highlightedNode === node.id
                  ? graphConfig.nodeSize * 1.5
                  : graphConfig.nodeSize
              }
              linkWidth={link => 
                (link.source as any).id === graphConfig.highlightedNode ||
                (link.target as any).id === graphConfig.highlightedNode
                  ? graphConfig.linkWidth * 2
                  : graphConfig.linkWidth
              }
              onNodeClick={handleNodeClick}
              linkDirectionalParticles={4}
              linkDirectionalParticleSpeed={d => d.value * 0.001}
              d3Force={('charge' as any, null)}
              d3VelocityDecay={0.3}
              cooldownTime={2000}
              nodeCanvasObject={(node, ctx, globalScale) => {
                const label = node.label as string;
                const fontSize = 12/globalScale;
                ctx.font = `${fontSize}px Sans-Serif`;
                ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.fillRect(
                  node.x! - ctx.measureText(label).width/2 - 2,
                  node.y! - fontSize/2 - 2,
                  ctx.measureText(label).width + 4,
                  fontSize + 4
                );
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#000';
                ctx.fillText(label, node.x!, node.y!);
              }}
            />
          )}
        </Box>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Comments
        </Typography>
        
        {user && (
          <Box sx={{ mb: 3 }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <TextField
              fullWidth
              multiline
              rows={3}
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Add a comment..."
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              onClick={() => createComment.mutate()}
              disabled={!newComment.trim()}
            >
              Post Comment
            </Button>
          </Box>
        )}

        <Divider sx={{ my: 3 }} />

        {bill.comments?.map((comment) => (
          <Card key={comment.id} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="body1">{comment.text}</Typography>
              <Typography variant="caption" color="textSecondary" display="block">
                By {comment.user.full_name} on{' '}
                {new Date(comment.created_at).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Paper>
    </Container>
  );
} 