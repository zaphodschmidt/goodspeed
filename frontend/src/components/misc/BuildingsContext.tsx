import { createContext } from "react";
import { Building } from "../../types";

export interface BuildingsContextType {
  buildings: Building[];
  loading: boolean;
}

export const BuildingsContext = createContext<BuildingsContextType | undefined>(
  undefined
);
