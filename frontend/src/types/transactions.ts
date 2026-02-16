import type { Status } from "./status";

export interface TransactionDetail {
  transaction_id: number;
  contractor_from: string;
  contractor_to: string;
  amount: number; // Decimal from backend serialized as number
  transaction_type: {
    transaction_type_id: number;
    code: string;
    display_name: string;
  };
  status: Status;
  created_at: string; // ISO datetime
  updated_at: string;
}

export interface TransactionListItem {
  transaction_id: number;
  contractor_from: string;
  contractor_to: string;
  amount: number;
  transaction_type: string;
  status: Status;
  created_at: string;
}

export interface TransactionListResponse {
  items: TransactionListItem[];
}

export interface TransactionCreateRequest {
  contractor_from_id: number;
  contractor_to_id: number;
  amount: number;
  status_id: number;
  transaction_type_id: number;
}

export interface TransactionUpdateRequest {
  status_id?: number;
}
