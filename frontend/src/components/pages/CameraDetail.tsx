import { useRef, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Building, Camera, ParkingSpot, Vertex } from "../../types.ts";
import {
  Button,
  Flex,
  AspectRatio,
  BackgroundImage,
  Group,
  Loader,
} from "@mantine/core";
import no_image from "../../assets/no_image.jpeg";
import { generateSlug } from "../misc/generateSlug.ts";
import { createParkingSpot, deleteParkingSpot, getCameraByID, updateParkingSpot } from "../../apiService.ts";
import SpotPolygon from "../spotComponents/SpotPolygon.tsx";
import SpotTable from "../spotComponents/SpotTable.tsx";
import { useBuildings } from "../misc/useBuildingsContext.ts";


function CameraDetail() {

  const { buildingSlug, camNum } = useParams<{
    buildingSlug: string;
    camNum: string;
  }>();
  
  const { buildings } = useBuildings()
  
  const building: Building | undefined = (buildings.find((b) => generateSlug(b.name) === buildingSlug));
  const camera_id = (building?.cameras.find((c) => c.cam_num === Number(camNum)))?.id || undefined
  const [camera, setCamera] = useState<Camera | undefined>()
  const [spots, setSpots] = useState<ParkingSpot[]>([])

  // Reference to the BackgroundImage to get its dimensions
  const imageRef = useRef<HTMLDivElement>(null);

  // Update the image dimensions when the component mounts, and fetch updated camera data.
  useEffect(() => {
    if (camera_id) {
      getCameraByID(camera_id).then((fetched_cam: Camera) => {
        setCamera(fetched_cam)
        setSpots(fetched_cam.parking_spots)
        console.log(fetched_cam.parking_spots)
      })
    }
  }, [camera_id]);

  const deleteAllSpots = () => {
    for (const parking_spot of spots) {
      deleteParkingSpot(parking_spot)
    }
    setSpots([])
  }

  const deleteSpot = (spotToDelete: ParkingSpot) => {
    deleteParkingSpot(spotToDelete)
    setSpots(spots.filter((spot) => spot.id !== spotToDelete.id))
  }

  const AddNewSpot = (camera: Camera) => {
    const rect = imageRef.current!.getBoundingClientRect();
    const imageSize = { width: rect.width, height: rect.height };
    const spotNum = spots.length;

    const vertices: Vertex[] = [
      { x: Math.round(imageSize.width * 0.25), y: Math.round(imageSize.height * 0.25) },
      { x: Math.round(imageSize.width * 0.75), y: Math.round(imageSize.height * 0.25) },
      { x: Math.round(imageSize.width * 0.75), y: Math.round(imageSize.height * 0.75) },
      { x: Math.round(imageSize.width * 0.25), y: Math.round(imageSize.height * 0.75) },
    ];

    const newSpot: ParkingSpot = {
      camera: camera.id!,
      spot_num: spotNum,
      vertices,
    };
    console.log("newSpot:", newSpot)
    createParkingSpot(newSpot)
      .then((createdSpot) => {
        console.log("Parking spot created", createdSpot);
        setSpots([...spots, createdSpot])
      })
      .catch((error) => {
        console.error("Error in creating parking spot", error);
      });

  }

  const handleUpdateSpot = async (updatedSpot: ParkingSpot) => {
    await updateParkingSpot(updatedSpot)
    setSpots(spots.map((spot) => spot.id === updatedSpot.id ? updatedSpot : spot))
  }

  if (!building || !camera) {
    return <Loader />
  }

  return (
    <div>
      <AspectRatio
        maw={1000}
        mx="auto"
        pos='relative'
        ratio={4 / 3}
      >
        <BackgroundImage
          ref={imageRef}
          src={camera.image?.image_url || no_image}
          style={{
            position: 'relative',
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        >
          {spots.length > 0 &&
            spots.map((spot, index) => (
              <SpotPolygon
                key={spot.id}
                parking_spot={spot}
                colorKey={index}
                deleteSpot={deleteSpot}
                handleUpdateSpot={handleUpdateSpot}
              />
            ))}
        </BackgroundImage>
      </AspectRatio>
      <Flex align="center" justify="center" mt="lg">
        <Group>
          <Button onClick={() => AddNewSpot(camera)}>Add Spot To Camera</Button>
          <Button onClick={deleteAllSpots}>Delete All Spots From Camera</Button>
        </Group>
      </Flex>
      <SpotTable spots={spots} />
    </div>
  );
}

export default CameraDetail;