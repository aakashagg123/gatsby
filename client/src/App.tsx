import React, { useState, useEffect, useCallback } from "react";
import { User, Group } from "./types";
import { getUsers, getGroups } from "./api";
import AddUser from "./components/AddUser";
import CreateGroup from "./components/CreateGroup";
import GroupList from "./components/GroupList";
import GroupDetail from "./components/GroupDetail";
import "./App.css";

type View = "dashboard" | "group";

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [view, setView] = useState<View>("dashboard");
  const [selectedGroupId, setSelectedGroupId] = useState<string>("");
  const [showAddUser, setShowAddUser] = useState(false);
  const [showCreateGroup, setShowCreateGroup] = useState(false);

  const loadUsers = useCallback(async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch {
      console.error("Failed to load users");
    }
  }, []);

  const loadGroups = useCallback(async () => {
    try {
      const data = await getGroups();
      setGroups(data);
    } catch {
      console.error("Failed to load groups");
    }
  }, []);

  useEffect(() => {
    loadUsers();
    loadGroups();
  }, [loadUsers, loadGroups]);

  const handleSelectGroup = (id: string) => {
    setSelectedGroupId(id);
    setView("group");
  };

  const handleBackToDashboard = () => {
    setView("dashboard");
    setSelectedGroupId("");
    loadGroups();
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 onClick={handleBackToDashboard} style={{ cursor: "pointer" }}>
          Splitwise Clone
        </h1>
        <p className="subtitle">Split expenses with friends and groups</p>
      </header>

      <main className="app-main">
        {view === "dashboard" && (
          <>
            <div className="actions">
              <button
                className="action-btn"
                onClick={() => setShowAddUser(!showAddUser)}
              >
                {showAddUser ? "Cancel" : "+ Add User"}
              </button>
              <button
                className="action-btn primary"
                onClick={() => setShowCreateGroup(!showCreateGroup)}
              >
                {showCreateGroup ? "Cancel" : "+ Create Group"}
              </button>
            </div>

            {showAddUser && (
              <AddUser
                onUserAdded={() => {
                  loadUsers();
                  setShowAddUser(false);
                }}
              />
            )}

            {showCreateGroup && users.length > 0 && (
              <CreateGroup
                users={users}
                onGroupCreated={() => {
                  loadGroups();
                  setShowCreateGroup(false);
                }}
              />
            )}

            {users.length === 0 && (
              <div className="card info">
                <p>Start by adding some users, then create a group to track shared expenses.</p>
              </div>
            )}

            {users.length > 0 && (
              <div className="card">
                <h3>Users ({users.length})</h3>
                <div className="user-list">
                  {users.map((u) => (
                    <span key={u.id} className="user-chip">
                      {u.name}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <h2>Groups</h2>
            <GroupList groups={groups} onSelectGroup={handleSelectGroup} />
          </>
        )}

        {view === "group" && selectedGroupId && (
          <GroupDetail
            groupId={selectedGroupId}
            users={users}
            onBack={handleBackToDashboard}
          />
        )}
      </main>
    </div>
  );
}

export default App;
