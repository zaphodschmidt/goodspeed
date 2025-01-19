//id's are marked as optional with ? since they are assigned by backend and not known until then.

export interface Image {
    id?: number 
    image_url: string;
    uploaded_at: string
}

export interface Building {
    id?: number 
    name: string;
    cameras: Camera[];
}

export interface Camera {
    image?: Image
    building: number; //backend id of associated building
    id?: number //backend id of camera
    cam_num: number; //number in parking garage
    MAC: string; 
    IP: string;
    parking_spots: ParkingSpot[];
}

export interface ParkingSpot {
    id?: number; //id of parking spot in backend
    spot_num: number; //number of parking spot in garage
    occupied: boolean; 
    occupied_by_lpn: string;
    reserved_by_lpn: string
    start_datetime?: string;
    end_datetime?: string;
    camera: number; //backend id of associated camera
    vertices: Vertex[]; 
}

export interface Vertex {
    id?: number; //backend id of Vertex
    spot?: number; //backend id of associated parking spot
    x: number;
    y: number;
}