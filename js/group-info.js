import { checkAuthState, getCurrentDate } from "./authFunctions";

// initialize groupInfo object
let groupInfo = { date: getCurrentDate() };

// update groupInfo when user clicks next button
const updateGroupInfo = () => {
  groupInfo.groupName = document.getElementById('Group-2').value;
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

  // handle zip code (for sake of demo)
  if (groupInfo.groupName === 'First') groupInfo.zip = 74131;
  if (groupInfo.groupName === 'Second') groupInfo.zip = 74135;
  if (groupInfo.groupName === 'Third') groupInfo.zip = 74105;
  if (groupInfo.groupName === 'Fourth') groupInfo.zip = 74107;

  // check null values
  for (let key in groupInfo) {
    if (Number.isNaN(groupInfo[key])) groupInfo[key] = 0;
  }

  // check required fields
  if (groupInfo.name !== '') {
    // store groupInfo object in localStorage
    localStorage.setItem('groupInfo', JSON.stringify(groupInfo));

    // redirect to next page
    window.location.href = './confirmation-page.html';

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
