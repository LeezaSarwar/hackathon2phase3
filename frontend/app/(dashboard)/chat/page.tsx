"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useChat } from "@/hooks/useChat";

export default function ChatPage() {
  const { user } = useAuth();
  const { messages, isLoading, isSending, sendMessage } = useChat(user?.id || null);
  const [input, setInput] = useState("");

  // Removed auto-scroll behavior - user has full manual control

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const messageContent = input;
    setInput("");
    await sendMessage(messageContent);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-80px)] sm:h-[calc(100vh-80px)]">
        <div className="text-gray-500 text-sm sm:text-base">Loading chat history...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] sm:h-[calc(100vh-80px)] w-full max-w-4xl mx-auto px-3 py-4 sm:px-4 md:px-6 md:py-8">
      <div className="flex-1 overflow-y-auto mb-3 sm:mb-4 space-y-3 sm:space-y-4 pr-2 sm:pr-4">
        {messages.map((message, index) => (
          <div
            key={message.id || index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[90%] sm:max-w-[85%] md:max-w-[80%] rounded-2xl px-3 py-2 sm:px-4 sm:py-2.5 ${
                message.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              }`}
            >
              <p className="text-sm sm:text-base whitespace-pre-wrap break-words">{message.content}</p>
            </div>
          </div>
        ))}
        {isSending && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-2xl px-3 py-2 sm:px-4 sm:py-2.5">
              <div className="flex gap-1">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me to add a task..."
          className="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl px-3 py-2.5 pr-11 sm:px-4 sm:py-3 sm:pr-12 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          disabled={isSending}
        />
        <button
          type="submit"
          disabled={isSending || !input.trim()}
          className="absolute right-1.5 sm:right-2 top-1/2 -translate-y-1/2 p-2 sm:p-2 text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-lg transition-all disabled:opacity-50 touch-manipulation"
        >
          <svg className="w-5 h-5 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </form>
    </div>
  );
}
