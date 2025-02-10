import {
  List,
  Stack,
  Text,
  Title,
  useMantineTheme,
  Highlight,
  AspectRatio,
  Group,
  useMantineColorScheme,
  Image,
} from "@mantine/core";
import { useNavigate } from "react-router-dom";

// import { generateSlug } from '../misc/generateSlug';
// import { useBuildings } from '../misc/useBuildingsContext';

function Welcome() {
  const theme = useMantineTheme();
  const navigate = useNavigate();
  const { colorScheme } = useMantineColorScheme();

  return (
    <Stack align="center" gap="md" p="md">
      <Text
        w="100%"
        fs="italic"
        ta="center"
        fz="clamp(2rem, 5vw, 5rem)" // Adjust font size dynamically
        fw={900}
        variant="gradient"
        gradient={{ from: theme.primaryColor, to: "cyan", deg: 90 }}
      >
        Goodspeed
      </Text>
      <Highlight
        fz="xl"
        ta="center"
        highlight="goodspeedparking.info"
        highlightStyles={{
          backgroundImage:
            colorScheme === "dark"
              ? "linear-gradient(45deg, var(--mantine-color-white), var(--mantine-color-white))"
              : "linear-gradient(45deg, var(--mantine-color-black), var(--mantine-color-black))",
          fontWeight: 700,
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        Welcome to goodspeedparking.info, the management platform for Goodspeed
        Parking.
      </Highlight>

      <Title order={3} ta="center" mt="lg">
        Features:
      </Title>

      <List spacing="xs" fz="lg" withPadding>
        <List.Item>View camera feed snapshots for each building.</List.Item>
        <List.Item>
          Add and manage parking spots and vertices with a simple drag-and-drop
          interface.
        </List.Item>
        <List.Item>
          Monitor spot occupancy and reservation information.
        </List.Item>
      </List>

      {/* Hardcoded building buttons */}
      <Group justify="center" gap="5%" align="flex-start" mt="xl">
        <Stack align="center" w="25%">
          <AspectRatio
            ratio={1}
            style={{ cursor: "pointer" }}
            onClick={() => navigate("building/halley-rise")}
          >
            <Image
              radius="md"
              src="https://www.halleyrise.com/wp-content/uploads/2023/05/TMRW.Brookfield.Properties.Halley.Rise_.Aerial.01.Copyright.tmrw_.se_-scaled.jpg?x62406"
            />
          </AspectRatio>
          <Title
            ta="center"
            order={3}
            style={{ cursor: "pointer" }}
            onClick={() => navigate("building/halley-rise")}
          >
            Halley Rise
          </Title>
        </Stack>
        <Stack align="center" w="25%">
          <AspectRatio
            ratio={1}
            style={{ cursor: "pointer" }}
            onClick={() => navigate("building/vertex")}
          >
            <Image
              radius="md"
              src="https://www.vertexapts.com/wp-content/uploads/2022/05/0005_R6__3036-1-0x359-c-default.jpg.webp"
            />
          </AspectRatio>
          <Title
            order={3}
            style={{ cursor: "pointer" }}
            onClick={() => navigate("building/vertex")}
          >
            Vertex
          </Title>
        </Stack>
      </Group>
    </Stack>
  );
}

export default Welcome;
