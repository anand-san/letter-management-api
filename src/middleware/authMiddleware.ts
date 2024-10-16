import type { Context, Next } from "hono";
import { getAuth } from "firebase-admin/auth";
import { initializeServicesInContext } from "../context.ts";

export const authMiddleware = async (
  context: Context,
  next: Next,
  env: Record<string, string>
) => {
  const authHeader = context.req.header("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return context.json({ error: "Unauthorized" }, 401);
  }

  const token = authHeader.split("Bearer ")[1];
  try {
    const auth = getAuth();
    const decodedToken = await auth.verifyIdToken(token);
    // setup context

    context.set("user", decodedToken);
    context.set("env", env);
    initializeServicesInContext(context);
    await next();
  } catch (error) {
    console.error("Auth error:", error);
    return context.json({ error: "Invalid token" }, 401);
  }
};
