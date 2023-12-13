import { auth } from './firebase';
import { signInWithEmailAndPassword, onAuthStateChanged, signOut } from 'firebase/auth';

const signIn = async (email, password) => {
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log('user', user);
      document.getElementById('sign-in-box').style.display = 'none';
    })
    .catch((error) => {
      console.log(`${error.code}: ${error.message})`);
    });
};

const signOutUser = async () => {
  try {
    await signOut(auth);
  } catch (error) {
    console.error(error);
  }
};

// checks if firebase user is signed in
const checkAuthState = () => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log(`User ${user.uid} is signed in`);
    } else {
      window.location.href = './index.html';
      console.log('user is not signed in');
    }
  });
};

export { signIn, signOutUser, checkAuthState };
