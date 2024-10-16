import { FirebaseManager } from "./../../firebase/index";
import type { Context } from "hono";
import { LLMAssistant } from "../../service/openAI/OpenAiManager";

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

      const insightId = await this.processInsights(documentId, user_id, ctx);

      return ctx.json({ message: "Successful", id: insightId }, 202);
    } catch (error) {
      console.error("Error creating insights:", error);
      return ctx.json({ error: "Internal Server Error" }, 500);
    }
  };

  private static async processInsights(
    documentId: string,
    user_id: string,
    ctx: Context
  ) {
    try {
      const firebaseManager: FirebaseManager = ctx.get("firebaseManager");

      const documentOcr = await firebaseManager.firestore.getDocumentOcrData(
        documentId
      );
      if (!documentOcr) {
        console.error("Could not extract text from the document mentioned");
        return;
      }

      const llm = new LLMAssistant(user_id, ctx);
      const documentInsights = await llm.retrieveInsightsFromAssistant(
        documentOcr
      );

      await firebaseManager.firestore.saveDocumentInsights(
        documentId,
        documentInsights
      );

      console.log("Insights processing completed successfully");
    } catch (error) {
      console.error("Error processing insights in the background:", error);
    }
  }
}
