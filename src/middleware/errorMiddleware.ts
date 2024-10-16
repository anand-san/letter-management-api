import type { Context, Next } from "hono";

export const errorMiddleware = async (
  _ctx: Context,
  next: Next
): Promise<void> => {
  try {
    await next();
  } catch (err) {
    console.error("Global error:", err);
    throw err;
  }
};
