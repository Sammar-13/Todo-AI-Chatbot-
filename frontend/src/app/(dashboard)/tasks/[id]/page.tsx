"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { useTask } from "@/hooks/useTask";
import { Task, TaskStatus, TaskPriority } from "@/types";

const statusColors = {
  pending: "bg-yellow-100 text-yellow-800",
  completed: "bg-green-100 text-green-800",
};

const priorityColors = {
  low: "bg-blue-100 text-blue-800",
  medium: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-800",
};

export default function TaskDetailPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;

  const { isAuthenticated } = useAuth();
  const { updateTask, deleteTask, tasks } = useTask();

  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<Partial<Task>>({});
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    // Find task from context
    const foundTask = tasks.find((t) => t.id === taskId);
    if (foundTask) {
      setTask(foundTask);
      setEditData(foundTask);
    }
    setIsLoading(false);
  }, [taskId, tasks, isAuthenticated, router]);

  const handleStatusChange = async (newStatus: TaskStatus) => {
    if (!task) return;
    setIsSaving(true);
    try {
      setError(null);
      await updateTask(task.id, { status: newStatus });
      setTask({ ...task, status: newStatus });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update status";
      setError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  const handlePriorityChange = async (newPriority: TaskPriority) => {
    if (!task) return;
    setIsSaving(true);
    try {
      setError(null);
      await updateTask(task.id, { priority: newPriority });
      setTask({ ...task, priority: newPriority });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update priority";
      setError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!task) return;
    setIsSaving(true);
    try {
      setError(null);
      const updates = {
        title: editData.title !== task.title ? editData.title : undefined,
        description: editData.description !== task.description ? editData.description : undefined,
      };
      const filteredUpdates = Object.fromEntries(
        Object.entries(updates).filter(([, v]) => v !== undefined)
      );

      if (Object.keys(filteredUpdates).length > 0) {
        await updateTask(task.id, filteredUpdates);
        setTask({ ...task, ...filteredUpdates });
      }
      setIsEditing(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to save changes";
      setError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!task || !confirm("Are you sure you want to delete this task?")) return;
    try {
      setError(null);
      await deleteTask(task.id);
      router.push("/tasks");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to delete task";
      setError(errorMessage);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-500">Loading task...</div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Task Not Found</h2>
        <button
          onClick={() => router.push("/tasks")}
          className="text-indigo-600 hover:text-indigo-700 transition"
        >
          ← Back to Tasks
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <button
          onClick={() => router.push("/tasks")}
          className="text-indigo-600 hover:text-indigo-700 transition flex items-center gap-2"
        >
          ← Back to Tasks
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-lg p-6">
        {/* Title */}
        <div className="mb-6">
          {isEditing ? (
            <input
              type="text"
              value={editData.title || ""}
              onChange={(e) => setEditData({ ...editData, title: e.target.value })}
              className="w-full text-3xl font-bold text-gray-900 border-b-2 border-indigo-600 pb-2 focus:outline-none"
            />
          ) : (
            <h1 className="text-3xl font-bold text-gray-900">{task.title}</h1>
          )}
        </div>

        {/* Status & Priority */}
        <div className="flex flex-wrap gap-3 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              value={task.status}
              onChange={(e) => handleStatusChange(e.target.value as TaskStatus)}
              disabled={isSaving}
              className={`px-3 py-1 rounded text-sm font-medium border-0 ${
                statusColors[task.status as keyof typeof statusColors]
              } cursor-pointer disabled:opacity-50`}
            >
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
            <select
              value={task.priority}
              onChange={(e) => handlePriorityChange(e.target.value as TaskPriority)}
              disabled={isSaving}
              className={`px-3 py-1 rounded text-sm font-medium border-0 ${
                priorityColors[task.priority as keyof typeof priorityColors]
              } cursor-pointer disabled:opacity-50`}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        {/* Description */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
          {isEditing ? (
            <textarea
              value={editData.description || ""}
              onChange={(e) => setEditData({ ...editData, description: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent resize-none"
              rows={4}
            />
          ) : (
            <p className="text-gray-600 bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
              {task.description || "No description provided"}
            </p>
          )}
        </div>

        {/* Metadata */}
        <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
          <div>
            <label className="block font-medium text-gray-700 mb-1">Created</label>
            <p className="text-gray-600">
              {new Date(task.created_at).toLocaleString()}
            </p>
          </div>
          <div>
            <label className="block font-medium text-gray-700 mb-1">Last Updated</label>
            <p className="text-gray-600">
              {new Date(task.updated_at).toLocaleString()}
            </p>
          </div>
          {task.due_date && (
            <div>
              <label className="block font-medium text-gray-700 mb-1">Due Date</label>
              <p className="text-gray-600">
                {new Date(task.due_date).toLocaleDateString()}
              </p>
            </div>
          )}
          {task.completed_at && (
            <div>
              <label className="block font-medium text-gray-700 mb-1">Completed</label>
              <p className="text-gray-600">
                {new Date(task.completed_at).toLocaleString()}
              </p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-3 pt-6 border-t">
          {!isEditing ? (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="flex-1 px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                disabled={isSaving}
              >
                ✏️ Edit
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition disabled:opacity-50"
                disabled={isSaving}
              >
                🗑️ Delete
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleSaveEdit}
                className="flex-1 px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition disabled:opacity-50"
                disabled={isSaving}
              >
                💾 Save
              </button>
              <button
                onClick={() => {
                  setIsEditing(false);
                  setEditData(task);
                }}
                className="flex-1 px-4 py-2 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition disabled:opacity-50"
                disabled={isSaving}
              >
                ❌ Cancel
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
