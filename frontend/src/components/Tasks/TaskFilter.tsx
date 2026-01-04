"use client";

import { useTask } from "@/hooks/useTask";
import { TaskStatus, TaskPriority } from "@/types";

export default function TaskFilter() {
  const { filters, setFilter, loadTasks } = useTask();

  const handleStatusChange = (value: string) => {
    const status = value === "all" ? undefined : (value as TaskStatus);
    setFilter({ status });
    loadTasks({ status });
  };

  const handlePriorityChange = (value: string) => {
    const priority = value === "all" ? undefined : (value as TaskPriority);
    setFilter({ priority });
    loadTasks({ priority });
  };

  return (
    <div className="flex flex-wrap gap-4 mb-8">
      <div className="relative">
        <select
          value={filters.status || "all"}
          onChange={(e) => handleStatusChange(e.target.value)}
          className="appearance-none pl-4 pr-10 py-2.5 bg-slate-800 text-slate-200 border border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-500 hover:bg-slate-700/50 transition-all cursor-pointer text-sm font-medium"
        >
          <option value="all">All Status</option>
          <option value={TaskStatus.PENDING}>Pending</option>
          <option value={TaskStatus.COMPLETED}>Completed</option>
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      <div className="relative">
        <select
          value={filters.priority || "all"}
          onChange={(e) => handlePriorityChange(e.target.value)}
          className="appearance-none pl-4 pr-10 py-2.5 bg-slate-800 text-slate-200 border border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-500 hover:bg-slate-700/50 transition-all cursor-pointer text-sm font-medium"
        >
          <option value="all">All Priorities</option>
          <option value={TaskPriority.LOW}>Low Priority</option>
          <option value={TaskPriority.MEDIUM}>Medium Priority</option>
          <option value={TaskPriority.HIGH}>High Priority</option>
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
}