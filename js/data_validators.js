// check input for null values
const checkNull = (input) => {
  if (Number.isNaN(input)) return 0;
  return input;
};

// check input for negatives
const checkNegatives = (input) => {
  if (input < 0) return 0;
  return input;
};

// check input for decimals
const checkDecimals = (input) => {
  if (input % 1 !== 0) return 0;
  return input;
};
