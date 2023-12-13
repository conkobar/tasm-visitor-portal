import {signIn, signOutUser, checkAuthStateFalse, checkAuthState} from "./authFunctions";

document.getElementById("sign-in-btn").addEventListener("click", () => {
  const email = document.getElementById("sign-in-email").value;
  const password = document.getElementById("sign-in-password").value;

  signIn(email, password)
    .then(() => console.log("signed in"))
    .catch(e => console.error(e));
});

document.getElementById("sign-out-btn").addEventListener("click", () => {
  signOutUser()
    .then(() => console.log("signed out"))
    .catch(e => console.error(e));
});

// check if user is signed in
document.addEventListener('DOMContentLoaded', () => {
  checkAuthState(() => document.getElementById('sign-in-form').style.display = 'flex');
});
