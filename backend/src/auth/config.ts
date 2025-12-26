import { betterAuth } from "better-auth";
import { neon } from "@neondatabase/serverless";

// Database connection for Neon DB
const db = neon(process.env.NEON_DB_URL!);

// Extended user schema with additional fields for personalization
const extendedUserSchema = {
  // Add the additional fields to the user schema
  software_background: {
    type: "string",
    required: true,
  },
  hardware_background: {
    type: "string",
    required: true,
  },
};

export const auth = betterAuth({
  database: {
    connection: db,
    provider: "neon",
  },
  user: {
    additionalFields: {
      software_background: {
        type: "string",
        required: true,
      },
      hardware_background: {
        type: "string",
        required: true,
      },
    },
  },
  socialProviders: {
    // Add social provider configurations if needed
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  // Configure JWT settings for RS256 algorithm
  jwt: {
    expiresIn: "7d", // Token expires in 7 days
    algorithm: "RS256", // Use RS256 algorithm as required
  },
});

export default auth;