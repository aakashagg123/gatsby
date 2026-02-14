import React, { useState } from "react";
import { User } from "../types";
import { createGroup } from "../api";

interface Props {
  users: User[];
  onGroupCreated: () => void;
}

export default function CreateGroup({ users, onGroupCreated }: Props) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [createdBy, setCreatedBy] = useState("");
  const [selectedMembers, setSelectedMembers] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const toggleMember = (userId: string) => {
    setSelectedMembers((prev) =>
      prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!createdBy) {
      setError("Please select who is creating this group");
      return;
    }
    setError("");
    setLoading(true);
    try {
      await createGroup(name.trim(), description.trim(), createdBy, selectedMembers);
      setName("");
      setDescription("");
      setCreatedBy("");
      setSelectedMembers([]);
      onGroupCreated();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create group");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Create Group</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Group name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select value={createdBy} onChange={(e) => setCreatedBy(e.target.value)} required>
          <option value="">Select creator</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name}
            </option>
          ))}
        </select>
        <div className="member-select">
          <label>Add members:</label>
          {users
            .filter((u) => u.id !== createdBy)
            .map((u) => (
              <label key={u.id} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={selectedMembers.includes(u.id)}
                  onChange={() => toggleMember(u.id)}
                />
                {u.name}
              </label>
            ))}
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Create Group"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
