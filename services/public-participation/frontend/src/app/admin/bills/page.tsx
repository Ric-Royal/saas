'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useAuth } from '@/contexts/AuthContext';
import axios from 'axios';
import { useRouter } from 'next/navigation';

interface Bill {
  id: number;
  title: string;
  description: string;
  status: string;
  pdf_url: string;
  created_at: string;
  updated_at: string;
}

interface BillFormData {
  title: string;
  description: string;
  status: string;
  pdf_url: string;
}

export default function AdminBillsPage() {
  const { user } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [editingBill, setEditingBill] = useState<Bill | null>(null);
  const [formData, setFormData] = useState<BillFormData>({
    title: '',
    description: '',
    status: 'draft',
    pdf_url: '',
  });
  const [error, setError] = useState<string | null>(null);

  // Redirect if not superuser
  if (user && !user.is_superuser) {
    router.push('/');
    return null;
  }

  // Fetch bills
  const { data: bills, isLoading } = useQuery<Bill[]>({
    queryKey: ['admin-bills'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/admin/bills');
      return response.data;
    },
  });

  // Create bill mutation
  const createBill = useMutation({
    mutationFn: async (data: BillFormData) => {
      const response = await axios.post('/api/v1/admin/bills', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-bills'] });
      handleClose();
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to create bill');
    },
  });

  // Update bill mutation
  const updateBill = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: BillFormData }) => {
      const response = await axios.put(`/api/v1/admin/bills/${id}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-bills'] });
      handleClose();
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to update bill');
    },
  });

  // Delete bill mutation
  const deleteBill = useMutation({
    mutationFn: async (id: number) => {
      await axios.delete(`/api/v1/admin/bills/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-bills'] });
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to delete bill');
    },
  });

  const handleOpen = (bill?: Bill) => {
    if (bill) {
      setEditingBill(bill);
      setFormData({
        title: bill.title,
        description: bill.description,
        status: bill.status,
        pdf_url: bill.pdf_url,
      });
    } else {
      setEditingBill(null);
      setFormData({
        title: '',
        description: '',
        status: 'draft',
        pdf_url: '',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingBill(null);
    setFormData({
      title: '',
      description: '',
      status: 'draft',
      pdf_url: '',
    });
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingBill) {
      updateBill.mutate({ id: editingBill.id, data: formData });
    } else {
      createBill.mutate(formData);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this bill?')) {
      deleteBill.mutate(id);
    }
  };

  if (isLoading) {
    return (
      <Container>
        <Typography>Loading...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Manage Bills
        </Typography>
        <Button variant="contained" color="primary" onClick={() => handleOpen()}>
          Create New Bill
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Updated</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bills?.map((bill) => (
              <TableRow key={bill.id}>
                <TableCell>{bill.title}</TableCell>
                <TableCell>{bill.status}</TableCell>
                <TableCell>{new Date(bill.created_at).toLocaleDateString()}</TableCell>
                <TableCell>{new Date(bill.updated_at).toLocaleDateString()}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(bill)} color="primary">
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(bill.id)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editingBill ? 'Edit Bill' : 'Create New Bill'}</DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Title"
              fullWidth
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
            <TextField
              margin="dense"
              label="Description"
              fullWidth
              multiline
              rows={4}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <FormControl fullWidth margin="dense">
              <InputLabel>Status</InputLabel>
              <Select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                label="Status"
                required
              >
                <MenuItem value="draft">Draft</MenuItem>
                <MenuItem value="published">Published</MenuItem>
                <MenuItem value="archived">Archived</MenuItem>
              </Select>
            </FormControl>
            <TextField
              margin="dense"
              label="PDF URL"
              fullWidth
              value={formData.pdf_url}
              onChange={(e) => setFormData({ ...formData, pdf_url: e.target.value })}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button type="submit" variant="contained" color="primary">
              {editingBill ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
} 