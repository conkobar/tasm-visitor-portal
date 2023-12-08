import { getCollection, addDocument } from "./firestoreFunctions.js";

if (typeof global === 'undefined') {
  var global = window;
}


// test getCollection and addDocument
getCollection("test")
  .then((data) => console.log(data))
  .catch((error) => console.error(error));

// const testData = {
//   name: "buzz",
//   goal: "test",
//   money: false,
//   hoes: false,
//   sillyGoose: true,
//   date: new Date()
// };
// addDocument("test", testData)
//   .then((data) => console.log(data))
//   .catch((error) => console.error(error));
