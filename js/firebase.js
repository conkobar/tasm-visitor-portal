// Import the functions you need from the SDKs you need
import "regenerator-runtime/runtime";
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// import { getAnalytics } from "firebase/analytics";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAdnD44dd-Fg3pT9Dj3WFbI9ufRvUVA4Qo",
  authDomain: "tasm-visitor-signin.firebaseapp.com",
  projectId: "tasm-visitor-signin",
  storageBucket: "tasm-visitor-signin.appspot.com",
  messagingSenderId: "720433299143",
  appId: "1:720433299143:web:9c46a8d5edc434a63848e2",
  measurementId: "G-2EQ86NZ0JQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getFirestore(app);

export { db };
