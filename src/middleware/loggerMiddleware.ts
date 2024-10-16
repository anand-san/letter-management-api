import type { Context, Next } from "hono";

export const loggerMiddleware = async (c: Context, next: Next) => {
  await next();
  console.log(`${c.req.method} ${c.req.url} - ${c.res.status}`);
};
