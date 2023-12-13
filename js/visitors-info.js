import { checkAuthState } from "./authFunctions";

// new visitors test info object
let visitorsInfo = {};

// get the current date
visitorsInfo.date = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();

  return `${year}-${month}-${day}`;
};

// function to update visitorsInfo object
const updateVisitorsInfo = () => {
  visitorsInfo.name = document.getElementById('name').value,
  visitorsInfo.zip = parseInt(document.getElementById('zip').value),
  visitorsInfo.kid = parseInt(document.getElementById('kid').value),
  visitorsInfo.student = parseInt(document.getElementById('student').value),
  visitorsInfo.adult = parseInt(document.getElementById('adult').value),
  visitorsInfo.senior = parseInt(document.getElementById('senior').value);

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
document.addEventListener('DOMContentLoaded', checkAuthState);
