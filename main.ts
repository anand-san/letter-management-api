import { Hono, type Context, type Next } from "hono";
import { serve } from "std/http/server.ts";
import router from "./src/router/appRouter.ts";
import env, { Env } from "./env.ts";
import { initializeFirebaseAppAdmin } from "./src/firebase.ts";
import "./src/firebase.ts";

// Import Middlewares
import { authMiddleware } from "./src/middleware/authMiddleware.ts";
import { loggerMiddleware } from "./src/middleware/loggerMiddleware.ts";
import { timingMiddleware } from "./src/middleware/timingMiddleware.ts";
import { errorMiddleware } from "./src/middleware/errorMiddleware.ts";

const withEnv =
  (
    middleware: (c: Context, next: Next) => Promise<Response | void | undefined>
  ) =>
  async (c: Context<{ Bindings: Env }>, next: Next) => {
    c.env = env;
    return await middleware(c, next);
  };

const main = async () => {
  try {
    const serviceAccount = JSON.parse(env.FIREBASE_SERVICE_ACCOUNT);
    const storageBucket = env.FIREBASE_STORAGE_BUCKET;
    initializeFirebaseAppAdmin(serviceAccount, storageBucket);

    const port = parseInt(env.PORT) || 0;
    const app = new Hono<{ Bindings: Env }>();

    // Middlewares
    app.use("/*", withEnv(loggerMiddleware));
    app.use("/*", withEnv(timingMiddleware));
    app.use("/*", withEnv(errorMiddleware));
    app.use("/*", withEnv(authMiddleware));

    // Router
    app.route("/", router);

    console.log(`Server is running on http://localhost:${port}`);

    await serve(app.fetch, { port });
  } catch (e) {
    console.log(e);
  }
};

main();
