import { Hono } from "hono";
import { DocumentService } from "../service/documentService/DocumentService";

export const documentsRouter = new Hono();

documentsRouter.get("/", DocumentService.getDocuments);
documentsRouter.post("/", DocumentService.uploadDocuments);
