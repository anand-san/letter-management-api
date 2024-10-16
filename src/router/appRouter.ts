import { Hono } from "hono";
import { userRouter } from "./userRouter.ts";
import { documentsRouter } from "./documentsRouter.ts";
import { insightsRouter } from "./insightsRouter.ts";

const router = new Hono();

router.get("/", (c) => c.text("Hello, World!"));

router.route("/user", userRouter);
router.route("/insights", insightsRouter);
router.route("/documents", documentsRouter);

export default router;
