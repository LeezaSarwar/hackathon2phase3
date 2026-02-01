"use client";

import { useState, useEffect, useCallback } from "react";
import type { Task, TaskCreate, TaskUpdate } from "@/types";
import * as api from "@/lib/api";

export function useTasks(userId: string | null) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    if (!userId) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      const data = await api.getTasks(userId);
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Refresh when window gains focus (e.g., after returning from chatbot)
  useEffect(() => {
    const handleFocus = () => {
      fetchTasks();
    };

    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [fetchTasks]);

  // Refresh when external task modification events occur (e.g., from chatbot)
  useEffect(() => {
    const handleTasksChanged = () => {
      fetchTasks();
    };

    window.addEventListener("tasks-changed", handleTasksChanged);
    return () => window.removeEventListener("tasks-changed", handleTasksChanged);
  }, [fetchTasks]);

  // Also refresh on storage events (cross-tab communication)
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      if (e.key === "tasks-updated") {
        fetchTasks();
      }
    };

    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [fetchTasks]);

  const createTask = useCallback(
    async (data: TaskCreate) => {
      if (!userId) throw new Error("Not authenticated");

      const newTask = await api.createTask(userId, data);
      setTasks((prev) => [newTask, ...prev]);
      return newTask;
    },
    [userId]
  );

  const updateTask = useCallback(
    async (taskId: number, data: TaskUpdate) => {
      if (!userId) throw new Error("Not authenticated");

      const updatedTask = await api.updateTask(userId, taskId, data);
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? updatedTask : t))
      );
      return updatedTask;
    },
    [userId]
  );

  const toggleComplete = useCallback(
    async (taskId: number, completed: boolean) => {
      if (!userId) throw new Error("Not authenticated");

      // Optimistic update
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, completed } : t))
      );

      try {
        const updatedTask = await api.toggleTaskComplete(userId, taskId, completed);
        setTasks((prev) =>
          prev.map((t) => (t.id === taskId ? updatedTask : t))
        );
      } catch (err) {
        // Rollback on error
        setTasks((prev) =>
          prev.map((t) => (t.id === taskId ? { ...t, completed: !completed } : t))
        );
        throw err;
      }
    },
    [userId]
  );

  const deleteTask = useCallback(
    async (taskId: number) => {
      if (!userId) throw new Error("Not authenticated");

      // Store task for potential rollback
      const taskToDelete = tasks.find((t) => t.id === taskId);

      // Optimistic update
      setTasks((prev) => prev.filter((t) => t.id !== taskId));

      try {
        await api.deleteTask(userId, taskId);
      } catch (err) {
        // Rollback on error
        if (taskToDelete) {
          setTasks((prev) => [...prev, taskToDelete].sort(
            (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          ));
        }
        throw err;
      }
    },
    [userId, tasks]
  );

  return {
    tasks,
    isLoading,
    error,
    createTask,
    updateTask,
    toggleComplete,
    deleteTask,
    refresh: fetchTasks,
  };
}
