import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MantineProvider } from "@mantine/core";
import "./App.css";
import "@mantine/core/styles.css"; // Import Mantine core styles
import Welcome from "./components/pages/Welcome.tsx";
import BuildingDetail from "./components/pages/BuildingDetail";
import CameraDetail from "./components/pages/CameraDetail";
import "mantine-react-table/styles.css"; //import MRT styles
import { mantineTheme } from "./theme.ts";
import { mantineCssVariableResolver } from "./cssVariableResolver.ts";
import CustomAppShell from "./components/misc/CustomAppShell.tsx";
import { BuildingsProvider } from "./components/misc/BuildingsProvider.tsx";

function App() {
  return (
    <MantineProvider
      defaultColorScheme="auto"
      theme={mantineTheme}
      cssVariablesResolver={mantineCssVariableResolver}
    >
      <BuildingsProvider>
        <BrowserRouter>
          <Routes>
            <Route
              path="/"
              element={
                <CustomAppShell>
                  <Welcome />
                </CustomAppShell>
              }
            />
            <Route
              path="/building/:buildingSlug"
              element={
                <CustomAppShell>
                  <BuildingDetail />
                </CustomAppShell>
              }
            />
            <Route
              path="/building/:buildingSlug/camera/:camNum"
              element={
                <CustomAppShell>
                  <CameraDetail />
                </CustomAppShell>
              }
            />
          </Routes>
        </BrowserRouter>
      </BuildingsProvider>
    </MantineProvider>
  );
}

export default App;
