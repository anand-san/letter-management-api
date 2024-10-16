import { initializeApp, cert, getApps } from "firebase-admin/app";

export const initializeFirebaseAppAdmin = (
  serviceAccount: Record<string, string>,
  storageBucket: string
) => {
  try {
    const apps = getApps();

    if (apps.length === 0) {
      initializeApp({
        credential: cert(serviceAccount),
        storageBucket: storageBucket,
      });
      console.log("Firebase app initialized.");
    } else {
      console.log("Firebase app already initialized.");
    }
  } catch (e) {
    console.log(e);
    throw "failed to initialise Firebase app";
  }
};

export const getFirebaseApp = () => {
  const apps = getApps();
  if (apps.length === 0) {
    throw new Error("Firebase app not initialized.");
  }
  return apps[0];
};
