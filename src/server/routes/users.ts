import { Router, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import { getDb } from "../database";

const router = Router();

router.get("/", (_req: Request, res: Response) => {
  const db = getDb();
  const users = db.prepare("SELECT * FROM users ORDER BY name").all();
  res.json(users);
});

router.get("/:id", (req: Request, res: Response) => {
  const db = getDb();
  const user = db.prepare("SELECT * FROM users WHERE id = ?").get(req.params.id);
  if (!user) {
    res.status(404).json({ error: "User not found" });
    return;
  }
  res.json(user);
});

router.post("/", (req: Request, res: Response) => {
  const db = getDb();
  const { name, email } = req.body;

  if (!name || !email) {
    res.status(400).json({ error: "Name and email are required" });
    return;
  }

  const existing = db.prepare("SELECT id FROM users WHERE email = ?").get(email);
  if (existing) {
    res.status(409).json({ error: "Email already exists" });
    return;
  }

  const id = uuidv4();
  db.prepare("INSERT INTO users (id, name, email) VALUES (?, ?, ?)").run(id, name, email);

  const user = db.prepare("SELECT * FROM users WHERE id = ?").get(id);
  res.status(201).json(user);
});

router.get("/:id/balances", (req: Request, res: Response) => {
  const db = getDb();
  const userId = req.params.id;

  const user = db.prepare("SELECT * FROM users WHERE id = ?").get(userId);
  if (!user) {
    res.status(404).json({ error: "User not found" });
    return;
  }

  // Calculate what this user owes others (from expense splits where someone else paid)
  const owes = db.prepare(`
    SELECT u.id, u.name, SUM(es.amount) as amount
    FROM expense_splits es
    JOIN expenses e ON es.expense_id = e.id
    JOIN users u ON e.paid_by = u.id
    WHERE es.user_id = ? AND e.paid_by != ?
    GROUP BY u.id, u.name
  `).all(userId, userId) as Array<{ id: string; name: string; amount: number }>;

  // Calculate what others owe this user (from expenses this user paid)
  const owed = db.prepare(`
    SELECT u.id, u.name, SUM(es.amount) as amount
    FROM expense_splits es
    JOIN expenses e ON es.expense_id = e.id
    JOIN users u ON es.user_id = u.id
    WHERE e.paid_by = ? AND es.user_id != ?
    GROUP BY u.id, u.name
  `).all(userId, userId) as Array<{ id: string; name: string; amount: number }>;

  // Factor in settlements
  const settlementsOut = db.prepare(`
    SELECT paid_to as id, SUM(amount) as amount
    FROM settlements
    WHERE paid_by = ?
    GROUP BY paid_to
  `).all(userId) as Array<{ id: string; amount: number }>;

  const settlementsIn = db.prepare(`
    SELECT paid_by as id, SUM(amount) as amount
    FROM settlements
    WHERE paid_to = ?
    GROUP BY paid_by
  `).all(userId) as Array<{ id: string; amount: number }>;

  // Net balances per person
  const balanceMap = new Map<string, { name: string; amount: number }>();

  for (const entry of owed) {
    balanceMap.set(entry.id, { name: entry.name, amount: entry.amount });
  }

  for (const entry of owes) {
    const current = balanceMap.get(entry.id) || { name: entry.name, amount: 0 };
    current.amount -= entry.amount;
    balanceMap.set(entry.id, current);
  }

  for (const entry of settlementsOut) {
    const current = balanceMap.get(entry.id);
    if (current) {
      current.amount -= entry.amount;
    }
  }

  for (const entry of settlementsIn) {
    const current = balanceMap.get(entry.id);
    if (current) {
      current.amount += entry.amount;
    }
  }

  const balances = Array.from(balanceMap.entries()).map(([id, data]) => ({
    userId: id,
    name: data.name,
    amount: Math.round(data.amount * 100) / 100,
  })).filter(b => Math.abs(b.amount) > 0.01);

  const totalBalance = balances.reduce((sum, b) => sum + b.amount, 0);

  res.json({
    userId,
    balances,
    totalBalance: Math.round(totalBalance * 100) / 100,
  });
});

export default router;
