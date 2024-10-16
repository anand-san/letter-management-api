import type { Context, Next } from "hono";

export const errorMiddleware = async (c: Context, next: Next) => {
  try {
    await next();
  } catch (err) {
    console.error("Global error:", err);
    return c.json({ error: "Internal Server Error" }, 500);
  }
};
