import { useNavigate } from 'react-router-dom';
import { Button, Stack, Center } from '@mantine/core';
import { generateSlug } from '../misc/generateSlug';
import { useBuildings } from '../misc/useBuildingsContext';


function BuildingsList() {
    const { buildings } = useBuildings()
    const navigate = useNavigate();

    return (
        <div>
            <Center>
                <Stack h="500px" w="500px">
                    {buildings.map((building) => {
                        const slug = generateSlug(building.name);
                        return (
                            <Button
                                key={building.id}
                                onClick={() => navigate(`/building/${slug}`)}
                            >
                                {building.name}
                            </Button>
                        );
                    })}
                </Stack>
            </Center>
        </div>
    );
}

export default BuildingsList;
