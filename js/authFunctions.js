import { auth } from './firebase';
import { signInWithEmailAndPassword, onAuthStateChanged, signOut } from 'firebase/auth';

const signIn = async (email, password) => {
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log('user', user);
      document.getElementById('sign-in-form').style.display = 'none';
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
const checkAuthState = (callback) => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log(`User ${user.uid} is signed in`);
    } else {
      console.log('User is not signed in');
      // Ensure the callback is a function before calling it
      if (typeof callback === 'function') {
        callback();
      }
    }
  });
};

// checks if firebase user is signed in with false callback
const checkAuthStateFalse = (callback) => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log(`User ${user.uid} is signed in`);
      // Ensure the callback is a function before calling it
      if (typeof callback === 'function') {
        callback();
      }
    } else {
      console.log('User is not signed in');
    }
  });
};

export { signIn, signOutUser, checkAuthState, checkAuthStateFalse };
