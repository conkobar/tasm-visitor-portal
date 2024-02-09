import { checkAuthState, getCurrentDate } from "./authFunctions";
import { checkInput} from "./data_validators";
import { getCollection } from "./firestoreFunctions";

// initialize groupInfo object
let groupInfo = { date: getCurrentDate() };

// update groupInfo when user clicks next button
const updateGroupInfo = () => {
  // grab values from "select" dropdown of field trip groups
  const selectElement = document.getElementById("Group-2");

  // populate data from form
  groupInfo.groupName = selectElement.options[selectElement.selectedIndex].text;
  groupInfo.zip = parseInt(document.getElementById('Group-2').value);
  groupInfo.students = parseInt(document.getElementById('students').value);
  groupInfo.adults = parseInt(document.getElementById('adults').value);
  groupInfo.boys = parseInt(document.getElementById('boys').value);
  groupInfo.girls = parseInt(document.getElementById('girls').value);
  groupInfo.firstGrade = parseInt(document.getElementById('grade-1').value);
  groupInfo.secondGrade = parseInt(document.getElementById('grade-2').value);
  groupInfo.thirdGrade = parseInt(document.getElementById('grade-3').value);
  groupInfo.fourthGrade = parseInt(document.getElementById('grade-4').value);
  groupInfo.fifthGrade = parseInt(document.getElementById('grade-5').value);
  groupInfo.sixthGrade = parseInt(document.getElementById('grade-6').value);
  groupInfo.seventhGrade = parseInt(document.getElementById('grade-7').value);
  groupInfo.eighthGrade = parseInt(document.getElementById('grade-8').value);
  groupInfo.ninthGrade = parseInt(document.getElementById('grade-9').value);
  groupInfo.tenthGrade = parseInt(document.getElementById('grade-10').value);
  groupInfo.eleventhGrade = parseInt(document.getElementById('grade-11').value);
  groupInfo.twelfthGrade = parseInt(document.getElementById('grade-12').value);

  // check input values
  for (let key in groupInfo) {
    // check input if it is a number
    if (typeof groupInfo[key] === 'number') {
      groupInfo[key] = checkInput(groupInfo[key]);
    }
  }

  // check required fields
  if (groupInfo.groupName !== "Select one...") {
    // define properties of groupInfo object
    let visitors = ['students', 'adults', 'boys', 'girls', 'firstGrade', 'secondGrade', 'thirdGrade', 'fourthGrade', 'fifthGrade', 'sixthGrade', 'seventhGrade', 'eighthGrade', 'ninthGrade', 'tenthGrade', 'eleventhGrade', 'twelfthGrade'];

    // calculate sum of groupInfo visitors
    let sum = visitors.reduce((total, property) => total + groupInfo[property], 0);

    if (sum > 0) {
      console.log("The sum of the numbers is more than zero.");

      // store groupInfo object in localStorage
      localStorage.setItem('groupInfo', JSON.stringify(groupInfo));

      // redirect to next page
      window.location.href = './confirmation-page.html';
    } else {
      alert('Please specify the number of visitors.')
    }
  } else {
    alert('Group Name is a required field.');
  }

  // show new groupInfo object in console
  console.log(groupInfo);
};

// listen for next button to be clicked
document.getElementById('group').addEventListener('click', updateGroupInfo);

// check if user is signed in
document.addEventListener('DOMContentLoaded', () => {
  checkAuthState(() => window.location.href = './index.html');
});

// populate groups list from firebase
const populateGroups = () => {
  // get groups from firebase
  const groupsRef = getCollection('schools');
  console.log(groupsRef);

  // Get the select element
  const selectElement = document.getElementById("Group-2");

  // Loop through the array and append options to the select element
  groupsRef.then((groups) => {
    groups.forEach((group) => {
      console.log(group);
      console.log(group.name);
      // Create an option element
      const optionElement = document.createElement("option");

      // Assign text and value to option element
      optionElement.textContent = group.name;
      optionElement.value = group.zip;

      // Append the option element to the select element
      selectElement.appendChild(optionElement);
    });
  });
};

// listen for DOMContentLoaded event
document.addEventListener('DOMContentLoaded', populateGroups);
