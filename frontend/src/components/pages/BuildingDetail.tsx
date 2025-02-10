import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Building, Camera, ParkingSpot } from "../../types";
import {
  Stack,
  Pagination,
  Grid,
  AspectRatio,
  Image,
  Text,
  Group,
  Tabs,
  Title,
  // useMatches,
  useMantineTheme,
  useMantineColorScheme,
  Center,
} from "@mantine/core";
import { generateSlug } from "../misc/generateSlug";
import no_image from "../../assets/no_image.jpeg";
import SpotTable from "../spotComponents/SpotTable";
import { useBuildings } from "../misc/useBuildingsContext";
import CustomLoader from "../misc/CustomLoader";

function BuildingDetail() {
  const { buildings } = useBuildings();
  const { buildingSlug } = useParams<{ buildingSlug: string }>();
  const navigate = useNavigate();
  const building: Building | undefined = buildings.find(
    (b) => generateSlug(b.name) === buildingSlug
  );
  const cameras: Camera[] =
    building?.cameras.sort((a, b) => a.cam_num - b.cam_num) || [];

  const [activePage, setPage] = useState(1);

  const theme = useMantineTheme();
  const { colorScheme } = useMantineColorScheme();

  const camsPerPage = 12;
  // const camsPerPage = useMatches({
  //   base: 6,
  //   sm: 9,
  //   lg: 12,
  // });
  const numPages = Math.ceil(cameras.length / camsPerPage);
  const displayedCameras: Camera[] = cameras.slice(
    (activePage - 1) * camsPerPage,
    activePage * camsPerPage
  );
  const [activeTab, setActiveTab] = useState<string | null>("cameras");

  const spots: ParkingSpot[] =
    cameras
      ?.flatMap((camera) =>
        camera.parking_spots.map((spot) => ({
          ...spot,
          cam_num: camera.cam_num,
        }))
      )
      .sort((a, b) => a.spot_num - b.spot_num) || [];

  useEffect(() => {
    setPage(1);
    setActiveTab("cameras");
  }, [building]);

  if (!building) return <CustomLoader />;

  return (
    <Stack mt="lg" mb="lg">
      <Title ta="center">{building.name}</Title>
      <Tabs value={activeTab} onChange={setActiveTab}>
        <Tabs.List>
          <Tabs.Tab value="cameras">Cameras</Tabs.Tab>
          <Tabs.Tab value="spots">Parking Spots</Tabs.Tab>
        </Tabs.List>
        <Tabs.Panel value="cameras">
          <Stack align="center">
            <Center
              w='100%'
              p='md'
              bg={
                colorScheme === "dark"
                  ? theme.colors.dark[7]
                  : theme.white
              }
              style={{
                position: "sticky",
                top: 75, // Adjust this value if you have a header or other elements above
                // zIndex: 100, // Ensure it stays above other content
                // background: "white", // Add a background to avoid transparency issues
                // padding: "0.5rem 0", // Optional padding for better appearance
              }}
            >
              <Pagination
                size="md"
                value={activePage}
                onChange={setPage}
                total={numPages}
              />
            </Center>
            <Grid align="center" justify="flex-start" p='md'>
              {displayedCameras.map((camera) => (
                <Grid.Col span={{ base: 6, sm: 4, md: 3 }} key={camera.id}>
                  <AspectRatio ratio={4 / 3}>
                    <div
                      style={{ cursor: "pointer" }}
                      onClick={() =>
                        navigate(
                          `/building/${buildingSlug}/camera/${camera.cam_num}`
                        )
                      }
                    >
                      <Image
                        src={camera.image?.image_url || no_image}
                        onError={(event) => {
                          event.currentTarget.src = no_image; // Set fallback image if the original URL is invalid
                        }}
                        radius="md"
                      />
                      <Group justify="space-between" gap="xs" wrap="nowrap">
                        <Text fz="clamp(0.25rem, 5vw, 1rem)">
                          {camera.cam_num}
                        </Text>
                        <Text
                          fz="clamp(0.25rem, 5vw, .75rem)"
                          c="gray"
                          truncate="end"
                        >
                          {camera.MAC}
                        </Text>
                      </Group>
                    </div>
                  </AspectRatio>
                </Grid.Col>
              ))}
            </Grid>
          </Stack>
        </Tabs.Panel>
        <Tabs.Panel value="spots">
          <SpotTable spots={spots} detailed />
        </Tabs.Panel>
      </Tabs>
    </Stack>
  );
}

export default BuildingDetail;
