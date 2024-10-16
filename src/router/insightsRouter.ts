import { Hono } from "hono";
import { InsightsService } from "../service/insightService/InsightsService";

export const insightsRouter = new Hono();

insightsRouter.get("/", InsightsService.getInsights);
insightsRouter.post("/", InsightsService.createInsights);
