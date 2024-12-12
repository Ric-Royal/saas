import { describe, expect, it } from '@jest/globals';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import BillList from '../BillList';
import { BillStatus, BillType } from '@/types/enums';

describe('BillList', () => {
  it('renders empty state when no bills are provided', () => {
    render(<BillList bills={[]} />);
    expect(screen.getByText('No bills found matching your criteria')).toBeInTheDocument();
  });

  it('renders bills correctly', () => {
    const mockBills = [
      {
        id: 1,
        bill_number: 'HB123',
        title: 'Test Bill',
        description: 'A test bill for testing purposes',
        status: BillStatus.IN_COMMITTEE,
        bill_type: BillType.HOUSE_BILL,
        introduced_date: '2024-01-01T00:00:00Z',
        last_action_date: '2024-01-02T00:00:00Z',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z',
        versions: [],
        actions: [],
        votes: [],
      },
    ];

    render(<BillList bills={mockBills} />);
    
    expect(screen.getByText('HB123: Test Bill')).toBeInTheDocument();
    expect(screen.getByText('A test bill for testing purposes')).toBeInTheDocument();
    expect(screen.getByText('IN_COMMITTEE')).toBeInTheDocument();
    expect(screen.getByText('Type: HOUSE_BILL')).toBeInTheDocument();
  });
}); 