// import type { User, AuthState } from "@/types";

// const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://backend-todo-ai-render.onrender.com";

// interface AuthResponse {
//   user: User;
// }

// export async function signUp(
//   email: string,
//   password: string
// ): Promise<AuthResponse> {
//   const response = await fetch(`${API_URL}/api/auth/signup`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     credentials: "include",
//     body: JSON.stringify({ email, password }),
//   });

//   if (!response.ok) {
//     const error = await response.json();
//     throw new Error(error.detail || "Failed to sign up");
//   }

//   return response.json();
// }

// export async function signIn(
//   email: string,
//   password: string
// ): Promise<AuthResponse> {
//   const response = await fetch(`${API_URL}/api/auth/signin`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     credentials: "include",
//     body: JSON.stringify({ email, password }),
//   });

//   if (!response.ok) {
//     const error = await response.json();
//     throw new Error(error.detail || "Failed to sign in");
//   }

//   return response.json();
// }

// export async function signOut(): Promise<void> {
//   try {
//     const response = await fetch(`${API_URL}/api/auth/signout`, {
//       method: "POST",
//       credentials: "include",
//     });

//     // Don't throw error if signout fails - we'll clear local state anyway
//     if (!response.ok) {
//       console.warn("Backend signout failed, but clearing local session anyway");
//     }
//   } catch (error) {
//     // If fetch fails (network error, backend down, etc.), just log it
//     // We'll still clear the local session below
//     console.warn("Failed to reach backend for signout:", error);
//   }

// //   // Always clear local state, even if backend call failed
// //   // This ensures user can sign out even if backend is down
// // }
// // // comment working code
// // // export async function getSession(): Promise<User | null> {
// // //   try {
// // //     const response = await fetch(`${API_URL}/api/auth/session`, {
// // //       credentials: "include",
// // //     });

// // //     if (!response.ok) {
// // //       return null;
// // //     }

// // //     const data = await response.json();
// // //     return data.user || null;
// // //   } catch {
// // //     return null;
// // //   }
// // // }

// export async function getSession(): Promise<User | null> {
//   try {
//     const response = await fetch(`${API_URL}/api/auth/session`, {
//       credentials: "include", // <- very important
//     });
//     if (!response.ok) return null;
//     const data = await response.json();
//     return data.user || null;
//   } catch {
//     return null;
//   }
// }



// new
import type { User, AuthResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://render-todo-auth-combine-ai.onrender.com";

// Helper to store token
function setAuthToken(token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
}

// Helper to get token
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
}

// Helper to clear token
function clearAuthToken() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
}

export async function signUp(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/api/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // Remove credentials: "include" to avoid cookie dependency
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to sign up");
  }

  const data: AuthResponse = await response.json();

  // Store the JWT token in localStorage
  if (data.token) {
    setAuthToken(data.token);
  }

  return data;
}

export async function signIn(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/api/auth/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // Remove credentials: "include" to avoid cookie dependency
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to sign in");
  }

  const data: AuthResponse = await response.json();

  // Store the JWT token in localStorage
  if (data.token) {
    setAuthToken(data.token);
  }

  return data;
}

export async function signOut(): Promise<void> {
  // Get the token to include in the request
  const token = getAuthToken();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/api/auth/signout`, {
    method: "POST",
    headers,
    // Remove credentials: "include" to avoid cookie dependency
  });

  clearAuthToken(); // Clear stored token

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to sign out");
  }
}

export async function getSession(): Promise<User | null> {
  try {
    const token = getAuthToken();
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}/api/auth/session`, {
      headers,
      // Remove credentials: "include" to avoid cookie dependency
    });

    if (!response.ok) {
      if (response.status === 401) {
        clearAuthToken();
      }
      return null;
    }

    const data = await response.json();
    return data.user || null;
  } catch (error) {
    console.error("Session error:", error);
    clearAuthToken(); // Clear token on error
    return null;
  }
}
