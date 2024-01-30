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

// check for common input errors
const checkInput = (input) => {
  input = checkNull(input);
  input = checkNegatives(input);
  input = checkDecimals(input);
  return input;
}

export { checkInput, checkNull, checkNegatives, checkDecimals };
