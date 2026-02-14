import { User, Group, Expense, Settlement, GroupBalances } from "../types";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:3001/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(error.error || "Request failed");
  }
  return res.json();
}

// Users
export const getUsers = () => request<User[]>("/users");
export const createUser = (name: string, email: string) =>
  request<User>("/users", {
    method: "POST",
    body: JSON.stringify({ name, email }),
  });

// Groups
export const getGroups = () => request<Group[]>("/groups");
export const getGroup = (id: string) => request<Group>("/groups/" + id);
export const createGroup = (
  name: string,
  description: string,
  created_by: string,
  member_ids: string[]
) =>
  request<Group>("/groups", {
    method: "POST",
    body: JSON.stringify({ name, description, created_by, member_ids }),
  });
export const addGroupMember = (groupId: string, userId: string) =>
  request("/groups/" + groupId + "/members", {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
export const getGroupBalances = (groupId: string) =>
  request<GroupBalances>("/groups/" + groupId + "/balances");

// Expenses
export const getGroupExpenses = (groupId: string) =>
  request<Expense[]>("/expenses/group/" + groupId);
export const createExpense = (data: {
  group_id: string;
  description: string;
  amount: number;
  paid_by: string;
  splits?: Array<{ user_id: string; amount: number }>;
}) =>
  request<Expense>("/expenses", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const deleteExpense = (id: string) =>
  request("/expenses/" + id, { method: "DELETE" });

// Settlements
export const getGroupSettlements = (groupId: string) =>
  request<Settlement[]>("/settlements/group/" + groupId);
export const createSettlement = (data: {
  group_id: string;
  paid_by: string;
  paid_to: string;
  amount: number;
}) =>
  request<Settlement>("/settlements", {
    method: "POST",
    body: JSON.stringify(data),
  });
