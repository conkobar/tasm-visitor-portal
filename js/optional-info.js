import { checkAuthState } from "./authFunctions";


// get the visitors info from local storage
let visitorsInfo = JSON.parse(localStorage.getItem('visitorsInfo'));

console.log(visitorsInfo);

// function to update visitorsInfo object with optional info
const updateOptionalInfo = () => {
  visitorsInfo.membership = document.getElementById('radio').checked;
  visitorsInfo.email = document.getElementById('email-2').value;
  visitorsInfo.website = document.getElementById('checkbox').checked,
  visitorsInfo.facebook = document.getElementById('checkbox-6').checked,
  visitorsInfo.instagram = document.getElementById('checkbox-5').checked,
  visitorsInfo.twitter = document.getElementById('checkbox-4').checked,
  visitorsInfo.linkedin = document.getElementById('checkbox-3').checked,
  visitorsInfo.other = document.getElementById('checkbox-2').checked

  // check required fields
  if (document.getElementById('radio').checked || document.getElementById('radio-2').checked) {
    // store visitorsInfo object in localStorage
    localStorage.setItem('visitorsInfo', JSON.stringify(visitorsInfo));

    // redirect to next page
    window.location.href = './confirmation-page.html';
  } else {
    alert('Please specify if you are a member.');
  }

  // show new visitorsInfo object in console
  console.log(visitorsInfo);
};

// listen for click on submit button
document.getElementById('submit').addEventListener('click', updateOptionalInfo);

// check if user is signed in
document.addEventListener('DOMContentLoaded', () => {
  checkAuthState(() => window.location.href = './index.html');
});
