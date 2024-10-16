import { getStorage, Storage } from "firebase-admin/storage";

export class FirebaseStorageManager {
  userId: string;
  storage: Storage;

  constructor(userId: string) {
    this.userId = userId;
    this.storage = getStorage();
  }

  async uploadDocument(file: File, fileId: string): Promise<string> {
    try {
      const bucket = this.storage.bucket();

      const filePath = `documents/${this.userId}/${fileId}`;
      const fileUpload = bucket.file(filePath);
      const arrayBuffer = await file.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);

      await fileUpload.save(uint8Array, {
        metadata: {
          contentType: file.type,
        },
      });

      return fileUpload.publicUrl();
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to save document: ${e.message}`);
      } else {
        throw new Error("Failed to save document: Unknown error");
      }
    }
  }
}
