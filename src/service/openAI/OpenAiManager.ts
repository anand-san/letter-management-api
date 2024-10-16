import type { Context } from "hono";
// import { FirebaseManager } from "../../firebase/index";
import path from "path";
import fs from "fs/promises";
import OpenAI from "openai";

export class LLMAssistant {
  // private userId: string;
  // private firebaseManager: FirebaseManager;
  private openai: OpenAI;
  private openaiModel: string;

  constructor(_userId: string, context: Context) {
    // this.userId = userId;
    // this.firebaseManager = new FirebaseManager(this.userId);
    this.openaiModel = context.env.OPENAI_MODEL;
    this.openai = new OpenAI({ apiKey: context.env.OPENAI_API_KEY });
  }

  private _loadFileTemplate = async (filename: string): Promise<string> => {
    try {
      const filePath = path.join("templates", filename);
      const promptText = await fs.readFile(filePath, "utf-8");
      return promptText;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") {
        throw new Error(`Template file "${filename}" not found`);
      }
      console.error("Error reading template file:", error);
      throw new Error(`Failed to load template file "${filename}"`);
    }
  };

  private async _gatherInsightsFromLlm(
    systemMessage: string,
    userMessage: string
  ): Promise<Record<string, string>> {
    const completion = await this.openai.chat.completions.create({
      model: this.openaiModel,
      messages: [
        {
          role: "system",
          content: [
            {
              type: "text",
              text: systemMessage,
            },
          ],
        },
        {
          role: "user",
          content: [
            {
              type: "text",
              text: userMessage,
            },
          ],
        },
      ],
      temperature: 0.5,
      max_tokens: 8000,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
      response_format: {
        type: "json_object",
      },
    });
    const llmResponse = completion.choices[0].message;

    // const tokenUsage = completion.usage;

    // await this.firestoreManager.saveUserTokenUsage(tokenUsage);

    return JSON.parse(llmResponse.content || "{}");
  }

  async retrieveInsightsFromAssistant(
    documentText: string
  ): Promise<Record<string, string>> {
    try {
      const promptText = await this._loadFileTemplate("insights_prompt.txt");
      return await this._gatherInsightsFromLlm(promptText, documentText);
    } catch (e) {
      throw e;
    }
  }
}
