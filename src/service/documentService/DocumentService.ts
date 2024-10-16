import type { Context } from "hono";
import { FirebaseManager } from "../../firebase/index";
import { ocrFile } from "../../googleCloud/documentAI";
import { stripSingleLine } from "../../utils/stripSingleLine";

export class DocumentService {
  static async getDocuments(context: Context) {
    const firebaseManager: FirebaseManager = context.get("firebaseManager");
    const documents = await firebaseManager.firestore.getAllUserDocuments();
    return context.json({ message: documents });
  }

  static async uploadDocuments(context: Context) {
    const body = await context.req.parseBody();
    const file = body.file;

    if (!file || !(file instanceof File) || !file.name) {
      return context.json({ error: "Please upload a valid file" }, 400);
    }

    if (!(file instanceof File)) {
      return context.json({ error: "Invalid file" }, 400);
    }

    const fileId = crypto.randomUUID();

    const firebaseManager: FirebaseManager = context.get("firebaseManager");

    const [uploadFileUrl, ocrResult] = await Promise.all([
      firebaseManager.storage.uploadDocument(file, fileId),
      ocrFile(file, context),
    ]);

    if (!uploadFileUrl) {
      return context.json({ error: "Could not upload document" }, 500);
    }

    const strippedOcrText = stripSingleLine(ocrResult);

    const savedDocumentId =
      await firebaseManager.firestore.saveDocumentMetadata(
        file,
        fileId,
        uploadFileUrl,
        strippedOcrText
      );

    if (!savedDocumentId) {
      return context.json({ error: "Could not save document" }, 500);
    }

    return context.json({
      message: "Successfully uploaded document",
      id: savedDocumentId,
    });
  }
}
