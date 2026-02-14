import React, { useState, useEffect, useCallback } from "react";
import { Group, Expense, GroupBalances, User } from "../types";
import {
  getGroup,
  getGroupExpenses,
  getGroupBalances,
  createExpense,
  deleteExpense,
  createSettlement,
} from "../api";

interface Props {
  groupId: string;
  users: User[];
  onBack: () => void;
}

export default function GroupDetail({ groupId, users, onBack }: Props) {
  const [group, setGroup] = useState<Group | null>(null);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [balances, setBalances] = useState<GroupBalances | null>(null);
  const [tab, setTab] = useState<"expenses" | "balances" | "settle">("expenses");
  const [error, setError] = useState("");

  // Add expense form
  const [expDesc, setExpDesc] = useState("");
  const [expAmount, setExpAmount] = useState("");
  const [expPaidBy, setExpPaidBy] = useState("");
  const [addingExpense, setAddingExpense] = useState(false);

  // Settle form
  const [settlePaidBy, setSettlePaidBy] = useState("");
  const [settlePaidTo, setSettlePaidTo] = useState("");
  const [settleAmount, setSettleAmount] = useState("");
  const [settling, setSettling] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [g, e, b] = await Promise.all([
        getGroup(groupId),
        getGroupExpenses(groupId),
        getGroupBalances(groupId),
      ]);
      setGroup(g);
      setExpenses(e);
      setBalances(b);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load group");
    }
  }, [groupId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAddExpense = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!expPaidBy) return;
    setAddingExpense(true);
    setError("");
    try {
      await createExpense({
        group_id: groupId,
        description: expDesc.trim(),
        amount: parseFloat(expAmount),
        paid_by: expPaidBy,
      });
      setExpDesc("");
      setExpAmount("");
      setExpPaidBy("");
      await loadData();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to add expense");
    } finally {
      setAddingExpense(false);
    }
  };

  const handleDeleteExpense = async (id: string) => {
    try {
      await deleteExpense(id);
      await loadData();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to delete expense");
    }
  };

  const handleSettle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settlePaidBy || !settlePaidTo) return;
    setSettling(true);
    setError("");
    try {
      await createSettlement({
        group_id: groupId,
        paid_by: settlePaidBy,
        paid_to: settlePaidTo,
        amount: parseFloat(settleAmount),
      });
      setSettlePaidBy("");
      setSettlePaidTo("");
      setSettleAmount("");
      await loadData();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to settle");
    } finally {
      setSettling(false);
    }
  };

  if (!group) return <div className="loading">Loading...</div>;

  const members = group.members || [];

  return (
    <div className="group-detail">
      <button className="back-btn" onClick={onBack}>
        &larr; Back to Groups
      </button>
      <h2>{group.name}</h2>
      {group.description && <p className="group-desc">{group.description}</p>}
      <p className="member-info">
        Members: {members.map((m) => m.name).join(", ") || "None"}
      </p>

      {error && <p className="error">{error}</p>}

      <div className="tabs">
        <button
          className={tab === "expenses" ? "tab active" : "tab"}
          onClick={() => setTab("expenses")}
        >
          Expenses
        </button>
        <button
          className={tab === "balances" ? "tab active" : "tab"}
          onClick={() => setTab("balances")}
        >
          Balances
        </button>
        <button
          className={tab === "settle" ? "tab active" : "tab"}
          onClick={() => setTab("settle")}
        >
          Settle Up
        </button>
      </div>

      {tab === "expenses" && (
        <div>
          <form className="inline-form" onSubmit={handleAddExpense}>
            <input
              type="text"
              placeholder="Description"
              value={expDesc}
              onChange={(e) => setExpDesc(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Amount"
              step="0.01"
              min="0.01"
              value={expAmount}
              onChange={(e) => setExpAmount(e.target.value)}
              required
            />
            <select
              value={expPaidBy}
              onChange={(e) => setExpPaidBy(e.target.value)}
              required
            >
              <option value="">Paid by</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
            <button type="submit" disabled={addingExpense}>
              {addingExpense ? "Adding..." : "Add Expense"}
            </button>
          </form>

          <div className="expense-list">
            {expenses.length === 0 ? (
              <p className="empty">No expenses yet</p>
            ) : (
              expenses.map((exp) => (
                <div key={exp.id} className="expense-item">
                  <div className="expense-main">
                    <strong>{exp.description}</strong>
                    <span className="amount">${exp.amount.toFixed(2)}</span>
                  </div>
                  <div className="expense-meta">
                    <span>
                      Paid by <strong>{exp.paid_by_name}</strong>
                    </span>
                    <span className="date">
                      {new Date(exp.created_at).toLocaleDateString()}
                    </span>
                    <button
                      className="delete-btn"
                      onClick={() => handleDeleteExpense(exp.id)}
                    >
                      Delete
                    </button>
                  </div>
                  {exp.splits && exp.splits.length > 0 && (
                    <div className="splits">
                      {exp.splits.map((s) => (
                        <span key={s.id} className="split-chip">
                          {s.user_name || users.find((u) => u.id === s.user_id)?.name || "Unknown"}:{" "}
                          ${s.amount.toFixed(2)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {tab === "balances" && balances && (
        <div>
          <h3>Member Balances</h3>
          <div className="balance-list">
            {balances.balances.map((b) => (
              <div
                key={b.userId}
                className={`balance-item ${b.balance > 0 ? "positive" : b.balance < 0 ? "negative" : ""}`}
              >
                <span>{b.name}</span>
                <span className="balance-amount">
                  {b.balance > 0 ? "+" : ""}
                  ${b.balance.toFixed(2)}
                </span>
              </div>
            ))}
          </div>

          {balances.simplifiedDebts.length > 0 && (
            <>
              <h3>Simplified Debts</h3>
              <div className="debt-list">
                {balances.simplifiedDebts.map((d, i) => (
                  <div key={i} className="debt-item">
                    <strong>{d.fromName}</strong> owes <strong>{d.toName}</strong>{" "}
                    <span className="amount">${d.amount.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {tab === "settle" && (
        <div>
          <h3>Record Settlement</h3>
          <form className="inline-form" onSubmit={handleSettle}>
            <select
              value={settlePaidBy}
              onChange={(e) => setSettlePaidBy(e.target.value)}
              required
            >
              <option value="">From</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
            <span className="arrow">→</span>
            <select
              value={settlePaidTo}
              onChange={(e) => setSettlePaidTo(e.target.value)}
              required
            >
              <option value="">To</option>
              {members
                .filter((m) => m.id !== settlePaidBy)
                .map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name}
                  </option>
                ))}
            </select>
            <input
              type="number"
              placeholder="Amount"
              step="0.01"
              min="0.01"
              value={settleAmount}
              onChange={(e) => setSettleAmount(e.target.value)}
              required
            />
            <button type="submit" disabled={settling}>
              {settling ? "Settling..." : "Settle"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
