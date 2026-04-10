import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyC3MGuRFqnPhnt_i435vzm1gQwDRofx8BY",
    authDomain: "mobile-service-7612f.firebaseapp.com",
    projectId: "mobile-service-7612f",
    storageBucket: "mobile-service-7612f.firebasestorage.app",
    messagingSenderId: "1098623185566",
    appId: "1:1098623185566:web:acc76edc9a215c8465818f",
    measurementId: "G-XPZHYBKSEJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// To ensure Recaptcha works without invisible bugs, we often set language or other settings here
auth.useDeviceLanguage();

export { auth };
