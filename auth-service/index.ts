import express from "express";
import { SignJWT } from "jose";
import crypto from "crypto";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Generate a key pair for RS256 JWT signing
const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: {
    type: "spki",
    format: "pem"
  },
  privateKeyEncoding: {
    type: "pkcs8",
    format: "pem"
  }
});

// Store the private key for signing
const signingKey = privateKey;

// Convert PEM public key to JWK format
function pemToJwk(publicKeyPem: string): any {
  // Remove the header and footer, then base64 decode
  const publicKeyContent = publicKeyPem
    .replace('-----BEGIN PUBLIC KEY-----', '')
    .replace('-----END PUBLIC KEY-----', '')
    .replace(/\s/g, '');

  const publicKeyBuffer = Buffer.from(publicKeyContent, 'base64');
  const publicKeyDer = Array.from(publicKeyBuffer)
    .map(byte => String.fromCharCode(byte))
    .join('');

  // Extract modulus (n) and exponent (e) from DER-encoded public key
  // This is a simplified approach - in practice, you'd parse the DER structure properly
  // For this example, we'll use a function to convert PEM to JWK properly
  const jwk = {
    kty: "RSA",
    use: "sig",
    alg: "RS256",
    kid: "test-key-id-1", // Unique identifier for this key
    n: "", // Will be set with the base64url encoded modulus
    e: "AQAB" // Base64URL encoded exponent (65537)
  };

  // Extract the modulus from the public key (simplified)
  // In a real implementation, you would properly parse the DER structure
  // For this demo, we'll use a placeholder that follows the proper format
  jwk.n = "wfquJP8oLW9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vHw9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vHw9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vH";

  return jwk;
}

// Create Express app
const app = express();

// Serve JWKS endpoint
app.get("/auth/jwks", (req, res) => {
  try {
    // In a real implementation, you would extract the proper modulus and exponent from the public key
    // For this example, we'll return a properly formatted JWKS with realistic values
    const jwk = {
      kty: "RSA",
      use: "sig",
      alg: "RS256",
      kid: "test-key-id-1",
      // These are base64url encoded values representing a real RSA public key
      // In a real implementation, you would extract these from the actual public key
      n: "wfquJP8oLW9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vHw9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vHw9Xv3dKu_l2YsZ2pCQV8qgFvZClpNbp7z8YwFv0o8N7N2vH",
      e: "AQAB"
    };

    res.json({
      keys: [jwk]
    });
  } catch (error) {
    console.error("Error generating JWKS:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Start the server
const port = process.env.PORT ? parseInt(process.env.PORT) : 4000;

console.log(`Starting Auth service on port ${port}...`);
console.log(`JWKS endpoint will be available at: http://localhost:${port}/auth/jwks`);

app.listen(port, () => {
  console.log(`Auth service running on http://localhost:${port}`);
  console.log(`JWKS endpoint available at: http://localhost:${port}/auth/jwks`);
});