import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/';

const api = axios.create({
    baseURL,
    withCredentials: true, // This is crucial for sending/receiving HttpOnly cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
