import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Укажите адрес вашего API
});

export default api;
