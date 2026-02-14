import { Router, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import { getDb } from "../database";

const router = Router();

router.get("/", (_req: Request, res: Response) => {
  const db = getDb();
  const groups = db.prepare(`
    SELECT g.*, u.name as created_by_name,
      (SELECT COUNT(*) FROM group_members gm WHERE gm.group_id = g.id) as member_count
    FROM groups g
    JOIN users u ON g.created_by = u.id
    ORDER BY g.created_at DESC
  `).all();
  res.json(groups);
});

router.get("/:id", (req: Request, res: Response) => {
  const db = getDb();
  const group = db.prepare(`
    SELECT g.*, u.name as created_by_name
    FROM groups g
    JOIN users u ON g.created_by = u.id
    WHERE g.id = ?
  `).get(req.params.id);

  if (!group) {
    res.status(404).json({ error: "Group not found" });
    return;
  }

  const members = db.prepare(`
    SELECT u.id, u.name, u.email, gm.joined_at
    FROM group_members gm
    JOIN users u ON gm.user_id = u.id
    WHERE gm.group_id = ?
    ORDER BY u.name
  `).all(req.params.id);

  res.json({ ...group, members });
});

router.post("/", (req: Request, res: Response) => {
  const db = getDb();
  const { name, description, created_by, member_ids } = req.body;

  if (!name || !created_by) {
    res.status(400).json({ error: "Name and created_by are required" });
    return;
  }

  const creator = db.prepare("SELECT id FROM users WHERE id = ?").get(created_by);
  if (!creator) {
    res.status(404).json({ error: "Creator user not found" });
    return;
  }

  const id = uuidv4();

  const insertGroup = db.prepare(
    "INSERT INTO groups (id, name, description, created_by) VALUES (?, ?, ?, ?)"
  );
  const insertMember = db.prepare(
    "INSERT OR IGNORE INTO group_members (group_id, user_id) VALUES (?, ?)"
  );

  const transaction = db.transaction(() => {
    insertGroup.run(id, name, description || null, created_by);
    insertMember.run(id, created_by);

    if (member_ids && Array.isArray(member_ids)) {
      for (const memberId of member_ids) {
        insertMember.run(id, memberId);
      }
    }
  });

  transaction();

  const group = db.prepare("SELECT * FROM groups WHERE id = ?").get(id);
  res.status(201).json(group);
});

router.post("/:id/members", (req: Request, res: Response) => {
  const db = getDb();
  const { user_id } = req.body;
  const groupId = req.params.id;

  if (!user_id) {
    res.status(400).json({ error: "user_id is required" });
    return;
  }

  const group = db.prepare("SELECT id FROM groups WHERE id = ?").get(groupId);
  if (!group) {
    res.status(404).json({ error: "Group not found" });
    return;
  }

  const user = db.prepare("SELECT id FROM users WHERE id = ?").get(user_id);
  if (!user) {
    res.status(404).json({ error: "User not found" });
    return;
  }

  db.prepare("INSERT OR IGNORE INTO group_members (group_id, user_id) VALUES (?, ?)").run(
    groupId,
    user_id
  );

  res.status(201).json({ message: "Member added" });
});

router.get("/:id/balances", (req: Request, res: Response) => {
  const db = getDb();
  const groupId = req.params.id;

  const group = db.prepare("SELECT id FROM groups WHERE id = ?").get(groupId);
  if (!group) {
    res.status(404).json({ error: "Group not found" });
    return;
  }

  const members = db.prepare(`
    SELECT u.id, u.name
    FROM group_members gm
    JOIN users u ON gm.user_id = u.id
    WHERE gm.group_id = ?
  `).all(groupId) as Array<{ id: string; name: string }>;

  // Calculate net balance for each member in this group
  const balanceMap = new Map<string, number>();
  members.forEach((m) => balanceMap.set(m.id, 0));

  // Add what each person paid
  const payments = db.prepare(`
    SELECT paid_by, SUM(amount) as total
    FROM expenses
    WHERE group_id = ?
    GROUP BY paid_by
  `).all(groupId) as Array<{ paid_by: string; total: number }>;

  for (const p of payments) {
    balanceMap.set(p.paid_by, (balanceMap.get(p.paid_by) || 0) + p.total);
  }

  // Subtract what each person owes (from splits)
  const splits = db.prepare(`
    SELECT es.user_id, SUM(es.amount) as total
    FROM expense_splits es
    JOIN expenses e ON es.expense_id = e.id
    WHERE e.group_id = ?
    GROUP BY es.user_id
  `).all(groupId) as Array<{ user_id: string; total: number }>;

  for (const s of splits) {
    balanceMap.set(s.user_id, (balanceMap.get(s.user_id) || 0) - s.total);
  }

  // Factor in settlements
  const settlements = db.prepare(`
    SELECT paid_by, paid_to, SUM(amount) as total
    FROM settlements
    WHERE group_id = ?
    GROUP BY paid_by, paid_to
  `).all(groupId) as Array<{ paid_by: string; paid_to: string; total: number }>;

  for (const s of settlements) {
    balanceMap.set(s.paid_by, (balanceMap.get(s.paid_by) || 0) - s.total);
    balanceMap.set(s.paid_to, (balanceMap.get(s.paid_to) || 0) + s.total);
  }

  const balances = members.map((m) => ({
    userId: m.id,
    name: m.name,
    balance: Math.round((balanceMap.get(m.id) || 0) * 100) / 100,
  }));

  // Calculate simplified debts (who owes whom)
  const debtors = balances.filter((b) => b.balance < -0.01).map((b) => ({ ...b }));
  const creditors = balances.filter((b) => b.balance > 0.01).map((b) => ({ ...b }));

  const simplifiedDebts: Array<{
    from: string;
    fromName: string;
    to: string;
    toName: string;
    amount: number;
  }> = [];

  debtors.sort((a, b) => a.balance - b.balance);
  creditors.sort((a, b) => b.balance - a.balance);

  let i = 0;
  let j = 0;
  while (i < debtors.length && j < creditors.length) {
    const debt = Math.min(-debtors[i].balance, creditors[j].balance);
    if (debt > 0.01) {
      simplifiedDebts.push({
        from: debtors[i].userId,
        fromName: debtors[i].name,
        to: creditors[j].userId,
        toName: creditors[j].name,
        amount: Math.round(debt * 100) / 100,
      });
    }
    debtors[i].balance += debt;
    creditors[j].balance -= debt;
    if (Math.abs(debtors[i].balance) < 0.01) i++;
    if (Math.abs(creditors[j].balance) < 0.01) j++;
  }

  res.json({ balances, simplifiedDebts });
});

export default router;
