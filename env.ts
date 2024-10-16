import "jsr:@std/dotenv/load";
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

function getEnv(): Env {
  // Use Deno.env to get environment variables
  return {
    PORT: Deno.env.get("PORT") || "",
    FIREBASE_SERVICE_ACCOUNT: Deno.env.get("FIREBASE_SERVICE_ACCOUNT") || "",
    FIREBASE_STORAGE_BUCKET: Deno.env.get("FIREBASE_STORAGE_BUCKET") || "",
    GOOGLE_CLOUD_PROJECT_ID: Deno.env.get("GOOGLE_CLOUD_PROJECT_ID") || "",
    GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION:
      Deno.env.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION") || "",
    GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID:
      Deno.env.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID") || "",
    OPENAI_API_KEY: Deno.env.get("OPENAI_API_KEY") || "",
    OPENAI_MODEL: Deno.env.get("OPENAI_MODEL") || "",
  };
}

const env: Env = getEnv();

export default env;
