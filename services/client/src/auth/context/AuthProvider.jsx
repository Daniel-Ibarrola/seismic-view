import {createContext, useState} from "react";

const AuthContext = createContext("");

export const AuthProvider = ({ children }) => {
    const getToken = () => {
        const tokenString = localStorage.getItem("token");
        return JSON.parse(tokenString);
    };

    const [token, setToken] = useState(getToken);

    return (
        <AuthContext.Provider value={{ token, setToken }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext;
