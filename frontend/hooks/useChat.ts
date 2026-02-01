"use client";

import { useState, useEffect, useCallback } from "react";
import * as api from "@/lib/api";

export interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

export function useChat(userId: string | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    if (!userId) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      const history = await api.getChatHistory();

      if (history.messages.length > 0) {
        setMessages(history.messages);
      } else {
        // No history, show initial greeting
        setMessages([
          {
            role: "assistant",
            content:
              "Hello! I'm your AI Task Assistant. I can help you add, edit, or delete tasks. What would you like to do today?",
          },
        ]);
      }
      setError(null);
    } catch (err) {
      console.error("Failed to fetch chat history:", err);
      // On error, show greeting anyway
      setMessages([
        {
          role: "assistant",
          content:
            "Hello! I'm your AI Task Assistant. I can help you add, edit, or delete tasks. What would you like to do today?",
        },
      ]);
      setError(null); // Don't show error to user for history fetch
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!userId || !content.trim() || isSending) return;

      const userMessage: Message = { role: "user", content };
      setMessages((prev) => [...prev, userMessage]);
      setIsSending(true);
      setError(null);

      try {
        const allMessages = [...messages, userMessage];
        const response = await api.chat(allMessages);

        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: response.content },
        ]);

        // Notify that tasks may have changed
        window.dispatchEvent(new Event("tasks-changed"));
        localStorage.setItem("tasks-updated", Date.now().toString());
      } catch (err: any) {
        const errorMessage =
          err.message || "I encountered an error. Please check your configuration.";
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `Error: ${errorMessage}` },
        ]);
        setError(errorMessage);
      } finally {
        setIsSending(false);
      }
    },
    [userId, messages, isSending]
  );

  return {
    messages,
    isLoading,
    isSending,
    error,
    sendMessage,
    refresh: fetchHistory,
  };
}
