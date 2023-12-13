import { getCollection } from "./firestoreFunctions.js";

// test getCollection and addDocument
getCollection("test")
  .then((data) => console.log(data))
  .catch((error) => console.error(error));
