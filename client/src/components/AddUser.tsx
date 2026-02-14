import React, { useState } from "react";
import { createUser } from "../api";

interface Props {
  onUserAdded: () => void;
}

export default function AddUser({ onUserAdded }: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await createUser(name.trim(), email.trim());
      setName("");
      setEmail("");
      onUserAdded();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to add user");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Add User</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add User"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
