const functions = require("firebase-functions");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

exports.createUserWithDefault = functions.https.onCall(async (data, context) => {
  const { email, role } = data;
  const defaultPassword = "ChangeMe123!";

  // Only systemAdmin or coordinator allowed
  const creatorRole = context.auth?.token.role;
  if (!creatorRole || (
      creatorRole !== "systemAdmin" &&
      creatorRole !== "coordinator"
  )) {
    throw new functions.https.HttpsError("permission-denied", "Not authorized");
  }

  if (creatorRole === "coordinator" && role === "systemAdmin") {
    throw new functions.https.HttpsError("permission-denied", "Coordinators can't create system admins");
  }
  if (creatorRole === "counselor" && role !== "student") {
    throw new functions.https.HttpsError("permission-denied", "Counselors can only create students");
  }

  try {
    const userRecord = await admin.auth().createUser({ email, password: defaultPassword });
    await admin.auth().setCustomUserClaims(userRecord.uid, { role });
    await db.collection("users").doc(email).set({ email, role, firstLogin: true });
    return { success: true, password: defaultPassword };
  } catch (err) {
    throw new functions.https.HttpsError("internal", err.message);
  }
});
exports.updateUserRole = functions.https.onCall(async (data, context) => {
  const { email, newRole } = data;

  // Only systemAdmin or coordinator allowed
  const creatorRole = context.auth?.token.role;
  if (!creatorRole || (
      creatorRole !== "systemAdmin" &&
      creatorRole !== "coordinator"
  )) {
    throw new functions.https.HttpsError("permission-denied", "Not authorized");
  }

  if (creatorRole === "coordinator" && newRole === "systemAdmin") {
    throw new functions.https.HttpsError("permission-denied", "Coordinators can't update to system admin");
  }
  if (creatorRole === "counselor" && newRole !== "student") {
    throw new functions.https.HttpsError("permission-denied", "Counselors can only update to student");
  }

  try {
    const userRecord = await admin.auth().getUserByEmail(email);
    await admin.auth().setCustomUserClaims(userRecord.uid, { role: newRole });
    await db.collection("users").doc(email).update({ role: newRole });
    return { success: true };
  } catch (err) {
    throw new functions.https.HttpsError("internal", err.message);
  }
});