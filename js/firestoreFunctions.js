import { db } from "./firebase.js";
import { addDoc, collection, getDocs } from "firebase/firestore";

// retrieves firebase collection as array of objects
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

// saves to firebase collection an array of objects
const addDocument = async (collectionName, data) => {
  try {
    const col = collection(db, collectionName);
    return await addDoc(col, data);
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export { getCollection, addDocument };
