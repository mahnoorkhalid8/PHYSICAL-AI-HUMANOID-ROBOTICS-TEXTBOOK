import { createAuthClient } from "@better-auth/client";

// Create the auth client
export const authClient = createAuthClient({
  baseURL: process.env.REACT_APP_BETTER_AUTH_URL || "http://localhost:4000", // Default to auth service port
  fetch: globalThis.fetch,
});

export default authClient;