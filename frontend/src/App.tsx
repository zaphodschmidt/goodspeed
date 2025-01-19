import { useState, useEffect } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import './App.css'
import '@mantine/core/styles.css'; // Import Mantine core styles
import { Building } from './types';
import { getBuildings } from './apiService';
import BuildingsPage from './components/pages/BuildingsList';
import CamerasPage from './components/pages/BuildingDetail';
import ParkingSpotsPage from './components/pages/CameraDetail'
import 'mantine-react-table/styles.css'; //import MRT styles
import { mantineTheme } from './theme.ts'


function App() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBuildings()
      .then((data: Building[]) => setBuildings(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div>Loading...</div>; // You can use a spinner or skeleton loader here
  }

  return (
    <MantineProvider
      defaultColorScheme="auto"
      theme={mantineTheme}
    >
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<BuildingsPage buildings={buildings} />} />
          <Route
              path="/building/:buildingSlug"
              element={<CamerasPage buildings={buildings} />}
            />
            <Route
              path="/building/:buildingSlug/camera/:camNum"
              element={<ParkingSpotsPage buildings={buildings} />}
            />
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App
