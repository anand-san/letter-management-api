import type { Context, Next } from "hono";

export const loggerMiddleware = async (c: Context, next: Next) => {
  console.log(`${c.req.method} ${c.req.url} - ${c.res.status}`);
  await next();
};
