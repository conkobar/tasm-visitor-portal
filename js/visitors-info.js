// new visitors test info
let visitorsInfo = {};

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
  }

  // show new visitorsInfo object in console
  console.log(visitorsInfo);
};

// listen for click on next button
document.getElementById('next').addEventListener('click', updateVisitorsInfo);
