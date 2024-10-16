import { Hono } from "hono";
import type { Context } from "hono";
import { getUserByUid } from "../firebase/auth.ts";

export const userRouter = new Hono();

async function getUser(context: Context) {
  const user = await getUserByUid(context.get("user").uid);
  return context.json({ user });
}

userRouter.get("/", getUser);
