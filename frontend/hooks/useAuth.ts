"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { User, AuthState } from "@/types";
import { getSession, signOut as authSignOut } from "@/lib/auth";

export function useAuth() {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  const checkSession = useCallback(async () => {
    try {
      // Add timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Session check timeout")), 10000)
      );

      const userPromise = getSession();
      const user = await Promise.race([userPromise, timeoutPromise]);

      setState({
        user: user as User,
        isLoading: false,
        isAuthenticated: !!user,
      });
    } catch (error) {
      console.log("Session check failed or timed out:", error);
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
      });
    }
  }, []);

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  const signOut = useCallback(async () => {
    try {
      // Try to call backend signout
      await authSignOut();
    } catch (error) {
      // If backend call fails, just log it - we'll still clear local state
      console.warn("Backend signout failed:", error);
    } finally {
      // Always clear local state and redirect, even if backend call failed
      // This ensures user can sign out even if backend is down
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
      });
      router.push("/signin");
    }
  }, [router]);

  return {
    ...state,
    signOut,
    refreshSession: checkSession,
  };
}
