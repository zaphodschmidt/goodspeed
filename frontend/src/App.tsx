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
import { mantineCssVariableResolver } from './cssVariableResolver.ts';
import CustomAppShell from "./components/misc/CustomAppShell.tsx"


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
      cssVariablesResolver={mantineCssVariableResolver}
    >
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CustomAppShell><BuildingsPage buildings={buildings} /></CustomAppShell>} />
          <Route
              path="/building/:buildingSlug"
              element={<CustomAppShell><CamerasPage buildings={buildings} /></CustomAppShell>}
            />
            <Route
              path="/building/:buildingSlug/camera/:camNum"
              element={<CustomAppShell><ParkingSpotsPage buildings={buildings} /></CustomAppShell>}
            />
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App
