// main.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyB5legh47kKcRPzWtg_Sii6x141YaSFXJw",
    authDomain: "prabal-login.firebaseapp.com",
    projectId: "prabal-login",
    storageBucket: "prabal-login.firebasestorage.app",
    messagingSenderId: "646848831374",
    appId: "1:646848831374:web:f2f86b3876ba103ac38edf"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth();

window.loginUser = function () {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // ✅ Send email to Flask backend
      fetch("/set_user", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `email=${encodeURIComponent(email)}`,
      }).then(() => {
        window.location.href = "/";
      });
    })
    .catch((error) => {
      alert("Login failed: " + error.message);
    });
};

window.registerUser = function () {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Send email to Flask backend
      fetch("/set_user", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `email=${encodeURIComponent(email)}`,
      }).then(() => {
        window.location.href = "/";
      });
    })
    .catch((error) => {
      alert("Registration failed: " + error.message);
    });
};
