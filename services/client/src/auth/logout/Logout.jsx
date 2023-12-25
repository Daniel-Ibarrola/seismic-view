import {useContext} from "react";
import AuthContext from "../context/AuthProvider.jsx";
import {Navigate} from "react-router-dom";



const Logout = () => {

    const { setToken } = useContext(AuthContext);
    setToken("");
    localStorage.clear();

    return <Navigate to="/"/>
};

export { Logout };
