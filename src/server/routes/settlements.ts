import { Router, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import { getDb } from "../database";

const router = Router();

router.get("/group/:groupId", (req: Request, res: Response) => {
  const db = getDb();
  const { groupId } = req.params;

  const settlements = db.prepare(`
    SELECT s.*,
      payer.name as paid_by_name,
      payee.name as paid_to_name
    FROM settlements s
    JOIN users payer ON s.paid_by = payer.id
    JOIN users payee ON s.paid_to = payee.id
    WHERE s.group_id = ?
    ORDER BY s.created_at DESC
  `).all(groupId);

  res.json(settlements);
});

router.post("/", (req: Request, res: Response) => {
  const db = getDb();
  const { group_id, paid_by, paid_to, amount } = req.body;

  if (!group_id || !paid_by || !paid_to || !amount) {
    res.status(400).json({ error: "group_id, paid_by, paid_to, and amount are required" });
    return;
  }

  if (amount <= 0) {
    res.status(400).json({ error: "Amount must be positive" });
    return;
  }

  if (paid_by === paid_to) {
    res.status(400).json({ error: "Cannot settle with yourself" });
    return;
  }

  const group = db.prepare("SELECT id FROM groups WHERE id = ?").get(group_id);
  if (!group) {
    res.status(404).json({ error: "Group not found" });
    return;
  }

  const id = uuidv4();
  db.prepare(
    "INSERT INTO settlements (id, group_id, paid_by, paid_to, amount) VALUES (?, ?, ?, ?, ?)"
  ).run(id, group_id, paid_by, paid_to, amount);

  const settlement = db.prepare("SELECT * FROM settlements WHERE id = ?").get(id);
  res.status(201).json(settlement);
});

export default router;
