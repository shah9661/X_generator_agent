import axios from "axios"

const BASE_URL = "http://localhost:8000"

export async function generateTweet(topic, maxIteration = 3) {
  const response = await axios.post(`${BASE_URL}/generate-tweet`, {
    topic,
    max_iteration: maxIteration,
  })
  return response.data
}

export async function getHistory(limit = 10) {
  const response = await axios.get(`${BASE_URL}/history?limit=${limit}`)
  return response.data
}

export async function checkHealth() {
  const response = await axios.get(`${BASE_URL}/health`)
  return response.data
}