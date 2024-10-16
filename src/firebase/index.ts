import { FirebaseFirestoreManager } from "./firebaseFirestore.ts";
import { FirebaseStorageManager } from "./firebaseStorage.ts";

export class FirebaseManager {
  userId: string;
  firestore: FirebaseFirestoreManager;
  storage: FirebaseStorageManager;

  constructor(userId: string) {
    this.userId = userId;
    this.firestore = new FirebaseFirestoreManager(userId);
    this.storage = new FirebaseStorageManager(userId);
  }
}
