import type { Context, Next } from "hono";
import { getAuth } from "firebase-admin/auth";
import { initializeServicesInContext } from "../context";

export const authMiddleware = async (
  context: Context,
  next: Next
): Promise<void> => {
  const authHeader = context.req.header("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    throw new Error("Unauthorized");
  }

  const token = authHeader.split("Bearer ")[1];
  try {
    const auth = getAuth();
    const decodedToken = await auth.verifyIdToken(token);

    context.set("user", decodedToken);
    initializeServicesInContext(context);
    await next();
  } catch (error) {
    console.error("Auth error:", error);
    throw error;
  }
};
