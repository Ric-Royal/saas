import { BillStatus, BillType } from './enums';

export interface BillVersion {
  id: number;
  version_number: number;
  version_text: string;
  changes?: Record<string, any>;
  created_at: string;
}

export interface BillAction {
  id: number;
  action_date: string;
  action_text: string;
  action_type: string;
  committee?: string;
  created_at: string;
}

export interface BillVote {
  id: number;
  vote_date: string;
  vote_type: string;
  yea_votes: number;
  nay_votes: number;
  abstain_votes: number;
  vote_result: string;
  vote_details?: Record<string, any>;
  created_at: string;
}

export interface Bill {
  id: number;
  bill_number: string;
  title: string;
  description: string;
  status: BillStatus;
  bill_type: BillType;
  introduced_date: string;
  last_action_date?: string;
  sponsors?: Record<string, any>;
  full_text_url?: string;
  summary?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
  versions: BillVersion[];
  actions: BillAction[];
  votes: BillVote[];
}

export interface BillFilters {
  status: string;
  billType: string;
  searchTerm: string;
  dateFrom: string;
  dateTo: string;
} 