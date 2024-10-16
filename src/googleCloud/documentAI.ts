import type { Context } from "hono";
import { DocumentProcessorServiceClient } from "documentai";

export async function ocrFile(file: File, ctx: Context): Promise<string> {
  try {
    const env = ctx.get("env");

    const client = new DocumentProcessorServiceClient({
      apiEndpoint: `${env.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION}-documentai.googleapis.com`,
    });

    const arrayBuffer = await file.arrayBuffer();
    const uint8Array = new Uint8Array(arrayBuffer);

    const processorName = `projects/${env.GOOGLE_CLOUD_PROJECT_ID}/locations/${env.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION}/processors/${env.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID}`;

    const [result] = await client.processDocument({
      name: processorName,
      rawDocument: {
        content: uint8Array,
        mimeType: file.type,
      },
    });

    return result.document?.text ?? "";
  } catch (e) {
    console.error(e);
    throw new Error("Failed to extract text from the document");
  }
}
