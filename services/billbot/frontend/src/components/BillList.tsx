'use client';

import { Bill } from '@/types/bill';
import Link from 'next/link';
import { formatDate } from '@/lib/utils';
import { BillStatus } from '@/types/enums';

interface BillListProps {
  bills: Bill[];
}

const statusColors: Record<BillStatus, { bg: string; text: string }> = {
  [BillStatus.INTRODUCED]: { bg: 'bg-blue-100', text: 'text-blue-800' },
  [BillStatus.IN_COMMITTEE]: { bg: 'bg-yellow-100', text: 'text-yellow-800' },
  [BillStatus.PASSED_COMMITTEE]: { bg: 'bg-green-100', text: 'text-green-800' },
  [BillStatus.FLOOR_VOTE]: { bg: 'bg-purple-100', text: 'text-purple-800' },
  [BillStatus.PASSED]: { bg: 'bg-green-100', text: 'text-green-800' },
  [BillStatus.FAILED]: { bg: 'bg-red-100', text: 'text-red-800' },
  [BillStatus.SIGNED]: { bg: 'bg-green-100', text: 'text-green-800' },
  [BillStatus.VETOED]: { bg: 'bg-red-100', text: 'text-red-800' },
  [BillStatus.ENACTED]: { bg: 'bg-green-100', text: 'text-green-800' },
};

export default function BillList({ bills }: BillListProps) {
  if (!bills.length) {
    return (
      <div className="text-center py-8 text-gray-500">
        No bills found matching your criteria
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {bills.map((bill) => (
        <Link
          key={bill.id}
          href={`/bills/${bill.id}`}
          className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200"
        >
          <div className="p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-semibold mb-2">
                  {bill.bill_number}: {bill.title}
                </h2>
                <p className="text-gray-600 mb-4 line-clamp-2">
                  {bill.description}
                </p>
              </div>
              <div className={`px-3 py-1 rounded-full ${statusColors[bill.status].bg} ${statusColors[bill.status].text}`}>
                {bill.status}
              </div>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-500">
              <div className="flex space-x-4">
                <span>Type: {bill.bill_type}</span>
                <span>Introduced: {formatDate(bill.introduced_date)}</span>
                {bill.last_action_date && (
                  <span>Last Action: {formatDate(bill.last_action_date)}</span>
                )}
              </div>
              <div className="flex space-x-2">
                <span>{bill.versions.length} versions</span>
                <span>•</span>
                <span>{bill.actions.length} actions</span>
                <span>•</span>
                <span>{bill.votes.length} votes</span>
              </div>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
} 