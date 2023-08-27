import React, { createContext, useEffect } from "react";
import { useContext, useState } from "react";


let AuthContext = createContext(
    {
        isAuthenticated: false,
        loginAuth: () => {},
        logoutAuth: () => {}
    }
);

export const Authentication = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const loginAuth = () => {
        setIsAuthenticated(true);
    };

    const logoutAuth = () => {
        setIsAuthenticated(false);
    };

    
    return(
        <AuthContext.Provider value={{isAuthenticated,loginAuth,logoutAuth}}>
            {children}
        </AuthContext.Provider>
    );
};
export const useAuth = () =>{
    return useContext(AuthContext);
}