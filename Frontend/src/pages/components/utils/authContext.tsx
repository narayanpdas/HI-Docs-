import React, { createContext, useContext, useState } from "react";
import type{AuthContextType} from "../../interfaces"


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [role, setRole] = useState<"ADMIN" | "VIEWER" | null>("VIEWER");

  return (
    <AuthContext.Provider value={{ role, setRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be inside AuthProvider");
  return context;
};
