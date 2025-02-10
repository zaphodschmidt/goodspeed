import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { Building, Camera, ParkingSpot, Vertex } from "../../types.ts";
import {
  Button,
  AspectRatio,
  BackgroundImage,
  Group,
  Stack,
  Title,
  ActionIcon,
  Tooltip,
  Image
} from "@mantine/core";
import no_image from "../../assets/no_image.jpeg";
import { generateSlug } from "../misc/generateSlug.ts";
import {
  createParkingSpot,
  deleteParkingSpot,
  getCameraByID,
  updateParkingSpot,
} from "../../apiService.ts";
import SpotPolygon from "../spotComponents/SpotPolygon.tsx";
import SpotTable from "../spotComponents/SpotTable.tsx";
import { useBuildings } from "../misc/useBuildingsContext.ts";
import CustomLoader from "../misc/CustomLoader.tsx";
import { IconCheck, IconEdit } from "@tabler/icons-react";
import { useElementSize } from '@custom-react-hooks/use-element-size';

const BACKEND_IMAGE_WIDTH = 2560;
const BACKEND_IMAGE_HEIGHT = 1920;
const LEFT_X = Math.round(BACKEND_IMAGE_WIDTH * 0.25);
const RIGHT_X = Math.round(BACKEND_IMAGE_WIDTH * 0.75);
const TOP_Y = Math.round(BACKEND_IMAGE_HEIGHT * 0.25);
const BOTTOM_Y = Math.round(BACKEND_IMAGE_HEIGHT * 0.75);

function CameraDetail() {
  /*
  Hooks
  */
  //obtain building information from current URL
  const { buildingSlug, camNum } = useParams<{
    buildingSlug: string;
    camNum: string;
  }>();
  // Reference to the BackgroundImage to get its dimensions
  const [imageRef, rect] = useElementSize();
  //get updated buildings using useBuildings context
  const { buildings } = useBuildings();

  /*
  Consts
  */
  //this building, based on the current URL
  const building: Building | undefined = buildings.find(
    (b) => generateSlug(b.name) === buildingSlug
  );
  //find the id of the camera based on the current building and url
  const camera_id =
    building?.cameras.find((c) => c.cam_num === Number(camNum))?.id ||
    undefined;
  const xScale = rect.width / BACKEND_IMAGE_WIDTH
  const yScale = rect.height / BACKEND_IMAGE_HEIGHT

  /*
  States
  */
  const [camera, setCamera] = useState<Camera | undefined>();
  const [spots, setSpots] = useState<ParkingSpot[]>([]);
  const [editMode, setEditMode] = useState(false);

  console.log(spots)

  /*
  UseEffects
  */
  // Update the image dimensions when the component mounts, and fetch updated camera data.
  useEffect(() => {
    if (camera_id) {
      getCameraByID(camera_id).then((fetched_cam: Camera) => {
        setCamera(fetched_cam);
        setSpots(fetched_cam.parking_spots);
        console.log(fetched_cam.parking_spots);
      });
    }
  }, [camera_id]);


  /*
  Functions
  */
  const deleteAllSpots = () => {
    for (const parking_spot of spots) {
      deleteParkingSpot(parking_spot);
    }
    setSpots([]);
  };

  const deleteSpot = (spotToDelete: ParkingSpot) => {
    deleteParkingSpot(spotToDelete);
    setSpots(spots.filter((spot) => spot.id !== spotToDelete.id));
  };

  const AddNewSpot = (camera: Camera) => {
    const spotNum = spots.length;
    const vertices: Vertex[] = [
      {
        x: LEFT_X,
        y: TOP_Y,
      },
      {
        x: LEFT_X,
        y: BOTTOM_Y,
      },
      {
        x: RIGHT_X,
        y: BOTTOM_Y,
      },
      {
        x: RIGHT_X,
        y: TOP_Y,
      },
    ];

    const newSpot: ParkingSpot = {
      camera: camera.id!,
      spot_num: spotNum,
      vertices,
      occupied: false,
    };
    console.log("newSpot:", newSpot);
    createParkingSpot(newSpot)
      .then((createdSpot) => {
        console.log("Parking spot created", createdSpot);
        setSpots([...spots, createdSpot]);
      })
      .catch((error) => {
        console.error("Error in creating parking spot", error);
      });
  };

  const handleUpdateSpot = async (updatedSpot: ParkingSpot) => {
    console.log("alrighty, updating this spot", updatedSpot)
    await updateParkingSpot(updatedSpot);
    setSpots(
      spots.map((spot) => (spot.id === updatedSpot.id ? updatedSpot : spot))
    );
  };

  function setSpot(newSpot: ParkingSpot){
    setSpots((prev) => prev.map((s) => s.id === newSpot.id ? newSpot : s))
  }

  /*
  Returns
  */
  if (!building || !camera) {
    return <CustomLoader />;
  }

  return (
    <Stack mt="lg" mb="lg" align="center">
      <Group align="center">
        <Title ml="50px">Camera {camera.cam_num}</Title>
        <Tooltip label={editMode ? "Close editor" : "Edit spots"}>
          <ActionIcon
            size="lg"
            variant="subtle"
            onClick={() => setEditMode(!editMode)}
          >
            {editMode ? <IconCheck /> : <IconEdit />}
          </ActionIcon>
        </Tooltip>
      </Group>
      <AspectRatio w={1000} mx="auto" pos="relative" ratio={4 / 3}>
        <BackgroundImage
          ref={imageRef}
          radius="md"
          // onLoad={() => {
          //   const rect = imageRef.current!.getBoundingClientRect();
          //   setXScale(rect.width / BACKEND_IMAGE_WIDTH)
          //   setYScale(rect.height / BACKEND_IMAGE_HEIGHT)
          // }}
          src={camera.image?.image_url || no_image}
          style={{
            position: "relative",
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        > 
          {spots.length > 0 &&
            spots.map((spot, index) => {
              return(<SpotPolygon
                xScale={xScale}
                yScale={yScale}
                key={spot.id}
                spot={spot}
                colorKey={index}
                deleteSpot={deleteSpot}
                handleUpdateSpot={handleUpdateSpot}
                editMode={editMode}
                setSpot={setSpot}
              />)
          })}
        </BackgroundImage>
      </AspectRatio>
      {editMode && (
        <Group align="center" justify="center">
          <Button onClick={() => AddNewSpot(camera)}>Add Spot</Button>
          <Button onClick={deleteAllSpots}>Delete All Spots</Button>
        </Group>
      )}
      <SpotTable spots={[...spots].sort((a, b) => a.spot_num - b.spot_num)} />
    </Stack>
  );
}

export default CameraDetail;
