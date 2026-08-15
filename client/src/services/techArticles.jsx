import axios from "axios";

// Backend URL
const BASE_URL="http://localhost:8000"

const getArticles = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/tech`)  
    return {
      data: response.data,
      status: response.status,
      error: null
    }
  } catch (error) {
    console.log(`getArticles failed: ${error}`)
    return {
      data: null,
      status: error.response.status,
      error: "Request failed"
    }
  }
}

const deleteArticle = async (id) => {
  try {
    const response = await axios.delete(`${BASE_URL}/api/tech/${id}`)  
    return {
      data: response.data,
      status: response.status,
      error: null
    }
  } catch (error) {
    console.log(`deleteArticle failed: ${error}`)
    return {
      data: null,
      status: error.response.status,
      error: "Request failed"
    }
  }
}

export default {
  getArticles,
  deleteArticle
}