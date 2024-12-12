'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  WbSunny,
  Notifications,
  Search as SearchIcon,
  Add as AddIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
  Timeline as TimelineIcon,
  Analytics as AnalyticsIcon
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';
import { AgriInsightsApi, PricePrediction, HistoricalAnalysis } from '../../lib/api/agriInsightsApi';
import DashboardLayout from '../../components/layout/DashboardLayout';

interface MarketData {
  commodity: string;
  price: number;
  change: number;
  volume: number;
  timestamp: string;
}

interface WeatherData {
  location: string;
  temperature: number;
  condition: string;
  humidity: number;
  rainfall: number;
  forecast: Array<{
    date: string;
    temperature: number;
    condition: string;
  }>;
}

interface Commodity {
  id: string;
  name: string;
  currentPrice: number;
  priceChange: number;
  isWatched: boolean;
  historicalData: Array<{
    date: string;
    price: number;
  }>;
}

interface Alert {
  id: string;
  type: string;
  message: string;
  timestamp: string;
  isRead: boolean;
}

const AgriInsightsPage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [commodities, setCommodities] = useState<Commodity[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [predictions, setPredictions] = useState<PricePrediction[]>([]);
  const [analysis, setAnalysis] = useState<HistoricalAnalysis | null>(null);
  const [showPredictionDialog, setShowPredictionDialog] = useState(false);
  const [showAnalysisDialog, setShowAnalysisDialog] = useState(false);
  const [selectedCommodityId, setSelectedCommodityId] = useState<number | null>(null);
  const [predictionHorizon, setPredictionHorizon] = useState(7);
  const [analysisType, setAnalysisType] = useState<'trend' | 'seasonality' | 'volatility' | 'all'>('all');
  
  const api = new AgriInsightsApi();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [marketResponse, weatherResponse, commoditiesResponse, alertsResponse] = await Promise.all([
          fetch('/api/agri-insights/market-data'),
          fetch('/api/agri-insights/weather'),
          fetch('/api/agri-insights/commodities'),
          fetch('/api/agri-insights/alerts')
        ]);

        const marketData = await marketResponse.json();
        const weatherData = await weatherResponse.json();
        const commoditiesData = await commoditiesResponse.json();
        const alertsData = await alertsResponse.json();

        setMarketData(marketData);
        setWeatherData(weatherData);
        setCommodities(commoditiesData);
        setAlerts(alertsData);
      } catch (error) {
        setError('Failed to fetch data');
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const toggleWatchlist = async (commodityId: string) => {
    try {
      const response = await fetch(`/api/agri-insights/watchlist/${commodityId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Failed to update watchlist');
      
      setCommodities(prev => prev.map(commodity => 
        commodity.id === commodityId 
          ? { ...commodity, isWatched: !commodity.isWatched }
          : commodity
      ));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const filteredCommodities = commodities.filter(commodity =>
    commodity.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleGetPredictions = async () => {
    if (!selectedCommodityId) return;
    try {
      const predictions = await api.getPricePredictions({
        commodity_id: selectedCommodityId,
        prediction_horizon: predictionHorizon,
        include_confidence: true
      });
      setPredictions(predictions);
      setShowPredictionDialog(true);
    } catch (error) {
      console.error('Error getting predictions:', error);
      setError('Failed to get predictions');
    }
  };

  const handleGetAnalysis = async () => {
    if (!selectedCommodityId) return;
    try {
      const analysis = await api.analyzeHistoricalData({
        commodity_id: selectedCommodityId,
        start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        end_date: new Date().toISOString().split('T')[0],
        analysis_type: analysisType
      });
      setAnalysis(analysis);
      setShowAnalysisDialog(true);
    } catch (error) {
      console.error('Error getting analysis:', error);
      setError('Failed to get analysis');
    }
  };

  const renderPredictionDialog = () => (
    <Dialog open={showPredictionDialog} onClose={() => setShowPredictionDialog(false)} maxWidth="md" fullWidth>
      <DialogTitle>Price Predictions</DialogTitle>
      <DialogContent>
        <Box height={400}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={predictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="prediction_date" />
              <YAxis />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="predicted_price"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Box>
        <List>
          {predictions.map((pred) => (
            <ListItem key={pred.prediction_date}>
              <ListItemText
                primary={`Date: ${new Date(pred.prediction_date).toLocaleDateString()}`}
                secondary={`Predicted Price: $${pred.predicted_price.toFixed(2)} (Confidence: ${(pred.confidence_score * 100).toFixed(1)}%)`}
              />
            </ListItem>
          ))}
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowPredictionDialog(false)}>Close</Button>
      </DialogActions>
    </Dialog>
  );

  const renderAnalysisDialog = () => (
    <Dialog open={showAnalysisDialog} onClose={() => setShowAnalysisDialog(false)} maxWidth="md" fullWidth>
      <DialogTitle>Historical Analysis</DialogTitle>
      <DialogContent>
        {analysis?.trend && (
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6">Trend Analysis</Typography>
              <Typography>
                Direction: {analysis.trend.direction.toUpperCase()}
                <TrendingUp
                  sx={{
                    color: analysis.trend.direction === 'up' ? 'success.main' : 'error.main',
                    ml: 1
                  }}
                />
              </Typography>
              <Typography>Strength: {(analysis.trend.strength * 100).toFixed(1)}%</Typography>
            </CardContent>
          </Card>
        )}
        {analysis?.seasonality && (
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6">Seasonality Analysis</Typography>
              <Box height={200}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={analysis.seasonality.pattern.map((value, index) => ({ day: index + 1, value }))}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="value" stroke="#82ca9d" />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Typography>Pattern Strength: {(analysis.seasonality.strength * 100).toFixed(1)}%</Typography>
            </CardContent>
          </Card>
        )}
        {analysis?.volatility && (
          <Card>
            <CardContent>
              <Typography variant="h6">Volatility Analysis</Typography>
              <Typography>Current Volatility: {analysis.volatility.current.toFixed(3)}</Typography>
              <Typography>
                Trend: {analysis.volatility.trend.toUpperCase()}
                <TrendingUp
                  sx={{
                    color: analysis.volatility.trend === 'decreasing' ? 'success.main' : 'error.main',
                    ml: 1
                  }}
                />
              </Typography>
              <Typography>Historical Mean: {analysis.volatility.historical_mean.toFixed(3)}</Typography>
            </CardContent>
          </Card>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowAnalysisDialog(false)}>Close</Button>
      </DialogActions>
    </Dialog>
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

  if (error) {
    return (
      <DashboardLayout>
        <Alert severity="error">{error}</Alert>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Grid container spacing={3}>
        {/* Weather Card */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <WbSunny sx={{ mr: 1 }} /> Weather Insights
            </Typography>
            {weatherData && (
              <>
                <Typography variant="h3" gutterBottom>
                  {weatherData.temperature}°C
                </Typography>
                <Typography variant="subtitle1">
                  {weatherData.location}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Humidity: {weatherData.humidity}% | Rainfall: {weatherData.rainfall}mm
                </Typography>
                <Box mt={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Forecast
                  </Typography>
                  <Grid container spacing={1}>
                    {weatherData.forecast.map((day) => (
                      <Grid item xs={4} key={day.date}>
                        <Paper sx={{ p: 1, textAlign: 'center' }}>
                          <Typography variant="caption" display="block">
                            {new Date(day.date).toLocaleDateString(undefined, { weekday: 'short' })}
                          </Typography>
                          <Typography variant="h6">
                            {day.temperature}°C
                          </Typography>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              </>
            )}
          </Paper>
        </Grid>

        {/* Market Overview */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Market Overview
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={marketData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(timestamp) => new Date(timestamp).toLocaleDateString()}
                  />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="price" stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Commodities and Alerts Tabs */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
              <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab label="Commodities" />
                <Tab label="Alerts" />
              </Tabs>
            </Box>

            {activeTab === 0 && (
              <>
                <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <TextField
                    size="small"
                    placeholder="Search commodities..."
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
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => {/* Add commodity to watchlist */}}
                  >
                    Add to Watchlist
                  </Button>
                </Box>

                <List>
                  {filteredCommodities.map((commodity) => (
                    <ListItem key={commodity.id}>
                      <ListItemText
                        primary={commodity.name}
                        secondary={`Current Price: $${commodity.currentPrice}`}
                      />
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Chip
                          icon={commodity.priceChange >= 0 ? <TrendingUp /> : <TrendingDown />}
                          label={`${commodity.priceChange}%`}
                          color={commodity.priceChange >= 0 ? 'success' : 'error'}
                        />
                        <IconButton
                          onClick={() => toggleWatchlist(commodity.id)}
                          color={commodity.isWatched ? 'primary' : 'default'}
                        >
                          {commodity.isWatched ? <StarIcon /> : <StarBorderIcon />}
                        </IconButton>
                      </Box>
                    </ListItem>
                  ))}
                </List>
              </>
            )}

            {activeTab === 1 && (
              <List>
                {alerts.map((alert) => (
                  <ListItem key={alert.id}>
                    <ListItemText
                      primary={alert.message}
                      secondary={new Date(alert.timestamp).toLocaleString()}
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" onClick={() => {/* Mark as read */}}>
                        <Notifications color={alert.isRead ? 'disabled' : 'primary'} />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>

        {/* ML Controls */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Market Intelligence
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Commodity</InputLabel>
                  <Select
                    value={selectedCommodityId || ''}
                    onChange={(e) => setSelectedCommodityId(Number(e.target.value))}
                  >
                    {commodities.map((commodity) => (
                      <MenuItem key={commodity.id} value={commodity.id}>
                        {commodity.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  type="number"
                  label="Prediction Days"
                  value={predictionHorizon}
                  onChange={(e) => setPredictionHorizon(Number(e.target.value))}
                  InputProps={{ inputProps: { min: 1, max: 30 } }}
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Analysis Type</InputLabel>
                  <Select
                    value={analysisType}
                    onChange={(e) => setAnalysisType(e.target.value as typeof analysisType)}
                  >
                    <MenuItem value="all">All</MenuItem>
                    <MenuItem value="trend">Trend</MenuItem>
                    <MenuItem value="seasonality">Seasonality</MenuItem>
                    <MenuItem value="volatility">Volatility</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<TimelineIcon />}
                  onClick={handleGetPredictions}
                  disabled={!selectedCommodityId}
                >
                  Get Price Predictions
                </Button>
              </Grid>
              <Grid item xs={6}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<AnalyticsIcon />}
                  onClick={handleGetAnalysis}
                  disabled={!selectedCommodityId}
                >
                  Analyze Historical Data
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
      {renderPredictionDialog()}
      {renderAnalysisDialog()}
    </DashboardLayout>
  );
};

export default AgriInsightsPage; 