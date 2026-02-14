import { Router, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import { getDb } from "../database";

const router = Router();

router.get("/group/:groupId", (req: Request, res: Response) => {
  const db = getDb();
  const { groupId } = req.params;

  const expenses = db.prepare(`
    SELECT e.*, u.name as paid_by_name
    FROM expenses e
    JOIN users u ON e.paid_by = u.id
    WHERE e.group_id = ?
    ORDER BY e.created_at DESC
  `).all(groupId);

  const expensesWithSplits = (expenses as Array<{ id: string }>).map((expense) => {
    const splits = db.prepare(`
      SELECT es.*, u.name as user_name
      FROM expense_splits es
      JOIN users u ON es.user_id = u.id
      WHERE es.expense_id = ?
    `).all(expense.id);
    return { ...expense, splits };
  });

  res.json(expensesWithSplits);
});

router.post("/", (req: Request, res: Response) => {
  const db = getDb();
  const { group_id, description, amount, paid_by, splits } = req.body;

  if (!group_id || !description || !amount || !paid_by) {
    res.status(400).json({ error: "group_id, description, amount, and paid_by are required" });
    return;
  }

  if (amount <= 0) {
    res.status(400).json({ error: "Amount must be positive" });
    return;
  }

  // Verify group exists
  const group = db.prepare("SELECT id FROM groups WHERE id = ?").get(group_id);
  if (!group) {
    res.status(404).json({ error: "Group not found" });
    return;
  }

  // Verify payer is a member
  const payerMember = db.prepare(
    "SELECT user_id FROM group_members WHERE group_id = ? AND user_id = ?"
  ).get(group_id, paid_by);
  if (!payerMember) {
    res.status(400).json({ error: "Payer must be a group member" });
    return;
  }

  const expenseId = uuidv4();

  const insertExpense = db.prepare(
    "INSERT INTO expenses (id, group_id, description, amount, paid_by) VALUES (?, ?, ?, ?, ?)"
  );
  const insertSplit = db.prepare(
    "INSERT INTO expense_splits (id, expense_id, user_id, amount) VALUES (?, ?, ?, ?)"
  );

  const transaction = db.transaction(() => {
    insertExpense.run(expenseId, group_id, description, amount, paid_by);

    if (splits && Array.isArray(splits) && splits.length > 0) {
      // Custom splits
      const totalSplit = splits.reduce(
        (sum: number, s: { amount: number }) => sum + s.amount,
        0
      );
      if (Math.abs(totalSplit - amount) > 0.01) {
        throw new Error("Split amounts must equal the total expense amount");
      }
      for (const split of splits) {
        insertSplit.run(uuidv4(), expenseId, split.user_id, split.amount);
      }
    } else {
      // Equal split among all group members
      const members = db.prepare(
        "SELECT user_id FROM group_members WHERE group_id = ?"
      ).all(group_id) as Array<{ user_id: string }>;

      const splitAmount = Math.round((amount / members.length) * 100) / 100;
      const remainder = Math.round((amount - splitAmount * members.length) * 100) / 100;

      members.forEach((member, index) => {
        const memberSplit = index === 0 ? splitAmount + remainder : splitAmount;
        insertSplit.run(uuidv4(), expenseId, member.user_id, memberSplit);
      });
    }
  });

  try {
    transaction();
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Failed to create expense";
    res.status(400).json({ error: message });
    return;
  }

  const expense = db.prepare("SELECT * FROM expenses WHERE id = ?").get(expenseId) as Record<string, unknown>;
  const expenseSplits = db.prepare("SELECT * FROM expense_splits WHERE expense_id = ?").all(
    expenseId
  );

  res.status(201).json({ ...expense, splits: expenseSplits });
});

router.delete("/:id", (req: Request, res: Response) => {
  const db = getDb();
  const result = db.prepare("DELETE FROM expenses WHERE id = ?").run(req.params.id);
  if (result.changes === 0) {
    res.status(404).json({ error: "Expense not found" });
    return;
  }
  res.json({ message: "Expense deleted" });
});

export default router;
