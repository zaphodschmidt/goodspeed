import { useContext } from "react";
import { BuildingsContext, BuildingsContextType } from "./BuildingsContext";

export const useBuildings = (): BuildingsContextType => {
  const context = useContext(BuildingsContext);
  if (!context) {
    throw new Error("useBuildings must be used within a BuildingsProvider");
  }
  return context;
};
