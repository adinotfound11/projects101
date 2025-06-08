import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import {
  getAuth, onAuthStateChanged, signOut
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";
import {
  getFirestore, doc, getDoc, updateDoc,
  collection, query, where, getDocs, orderBy
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";
import {
  getStorage, ref, uploadBytes, getDownloadURL
} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-storage.js";

const firebaseConfig = { /* same config */ };
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

const usernameEl = document.getElementById("username");
const fullnameEl = document.getElementById("fullname");
const bioEl = document.getElementById("bio");
const pfpEl = document.getElementById("pfp");
const postsEl = document.getElementById("posts");
const uploadPfp = document.getElementById("upload-pfp");
const savePfp = document.getElementById("save-pfp");
const saveBio = document.getElementById("save-bio");

let currentUser = null;

onAuthStateChanged(auth, async user => {
  if (!user) return window.location.href = "login.html";
  currentUser = user;
  const userRef = doc(db, "user", user.uid);
  const userSnap = await getDoc(userRef);
  if (userSnap.exists()) {
    const data = userSnap.data();
    usernameEl.textContent = `@${data.username}`;
    fullnameEl.textContent = data["full name"] || "No name";
    bioEl.value = data.bio || "";
    if (data.photoURL) pfpEl.src = data.photoURL;
  }
  loadPosts(user.uid);
});

saveBio.addEventListener("click", async () => {
  if (!currentUser) return; 
  const newBio = bioEl.value.trim();
  await updateDoc(doc(db, "user", currentUser.uid), { bio: newBio });
  alert("Bio updated!");
});

savePfp.addEventListener("click", async () => {
  const file = uploadPfp.files[0];
  if (!file || !currentUser) return alert("Select a picture first.");
  const storageRef = ref(storage, `profile_pics/${currentUser.uid}.jpg`);
  await uploadBytes(storageRef, file);
  const url = await getDownloadURL(storageRef);
  await updateDoc(doc(db, "user", currentUser.uid), { photoURL: url });
  pfpEl.src = url;
  alert("Profile picture updated!");
});

async function loadPosts(uid) {
  const q = query(collection(db, "posts"), where("uid", "==", uid), orderBy("timestamp", "desc"));
  const snap = await getDocs(q);
  postsEl.innerHTML = "";
  snap.forEach(doc => {
    const post = doc.data();
    const div = document.createElement("div");
    div.className = "post";
    div.innerHTML = `<div>${post.content}</div><small>${new Date(post.timestamp?.toDate()).toLocaleString()}</small>`;
    postsEl.appendChild(div);
  });
}
