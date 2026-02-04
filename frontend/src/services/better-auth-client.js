import { createAuthClient } from "better-auth/react";

export const { useAuth, signIn, signOut, signUp } = createAuthClient({
  fetchOptions: {
    baseUrl: typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000',
  },
});