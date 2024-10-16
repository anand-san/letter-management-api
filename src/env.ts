import dotenv from "dotenv";
import path from "path";

export interface Env {
  [key: string]: string;

  PORT: string;
  FIREBASE_SERVICE_ACCOUNT: string;
  FIREBASE_STORAGE_BUCKET: string;
  GOOGLE_CLOUD_PROJECT_ID: string;
  GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION: string;
  GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID: string;
  OPENAI_API_KEY: string;
  OPENAI_MODEL: string;
}

// Load .env file
if (process.env.NODE_ENV !== "production") {
  dotenv.config({ path: path.resolve(__dirname, "../.env") });
}
// Create and validate the env object
const env: Env = {
  PORT: process.env.PORT || "",
  FIREBASE_SERVICE_ACCOUNT: process.env.FIREBASE_SERVICE_ACCOUNT || "",
  FIREBASE_STORAGE_BUCKET: process.env.FIREBASE_STORAGE_BUCKET || "",
  GOOGLE_CLOUD_PROJECT_ID: process.env.GOOGLE_CLOUD_PROJECT_ID || "",
  GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION:
    process.env.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION || "",
  GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID:
    process.env.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID || "",
  OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
  OPENAI_MODEL: process.env.OPENAI_MODEL || "",
};

// Validate that all required environment variables are set
Object.entries(env).forEach(([key, value]) => {
  if (value === "") {
    throw new Error(`Environment variable ${key} is not set`);
  }
});

export default env;
