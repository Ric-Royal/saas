'use client';

import { useEffect, useState } from 'react';
import { Bill } from '@/types/bill';
import { getBills } from '@/lib/api';
import BillList from '@/components/BillList';
import BillFilters from '@/components/BillFilters';
import { BillStatus, BillType } from '@/types/enums';

export default function DashboardPage() {
  const [bills, setBills] = useState<Bill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    billType: '',
    searchTerm: '',
    dateFrom: '',
    dateTo: '',
  });

  useEffect(() => {
    const fetchBills = async () => {
      try {
        const data = await getBills(filters);
        setBills(data);
      } catch (err) {
        setError('Failed to fetch bills');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchBills();
  }, [filters]);

  if (loading) return <div className="animate-pulse">Loading bills...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Legislative Bills</h1>
        <div className="flex gap-4">
          <button
            onClick={() => window.location.href = '/bills/subscriptions'}
            className="px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200"
          >
            My Subscriptions
          </button>
          <button
            onClick={() => window.location.href = '/bills/analytics'}
            className="px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200"
          >
            Analytics
          </button>
        </div>
      </div>

      <BillFilters
        filters={filters}
        onFilterChange={setFilters}
        statuses={Object.values(BillStatus)}
        types={Object.values(BillType)}
      />

      <BillList bills={bills} />
    </div>
  );
} 