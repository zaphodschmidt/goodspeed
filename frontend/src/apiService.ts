// authUtils.ts
import axios, { AxiosRequestHeaders } from 'axios';

export const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

export function getAuthHeaders(): AxiosRequestHeaders['headers'] {
    const token = localStorage.getItem('access_token');
    if (!token) {
        throw new Error('No access token available');
    }
    return {
        Authorization: `Bearer ${token}`,
    };
}

export async function getBuildings() {
    console.log(API_BASE_URL)
    const response = await axios.get(`${API_BASE_URL}/api/buildings`, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Network response was not ok');
    }
    console.log(response.data)
    return response.data;
}