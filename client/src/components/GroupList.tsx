import React from "react";
import { Group } from "../types";

interface Props {
  groups: Group[];
  onSelectGroup: (id: string) => void;
}

export default function GroupList({ groups, onSelectGroup }: Props) {
  if (groups.length === 0) {
    return <p className="empty">No groups yet. Create one to get started!</p>;
  }

  return (
    <div className="group-list">
      {groups.map((group) => (
        <div
          key={group.id}
          className="group-card"
          onClick={() => onSelectGroup(group.id)}
        >
          <h3>{group.name}</h3>
          {group.description && <p>{group.description}</p>}
          <div className="group-meta">
            <span>{group.member_count || 0} members</span>
            <span>Created by {group.created_by_name}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
