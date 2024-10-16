import type { Context } from "hono";
import { FirebaseManager } from "./firebase/index";

export const initializeServicesInContext = (context: Context) => {
  try {
    const userId = context.get("user").uid;
    const firebaseManager = new FirebaseManager(userId);

    context.set("firebaseManager", firebaseManager);
  } catch {
    console.log("Error occured while initializing services to context");
  }
};
