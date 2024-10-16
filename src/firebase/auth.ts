import { getAuth } from "firebase-admin/auth";

export async function getUserByUid(uid: string) {
  try {
    const auth = getAuth();
    const userRecord = await auth.getUser(uid);
    return userRecord.toJSON();
  } catch (error) {
    console.log("Error fetching user data:", error);
    throw error;
  }
}
