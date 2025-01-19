import { List, Stack, Text, Title, useMantineTheme, Highlight, AspectRatio, Group, useMantineColorScheme, Box } from '@mantine/core';
import { useNavigate } from 'react-router-dom';

// import { generateSlug } from '../misc/generateSlug';
// import { useBuildings } from '../misc/useBuildingsContext';


function Welcome() {
    const theme = useMantineTheme()
    const navigate = useNavigate()
    const { colorScheme } = useMantineColorScheme()

    return (
        <Stack align='center' gap='xl'>
            <Text
                fs='italic'
                fz='100'
                fw={900}
                variant="gradient"
                gradient={{ from: theme.primaryColor, to: 'cyan', deg: 90 }}
            >
                Goodspeed.info
            </Text>
            <Stack w='75%' align='center'>

                <Highlight
                    fz='xl'
                    ta="center"
                    highlight="goodspeed.info"
                    highlightStyles={{
                        backgroundImage: colorScheme === 'dark'
                            ? 'linear-gradient(45deg, var(--mantine-color-white), var(--mantine-color-white))'
                            : 'linear-gradient(45deg, var(--mantine-color-black), var(--mantine-color-black))',
                        fontWeight: 700,
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                    }}
                >
                    Welcome to goodspeed.info, the all-in-one management platform for Goodspeed Parking.
                </Highlight>

                <Title order={3} ta='center' mt='lg' >
                    Features:
                </Title>

                <List spacing="xs" fz='lg' withPadding>
                    <List.Item>View camera feed snapshots for every building.</List.Item>
                    <List.Item>Add and manage parking spots with a simple drag-and-drop interface.</List.Item>
                    <List.Item>Gain insights into occupancy and streamline parking operations.</List.Item>
                </List>
            </Stack>

            {/* Hardcoded building buttons */}
            <Group justify='center' gap='5%' mt='lg'>
                <Stack
                    align='center'
                    w='25%'
                >
                    <AspectRatio
                        ratio={1}
                        style={{ cursor: 'pointer' }}
                        onClick={() => navigate('building/halley-rise')}>
                        <img src="https://www.halleyrise.com/wp-content/uploads/2023/05/TMRW.Brookfield.Properties.Halley.Rise_.Aerial.01.Copyright.tmrw_.se_-scaled.jpg?x62406" />
                    </AspectRatio>
                    <Title
                        order={3}
                        style={{ cursor: 'pointer' }}
                        onClick={() => navigate('building/halley-rise')}
                    >
                        Halley Rise
                    </Title>
                </Stack>
                <Stack align='center' w='25%'>
                    <AspectRatio
                        ratio={1}
                        style={{ cursor: 'pointer' }}
                        onClick={() => navigate('building/vertex')}>
                        <img src="https://www.vertexapts.com/wp-content/uploads/2022/05/0005_R6__3036-1-0x359-c-default.jpg.webp" />
                    </AspectRatio>
                    <Title
                        order={3}
                        style={{ cursor: 'pointer' }}
                        onClick={() => navigate('building/vertex')}
                    >
                        Vertex
                    </Title>

                </Stack>
            </Group>
        </Stack>
    );
}

export default Welcome;
