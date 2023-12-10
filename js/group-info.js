// initialize groupInfo object
let groupInfo = {};

// update groupInfo when user clicks next button
const updateGroupInfo = () => {
  groupInfo.name = document.getElementById('Group-2').value;

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
