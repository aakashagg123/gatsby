export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface Group {
  id: string;
  name: string;
  description: string | null;
  created_by: string;
  created_by_name: string;
  created_at: string;
  member_count?: number;
  members?: GroupMember[];
}

export interface GroupMember {
  id: string;
  name: string;
  email: string;
  joined_at: string;
}

export interface ExpenseSplit {
  id: string;
  expense_id: string;
  user_id: string;
  user_name?: string;
  amount: number;
}

export interface Expense {
  id: string;
  group_id: string;
  description: string;
  amount: number;
  paid_by: string;
  paid_by_name: string;
  created_at: string;
  splits: ExpenseSplit[];
}

export interface Settlement {
  id: string;
  group_id: string;
  paid_by: string;
  paid_to: string;
  paid_by_name: string;
  paid_to_name: string;
  amount: number;
  created_at: string;
}

export interface Balance {
  userId: string;
  name: string;
  balance: number;
}

export interface SimplifiedDebt {
  from: string;
  fromName: string;
  to: string;
  toName: string;
  amount: number;
}

export interface GroupBalances {
  balances: Balance[];
  simplifiedDebts: SimplifiedDebt[];
}
