import { 
    NativeSelect,
    Card,
    Title,
    Grid,
} from "@mantine/core";
import { useState, useEffect } from "react";
import { getBuildingLocations } from "../../apiService";
function CameraSettings(){
    const [locations, setLocation] = useState<string[]>([])
    const [selectedLocation, setSelectedLocation] = useState<string>("")

    useEffect(()=>{
        async function fetchLocations(){
            try{
                const data = await getBuildingLocations("Halley Rise");
                const locationNames = data.locations.map(location => location.name);
                setLocation(locationNames)
                console.log("Fetched data:", locationNames);
            } catch (error) {
                console.error("Error fetching locations:", error);
            }
        }
        fetchLocations();
    }, []);

    return(
        <Card shadow="sm" padding="lg" style={{ width: '100%', maxWidth: 400 }}>
            <Title order={2} align="center" mb="md">Camera Settings</Title>
            <Grid>
                <Grid.Col span={12}>
                    <NativeSelect
                        data={locations}
                        value={selectedLocation}
                        onChange={(event)=>setSelectedLocation(event.currentTarget.value)}
                        label="Select Location:"
                    />
                </Grid.Col>
            </Grid>
        </Card>
    );
}
export default CameraSettings;