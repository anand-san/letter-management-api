import { getFirestore, Firestore } from "firebase-admin/firestore";

export class FirebaseFirestoreManager {
  userId: string;
  db: Firestore;

  constructor(userId: string) {
    this.userId = userId;
    this.db = getFirestore();
  }

  async getAllUserDocuments(): Promise<
    Array<{ id: string; data: FirebaseFirestore.DocumentData }>
  > {
    try {
      const documentsSnapshot = await this.db
        .collection("User")
        .doc(this.userId)
        .collection("Documents")
        .select(
          "storedFileName",
          "fileType",
          "originalFileName",
          "fileUrl",
          "uploadedAt"
        )
        .get();

      const documents = documentsSnapshot.docs.map((doc) => ({
        id: doc.id,
        data: doc.data(),
      }));

      return documents;
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to retrieve user documents: ${e.message}`);
      } else {
        throw new Error("Failed to retrieve user documents: Unknown error");
      }
    }
  }

  async saveDocumentMetadata(
    file: File,
    fileId: string,
    filePublicUrl: string,
    ocrData: string
  ): Promise<string> {
    try {
      const docRef = this.db
        .collection("User")
        .doc(this.userId)
        .collection("Documents")
        .doc();
      await docRef.set({
        storedFileName: fileId,
        fileType: file.type,
        originalFileName: file.name,
        fileUrl: filePublicUrl,
        ocrData,
        uploadedAt: new Date().toISOString(),
      });
      return docRef.id;
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to save document: ${e.message}`);
      } else {
        throw new Error("Failed to save document: Unknown error");
      }
    }
  }

  async getDocumentOcrData(documentId: string): Promise<string | null> {
    try {
      const docRef = this.db
        .collection("User")
        .doc(this.userId)
        .collection("Documents")
        .doc(documentId);

      const doc = await docRef.get();

      if (doc.exists) {
        const data = doc.data();
        return data?.ocrData || null;
      } else {
        return null;
      }
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to get document OCR data: ${e.message}`);
      } else {
        throw new Error("Failed to get document OCR data: Unknown error");
      }
    }
  }

  async checkInsightsExist(documentId: string): Promise<boolean> {
    try {
      const insightsSnapshot = await this.db
        .collection("User")
        .doc(this.userId)
        .collection("Insights")
        .where("documentId", "==", documentId)
        .limit(1)
        .get();
      return !insightsSnapshot.empty;
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(
          `Failed to check document insights existence: ${e.message}`
        );
      } else {
        throw new Error(
          "Failed to check document insights existence: Unknown error"
        );
      }
    }
  }

  async saveDocumentInsights(
    documentId: string,
    insights: string
  ): Promise<string> {
    try {
      const insightRef = this.db
        .collection("User")
        .doc(this.userId)
        .collection("Insights")
        .doc();

      await insightRef.set({
        documentId: documentId,
        insights: insights,
        createdAt: new Date().toISOString(),
      });

      return insightRef.id;
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to save document insights: ${e.message}`);
      } else {
        throw new Error("Failed to save document insights: Unknown error");
      }
    }
  }

  async getDocumentInsights(documentId: string): Promise<string | null> {
    try {
      const insightsSnapshot = await this.db
        .collection("User")
        .doc(this.userId)
        .collection("Insights")
        .where("documentId", "==", documentId)
        .limit(1)
        .get();

      if (!insightsSnapshot.empty) {
        const insightDoc = insightsSnapshot.docs[0];
        const data = insightDoc.data();
        return data.insights || null;
      } else {
        return null;
      }
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(`Failed to get document insights: ${e.message}`);
      } else {
        throw new Error("Failed to get document insights: Unknown error");
      }
    }
  }
}
