"use client";

import { Task } from "@/types";
import TaskCard from "./TaskCard";

interface TaskListProps {
  tasks: Task[];
}

export default function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 bg-slate-800/30 rounded-2xl border border-slate-700/50 border-dashed">
        <div className="text-5xl mb-4 opacity-50">📋</div>
        <h3 className="text-lg font-medium text-slate-200 mb-1">No tasks yet</h3>
        <p className="text-slate-500 max-w-sm mx-auto">
          Get started by creating your first task to stay organized and productive.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}