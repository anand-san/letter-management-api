import type { Context, Next } from "hono";

export const timingMiddleware = async (c: Context, next: Next) => {
  const start = Date.now();
  const ms = Date.now() - start;
  c.res.headers.set("X-Response-Time", `${ms}ms`);
  await next();
};
