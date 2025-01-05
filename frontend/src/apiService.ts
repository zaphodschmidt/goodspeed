import axios, { AxiosRequestHeaders } from 'axios';
import { Camera, ParkingSpot, Vertex } from './types';

export const API_BASE_URL = 'https://goodspeedbackend.fly.dev'//import.meta.env.VITE_BACKEND_URL;

export function getAuthHeaders(): AxiosRequestHeaders['headers'] {
    const token = localStorage.getItem('access_token');
    if (!token) {
        throw new Error('No access token available');
    }
    return {
        Authorization: `Bearer ${token}`,
    };
}

// Get buildings which contain information for all cameras, parking spots, and vertices
export async function getBuildings() {
    const response = await axios.get(`${API_BASE_URL}/api/buildings`, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Could not get building data.');
    }
    return response.data;
}

// Create/Update/Delete for cameras
const CAMERAS_URL = `${API_BASE_URL}/api/cameras`;

export async function getCameraByID(id: number) {
    const response = await axios.get(`${CAMERAS_URL}/${id}/`, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Could not get camera by id.');
    }
    return response.data;
}

export async function createCamera(camera: Camera) {
    const response = await axios.post(`${CAMERAS_URL}`, camera, { withCredentials: true });
    if (response.status !== 201) {
        throw new Error('Failed to create camera');
    }
}

export async function updateCamera(camera: Camera) {
    if (!camera.id) {
        throw new Error('Cannot update a camera that does not have an id.');
    }
    const response = await axios.put(`${CAMERAS_URL}${camera.id}/`, camera, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Failed to update camera');
    }
}

export async function deleteCamera(camera: Camera) {
    if (!camera.id) {
        throw new Error('Cannot delete a camera that does not have an id.');
    }
    const response = await axios.delete(`${CAMERAS_URL}${camera.id}/`, { withCredentials: true });
    if (response.status !== 204) {
        throw new Error('Failed to delete camera');
    }
}

// Create/Update/Delete for parking spots
const PARKING_SPOTS_URL = `${API_BASE_URL}/api/parking_spots`;

export async function createParkingSpot(spot: ParkingSpot) {
    const response = await axios.post(`${PARKING_SPOTS_URL}/`, spot, { withCredentials: true });
    if (response.status !== 201) {
        throw new Error('Failed to create parking spot');
    }
    return response.data;
}

export async function updateParkingSpot(spot: ParkingSpot) {
    if (!spot.id) {
        throw new Error('Cannot update a parking spot that does not have an id.');
    }
    const response = await axios.put(`${PARKING_SPOTS_URL}/${spot.id}/`, spot, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Failed to update parking spot');
    }
}

export async function deleteParkingSpot(spot: ParkingSpot) {
    if (!spot.id) {
        throw new Error('Cannot delete a parking spot that does not have an id.');
    }
    const response = await axios.delete(`${PARKING_SPOTS_URL}/${spot.id}/`, { withCredentials: true });
    if (response.status !== 204) {
        throw new Error('Failed to delete parking spot');
    }
}

// Create/Update/Delete for vertices
const VERTICES_URL = `${API_BASE_URL}/api/vertices`;

export async function createVertex(vertex: Vertex) {
    const response = await axios.post(`${VERTICES_URL}`, vertex, { withCredentials: true });
    if (response.status !== 201) {
        throw new Error('Failed to create vertex');
    }
}

export async function updateVertex(vertex: Vertex) {
    if (!vertex.id) {
        throw new Error('Cannot update a vertex that does not have an id.');
    }
    const response = await axios.put(`${VERTICES_URL}/${vertex.id}/`, vertex, { withCredentials: true });
    if (response.status !== 200) {
        throw new Error('Failed to update vertex');
    }
}

export async function deleteVertex(vertex: Vertex) {
    if (!vertex.id) {
        throw new Error('Cannot delete a vertex that does not have an id.');
    }
    const response = await axios.delete(`${VERTICES_URL}/${vertex.id}/`, { withCredentials: true });
    if (response.status !== 204) {
        throw new Error('Failed to delete vertex');
    }
}
