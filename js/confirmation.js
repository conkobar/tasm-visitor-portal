import { addDocument } from "./firestoreFunctions";
import { checkAuthState } from "./authFunctions";

// pushes local data to fb
const confirmData = async () => {
  let visitorsInfo = JSON.parse(localStorage.getItem('visitorsInfo'));
  let groupInfo = JSON.parse(localStorage.getItem('groupInfo'));

  if (visitorsInfo) {
    try {
      await addDocument('visitors', visitorsInfo);
      console.log('visitorsInfo added to firestore');
    } catch (error) {
      console.error(error);
    }
  }

  if (groupInfo) {
    try {
      await addDocument('groups', groupInfo);
      console.log('groupInfo added to firestore');
    } catch (error) {
      console.error(error);
    }
  }

  localStorage.clear();
};

// confirm local storage data
if (window.location.pathname === '/confirmation-page.html') {
  confirmData()
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

// check if user is signed in
document.addEventListener('DOMContentLoaded', checkAuthState);
