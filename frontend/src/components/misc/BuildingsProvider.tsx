import { useState, useEffect } from "react";
import { getBuildings } from "../../apiService";
import { Building } from "../../types";
import { BuildingsContext } from "./BuildingsContext";

export function BuildingsProvider({ children }: { children: React.ReactNode }) {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBuildings()
      .then((data) => setBuildings(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <BuildingsContext.Provider value={{ buildings, loading }}>
      {children}
    </BuildingsContext.Provider>
  );
}
