import { useState, useEffect } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import './App.css'
import '@mantine/core/styles.css'; // Import Mantine core styles
import { Building } from './types';
import { getBuildings } from './apiService';
import BuildingsPage from './components/BuildingsPage';
import CamerasPage from './components/CamerasPage';
import ParkingSpotsPage from './components/ParkingSpotsPage'


function App() {

  const [buildings, setBuildings] = useState<Building[]>([])

  // Fetch buildings only once when the component mounts
  useEffect(() => {
    getBuildings().then((data: Building[]) => setBuildings(data));
  }, []); // Empty dependency array ensures this runs only once

  console.log(buildings);


  return (
    <MantineProvider
      theme={{
        fontFamily: 'Montserrat, sans-serif',
        headings: { fontFamily: 'Montserrat, sans-serif' },
      }}
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
