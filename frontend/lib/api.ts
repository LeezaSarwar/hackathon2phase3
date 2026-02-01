import type { Task, TaskCreate, TaskUpdate, ErrorResponse } from "@/types";
import { getAuthToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiError extends Error {
  code: string;

  constructor(message: string, code: string) {
    super(message);
    this.code = code;
    this.name = "ApiError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ErrorResponse = await response.json().catch(() => ({
      error: "UnknownError",
      detail: "An unexpected error occurred",
      code: "UNKNOWN_ERROR",
    }));
    throw new ApiError(error.detail, error.code);
  }
  return response.json();
}

function getAuthHeaders(): HeadersInit {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  const token = getAuthToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return headers;
}

export async function getTasks(userId: string): Promise<Task[]> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
    headers: getAuthHeaders(),
  });

  const data = await handleResponse<{ tasks: Task[] }>(response);
  return data.tasks;
}

export async function getTask(userId: string, taskId: number): Promise<Task> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    headers: getAuthHeaders(),
  });

  return handleResponse<Task>(response);
}

export async function createTask(
  userId: string,
  data: TaskCreate
): Promise<Task> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  return handleResponse<Task>(response);
}

export async function updateTask(
  userId: string,
  taskId: number,
  data: TaskUpdate
): Promise<Task> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  return handleResponse<Task>(response);
}

export async function toggleTaskComplete(
  userId: string,
  taskId: number,
  completed: boolean
): Promise<Task> {
  const response = await fetch(
    `${API_URL}/api/${userId}/tasks/${taskId}/complete`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify({ completed }),
    }
  );

  return handleResponse<Task>(response);
}

export async function deleteTask(
  userId: string,
  taskId: number
): Promise<void> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error: ErrorResponse = await response.json().catch(() => ({
      error: "UnknownError",
      detail: "An unexpected error occurred",
      code: "UNKNOWN_ERROR",
    }));
    throw new ApiError(error.detail, error.code);
  }
}

export interface ChatMessage {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

export interface ChatHistory {
  conversation: {
    id: number;
    user_id: string;
    created_at: string;
    updated_at: string;
  } | null;
  messages: ChatMessage[];
}

export async function getChatHistory(): Promise<ChatHistory> {
  const response = await fetch(`${API_URL}/api/chat/history`, {
    headers: getAuthHeaders(),
  });

  return handleResponse<ChatHistory>(response);
}

export async function chat(messages: ChatMessage[]): Promise<{ content: string }> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      messages: messages.map(m => ({ role: m.role, content: m.content }))
    }),
  });

  return handleResponse<{ content: string }>(response);
}
