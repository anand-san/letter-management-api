import { Hono } from "hono";
import { serve } from "std/http/server.ts";
import router from "./src/router/appRouter.ts";
import { loadSync } from "std/dotenv/mod.ts";
import { initializeFirebaseAppAdmin } from "./src/firebase.ts";
import "./src/firebase.ts";

// Import Middlewares
import { authMiddleware } from "./src/middleware/authMiddleware.ts";
import { loggerMiddleware } from "./src/middleware/loggerMiddleware.ts";
import { timingMiddleware } from "./src/middleware/timingMiddleware.ts";
import { errorMiddleware } from "./src/middleware/errorMiddleware.ts";

const main = async () => {
  try {
    const env = loadSync();
    const serviceAccount = env.FIREBASE_SERVICE_ACCOUNT;
    const storageBucket = env.FIREBASE_STORAGE_BUCKET;
    initializeFirebaseAppAdmin(serviceAccount, storageBucket);

    const port = parseInt(env.PORT) || 0;
    const app = new Hono();

    // Middlewares
    app.use("/*", loggerMiddleware);
    app.use("/*", timingMiddleware);
    app.use("/*", errorMiddleware);
    app.use("/*", (ctx, next) => authMiddleware(ctx, next, env));

    // Router
    app.route("/", router);

    console.log(`Server is running on http://localhost:${port}`);

    await serve(app.fetch, { port });
  } catch (e) {
    console.log(e);
  }
};

main();
