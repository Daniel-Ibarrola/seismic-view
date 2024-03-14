import {useContext} from "react";
import {Route, Routes, Navigate} from "react-router-dom"
import {
    Confirm,
    ChangePass,
    Login,
    Logout,
    Protected,
    Reconfirm,
    Register,
    Reset,
    ResetPassword,
} from "./auth/index.js";
import AuthContext from "./auth/context/AuthProvider.jsx";
import { Station } from "./station/index.js";
import { NavBar } from "./navbar/index.js";


const NoMatch = () => {
    return <h1>Aqui no hay nada: 404</h1>
}

const Home = () => {

    const { token } = useContext(AuthContext);
    if (!token){
        return <Navigate to="/login"/>;
    }

    return <Navigate to={"/station"} />;
}


const App = () => {
    return (
    <>
        <NavBar />
        <Routes>
            <Route index element={<Home />} />
            <Route
                path="station"
                element={
                <Protected>
                    <Station />
                </Protected>
                }
            />
            <Route
                path="change"
                element={
                    <Protected>
                        <ChangePass />
                    </Protected>
                }
            />
            <Route path="login" element={<Login />} />
            <Route path="logout" element={<Logout />} />
            <Route path="register" element={<Register />} />
            <Route path="confirm/:token" element={<Confirm />}/>
            <Route path="reconfirm" element={<Reconfirm />} />
            <Route path="resetpassword" element={<Reset />} />
            <Route path="reset/:token" element={<ResetPassword />} />
            <Route path="*" element={<NoMatch />} />
        </Routes>
    </>
    );
}

export default App;
