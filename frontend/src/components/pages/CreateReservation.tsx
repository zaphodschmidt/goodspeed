import { useParams } from "react-router-dom";
import { Building } from "../../types";
import { generateSlug } from "../misc/generateSlug";
import { useBuildings } from "../misc/useBuildingsContext";
import { Container, Center, Title, Stack } from "@mantine/core";


export default function CreateReservation(){
  const { buildings } = useBuildings();
  const { buildingSlug } = useParams<{ buildingSlug: string }>();
  const building: Building | undefined = buildings.find(
    (b) => generateSlug(b.name) === buildingSlug
  );

  return(
    <Center w='100vw' h='100vh'>
      <Stack>
        <Title order={1}>
          {building?.name}
        </Title>
        
      </Stack>
    </Center>
  )
}