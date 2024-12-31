//id's are marked as optional with ? since they are assigned by backend and not known until then.

export interface Building {
    id?: number 
    name: string;
    cameras: Camera[];
}

export interface Camera {
    building: number; //backend id of associated building
    id?: number //backend id of camera
    cam_num: number; //number in parking garage
    MAC: string; 
    IP: string;
    parking_spots: ParkingSpot[];
}

export interface ParkingSpot {
    id?: number; //id of parking spot in backend
    camera: number //backend id of associated camera
    spot_num: number; //number of parking spot in garage
    vertices: Vertex[]; 
}

export interface Vertex {
    id?: number; //backend id of Vertex
    spot?: number; //backend id of associated parking spot
    x: number;
    y: number;
}