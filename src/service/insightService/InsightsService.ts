import { FirebaseManager } from "./../../firebase/index.ts";
import type { Context } from "hono";
import { LLMAssistant } from "../../service/openAI/OpenAiManager.ts";

export class InsightsService {
  static async getInsights(context: Context) {
    const documentId = context.req.query("documentId");

    if (!documentId) {
      return context.json(
        { error: "documentId is required in the query string" },
        400
      );
    }

    const firebaseManager: FirebaseManager = context.get("firebaseManager");

    const insights = await firebaseManager.firestore.getDocumentInsights(
      documentId
    );

    return context.json({ message: insights });
  }

  // Define the createInsights function
  static createInsights = async (ctx: Context) => {
    try {
      const documentId = ctx.req.query("documentId");

      if (!documentId) {
        return ctx.json(
          { error: "documentId is required in the query string" },
          400
        );
      }

      const user_id = ctx.get("user_id");

      const firebaseManager: FirebaseManager = ctx.get("firebaseManager");

      const insightExists = await firebaseManager.firestore.checkInsightsExist(
        documentId
      );

      if (insightExists) {
        return ctx.json(
          {
            message:
              "Insight for the provided document already exist, Delete the document and re-upload to generate new insighta",
          },
          200
        );
      }

      await firebaseManager.firestore
        .getDocumentOcrData(documentId)
        .then((documentOcr) => {
          if (!documentOcr) {
            return ctx.json(
              { error: "Cound not extract text from the document mentioned" },
              404
            );
          }
          const llm = new LLMAssistant(user_id, ctx);
          llm
            .retrieveInsightsFromAssistant(documentOcr)
            .then((documentInsights) => {
              firebaseManager.firestore.saveDocumentInsights(
                documentId,
                documentInsights
              );
            });
        });

      return ctx.json({ message: "Processing" }, 201);
    } catch (error) {
      console.error("Error creating insights:", error);
      return ctx.json({ error: "Internal Server Error" }, 500);
    }
  };
}
