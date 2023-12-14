import { checkAuthState, getCurrentDate } from "./authFunctions";

// new visitors test info object
let visitorsInfo = { date: getCurrentDate() };

// function to update visitorsInfo object
const updateVisitorsInfo = () => {
  visitorsInfo.name = document.getElementById('name').value,
  visitorsInfo.zip = parseInt(document.getElementById('zip').value),
  visitorsInfo.kids = parseInt(document.getElementById('kid').value),
  visitorsInfo.students = parseInt(document.getElementById('student').value),
  visitorsInfo.adults = parseInt(document.getElementById('adult').value),
  visitorsInfo.seniors = parseInt(document.getElementById('senior').value);

  // check required fields
  if (visitorsInfo.name && visitorsInfo.zip) {
    // store visitorsInfo object in localStorage
    localStorage.setItem('visitorsInfo', JSON.stringify(visitorsInfo));

    // redirect to next page
    window.location.href = './optional-info.html';
  } else {
    alert('Name and Zip Code are required fields.');
  }

  // show new visitorsInfo object in console
  console.log(visitorsInfo);
};

// listen for click on next button
document.getElementById('next').addEventListener('click', updateVisitorsInfo);

// check if user is signed in
document.addEventListener('DOMContentLoaded', () => {
  checkAuthState(() => window.location.href = './index.html');
});
