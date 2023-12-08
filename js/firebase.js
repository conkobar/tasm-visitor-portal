// Import the functions you need from the SDKs you need
import "regenerator-runtime/runtime";
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
require('dotenv').config();
// import { getAnalytics } from "firebase/analytics";

if (typeof global === 'undefined') {
  var global = window;
}

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
// const firebaseConfig = {
//   apiKey: "AIzaSyAdnD44dd-Fg3pT9Dj3WFbI9ufRvUVA4Qo",
//   authDomain: "tasm-visitor-signin.firebaseapp.com",
//   projectId: "tasm-visitor-signin",
//   storageBucket: "tasm-visitor-signin.appspot.com",
//   messagingSenderId: "720433299143",
//   appId: "1:720433299143:web:9c46a8d5edc434a63848e2",
//   measurementId: "G-2EQ86NZ0JQ"
// };
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER,
  appId: process.env.FIREBASE_APP_ID,
  measurementId: process.env.FIREBASE_MEASUREMENT_ID
};

const testEnv = () => {
  console.log('Firebase API Key:', process.env.FIREBASE_API_KEY);
  console.log('Firebase Auth Domain:', process.env.FIREBASE_AUTH_DOMAIN);
  console.log('Firebase Project ID:', process.env.FIREBASE_PROJECT_ID);
  console.log('Firebase Storage Bucket:', process.env.FIREBASE_STORAGE_BUCKET);
  console.log('Firebase Messaging Sender ID:', process.env.FIREBASE_MESSAGING_SENDER_ID);
  console.log('Firebase App ID:', process.env.FIREBASE_APP_ID);
  console.log('Firebase Measurement ID:', process.env.FIREBASE_MEASUREMENT_ID);
}

testEnv();

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getFirestore(app);

export { db };
