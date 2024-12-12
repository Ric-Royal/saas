import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, CircularProgress, Box } from '@mui/material';
import { CheckCircle, Error as ErrorIcon } from '@mui/icons-material';

interface ServiceHealth {
  service: string;
  status: 'healthy' | 'unhealthy';
  latency: number;
  lastChecked: string;
}

interface HealthResponse {
  gateway: {
    status: string;
    timestamp: string;
  };
  services: ServiceHealth[];
}

class FetchError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'FetchError';
  }
}

const ServiceHealthStatus: React.FC = () => {
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealthStatus = async () => {
    try {
      const response = await fetch('/api/gateway/health');
      if (!response.ok) throw new FetchError('Failed to fetch health status');
      const data = await response.json();
      setHealthData(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealthStatus();
    const interval = setInterval(fetchHealthStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Paper sx={{ p: 2, bgcolor: 'error.light', color: 'error.contrastText' }}>
        <Typography variant="h6">Error: {error}</Typography>
      </Paper>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Service Health Status
          </Typography>
          <Grid container spacing={2}>
            {healthData?.services.map((service) => (
              <Grid item xs={12} sm={6} md={4} key={service.service}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    alignItems: 'center',
                    bgcolor: service.status === 'healthy' ? 'success.light' : 'error.light',
                  }}
                >
                  {service.status === 'healthy' ? (
                    <CheckCircle color="success" sx={{ mr: 1 }} />
                  ) : (
                    <ErrorIcon color="error" sx={{ mr: 1 }} />
                  )}
                  <Box>
                    <Typography variant="subtitle1">{service.service}</Typography>
                    <Typography variant="body2">
                      Latency: {service.latency}ms
                    </Typography>
                    <Typography variant="caption">
                      Last checked: {new Date(service.lastChecked).toLocaleString()}
                    </Typography>
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default ServiceHealthStatus; 