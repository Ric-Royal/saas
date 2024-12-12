'use client';

import { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  ChartOptions,
} from 'chart.js/auto';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { formatDate } from '@/lib/utils';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface AnalyticsData {
  summary: {
    total_bills: number;
    by_status: Record<string, number>;
    by_type: Record<string, number>;
  };
  trends: {
    bills_introduced: Record<string, number>;
    bill_actions: Record<string, number>;
  };
  popular_topics: Array<{ topic: string; count: number }>;
  success_rate: {
    total_bills: number;
    passed_bills: number;
    failed_bills: number;
    pending_bills: number;
    success_rate: number;
  };
}

export default function AnalyticsDashboard() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('30'); // days

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [summaryRes, trendsRes, topicsRes, successRateRes] = await Promise.all([
          fetch('/api/v1/analytics/summary'),
          fetch(`/api/v1/analytics/trends?days=${timeRange}`),
          fetch('/api/v1/analytics/popular-topics?limit=10'),
          fetch(`/api/v1/analytics/success-rate?days=${timeRange}`),
        ]);

        const [summary, trends, topics, successRate] = await Promise.all([
          summaryRes.json(),
          trendsRes.json(),
          topicsRes.json(),
          successRateRes.json(),
        ]);

        setData({ summary, trends, popular_topics: topics, success_rate: successRate });
      } catch (err) {
        setError('Failed to fetch analytics data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [timeRange]);

  if (loading) return <div className="animate-pulse">Loading analytics...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!data) return null;

  const billTrendsData = {
    labels: Object.keys(data.trends.bills_introduced).map(date => formatDate(date)),
    datasets: [
      {
        label: 'Bills Introduced',
        data: Object.values(data.trends.bills_introduced),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'Bill Actions',
        data: Object.values(data.trends.bill_actions),
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.1,
      },
    ],
  };

  const statusDistributionData = {
    labels: Object.keys(data.summary.by_status),
    datasets: [{
      data: Object.values(data.summary.by_status),
      backgroundColor: [
        'rgb(54, 162, 235)',
        'rgb(255, 99, 132)',
        'rgb(255, 206, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
      ],
    }],
  };

  const popularTopicsData = {
    labels: data.popular_topics.map(topic => topic.topic),
    datasets: [{
      label: 'Number of Bills',
      data: data.popular_topics.map(topic => topic.count),
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
    }],
  };

  const lineChartOptions: ChartOptions<'line'> = {
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        type: 'linear'
      }
    }
  };

  const barChartOptions: ChartOptions<'bar'> = {
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        type: 'linear'
      }
    }
  };

  const pieChartOptions: ChartOptions<'pie'> = {
    maintainAspectRatio: false
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
          className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="365">Last year</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Bill Success Rate</h2>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {data.success_rate.success_rate.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-500">Success Rate</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {data.success_rate.total_bills}
              </div>
              <div className="text-sm text-gray-500">Total Bills</div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-xl font-semibold text-green-600">
                {data.success_rate.passed_bills}
              </div>
              <div className="text-sm text-gray-500">Passed</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-semibold text-red-600">
                {data.success_rate.failed_bills}
              </div>
              <div className="text-sm text-gray-500">Failed</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-semibold text-yellow-600">
                {data.success_rate.pending_bills}
              </div>
              <div className="text-sm text-gray-500">Pending</div>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Status Distribution</h2>
          <div className="h-64">
            <Pie data={statusDistributionData} options={pieChartOptions} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Bill Activity Trends</h2>
          <div className="h-80">
            <Line
              data={billTrendsData}
              options={lineChartOptions}
            />
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Popular Topics</h2>
        <div className="h-80">
          <Bar
            data={popularTopicsData}
            options={barChartOptions}
          />
        </div>
      </div>
    </div>
  );
} 