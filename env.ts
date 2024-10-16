import { loadSync } from "std/dotenv/mod.ts";

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

const env = loadSync() as Env;

export default env;
