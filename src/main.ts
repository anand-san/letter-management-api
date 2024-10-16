import { Context, Hono, Next } from "hono";
import { serve } from "@hono/node-server";
import router from "./router/appRouter";
import env from "./env";
import { initializeFirebaseAppAdmin } from "./firebase";
import "./firebase";

import { authMiddleware } from "./middleware/authMiddleware";
import { loggerMiddleware } from "./middleware/loggerMiddleware";
import { timingMiddleware } from "./middleware/timingMiddleware";
import { errorMiddleware } from "./middleware/errorMiddleware";

const withEnv = (
  middleware: (c: Context, next: Next) => Promise<Response | void | undefined>
) => {
  return async (c: Context, next: Next) => {
    c.env = env;
    return await middleware(c, next);
  };
};

const main = async () => {
  try {
    const serviceAccount = env.FIREBASE_SERVICE_ACCOUNT;

    const serviceAccountKey = JSON.parse(serviceAccount);
    serviceAccountKey.private_key = serviceAccountKey.private_key.replace(
      /\\n/g,
      "\n"
    );

    const storageBucket = env.FIREBASE_STORAGE_BUCKET;
    initializeFirebaseAppAdmin(serviceAccountKey, storageBucket);

    const port = parseInt(env.PORT) || 0;
    const app = new Hono();

    // Middlewares
    app.use("/*", withEnv(loggerMiddleware));
    app.use("/*", withEnv(timingMiddleware));
    app.use("/*", withEnv(errorMiddleware));
    app.use("/*", withEnv(authMiddleware));

    // Router
    app.route("/", router);

    console.log(`Server is running on http://localhost:${port}`);

    serve({
      fetch: app.fetch,
      port: port,
    });
  } catch (e) {
    console.log(e);
  }
};

main();
