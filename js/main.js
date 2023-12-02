import { db } from "./firebase.js";
import { collection, getDocs } from "firebase/firestore";

const getCollection = async (collectionName) => {
  try {
    const col = collection(db, collectionName);
    const snapshot = await getDocs(col);
    return snapshot.docs.map((doc) => doc.data());
  } catch (error) {
    console.error(error);
    throw error;
  }
};

getCollection("test")
  .then((data) => console.log(data))
  .catch((error) => console.error(error));
