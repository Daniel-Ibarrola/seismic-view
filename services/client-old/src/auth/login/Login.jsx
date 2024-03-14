import { useReducer, useContext } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import { Link, Navigate } from "react-router-dom";

import AuthContext from "../context/AuthProvider.jsx";
import { formReducer, actions } from "../state/formReducer.js";
import { tokensUrl } from "../../api.js";
import { FailAlert } from "../../alerts/index.js";
import "../style.css";



const Login = () => {

    const [loginData, dispatchLoginData] = useReducer(formReducer, {
        email: "",
        password: "",
        isError: false,
        errorMsg: null,
    });
    const { token, setToken } = useContext(AuthContext);

    if (token) {
        return <Navigate to="/"/>
    }

    const handleEmailChange = (event) => {
        dispatchLoginData({
            type: actions.setEmail,
            payload: event.target.value
        });
    }

    const handlePasswordChange = (event) => {
        dispatchLoginData({
            type: actions.setPassword,
            payload: event.target.value
        });
    }

    const saveToken = (userToken) => {
        localStorage.setItem("token", JSON.stringify(userToken));
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(
                tokensUrl,
                {},
                { auth: {
                    username: loginData.email,
                    password: loginData.password,
                }
            });
            dispatchLoginData({
                type: actions.successLogin,
            });
            const token = response.data.token;
            saveToken(token);
            setToken(token);
        } catch (err) {
            let errMsg = null;
            if (!err?.response){
                errMsg = <p><strong>Error:</strong> Sin respuesta del servidor</p>
            }
            else if (err.response?.status === 400) {
                errMsg = (
                    <div>
                        <p><strong>Error:</strong> Usuario no confirmado</p>
                        <Link
                            to={"/reconfirm"}
                            state={{email: loginData.email, password: loginData.password}}
                        >
                            Click aquí para reenviar email de confirmación
                        </Link>
                    </div>

                )
            }
            else if (err.response?.status === 401) {
                errMsg = <p><strong>Error:</strong> Usuario o contraseña inválidos</p>
            }
            else {
                errMsg = <p><strong>Error:</strong> Falló el inicio de sesión</p>
            }
            dispatchLoginData({
                type: actions.errorLogin,
                payload: errMsg,
            });
        }
    }

    const handleSkipLogin = () => {
        // Skip login when developing
        if (import.meta.env.DEV){
            setToken({
                "token": "testToken",
                "expiration": null
            })
        }
    }

    return (
        <Container>
            <Row className="justify-content-center">
                <Col md={{span: 6}}>
                        <Card className="login-card">
                            <Card.Title className="login-title">Iniciar Sesión</Card.Title>
                            <hr />
                            <Card.Body className="login-body">
                                    <Form onSubmit={handleSubmit}>
                                        <Form.Group>
                                            <Form.Label
                                                htmlFor="email"
                                                className="form-label"
                                            >
                                                Correo
                                            </Form.Label>
                                            <Form.Control
                                                type="email"
                                                placeholder={"Email"}
                                                id="email"
                                                onChange={handleEmailChange}
                                                required
                                                className="login-row"
                                            />
                                        </Form.Group>
                                        <Form.Group>
                                            <Form.Label
                                                htmlFor="password"
                                                className="form-label"
                                            >
                                                Contraseña
                                            </Form.Label>
                                            <Form.Control
                                                type="password"
                                                placeholder="Contraseña"
                                                id="password"
                                                onChange={handlePasswordChange}
                                                required
                                                className="login-row"
                                            />
                                        </Form.Group>
                                        <div className="d-grid gap-2 login-button">
                                            <Button
                                                type="submit"
                                                disabled={!loginData.email || !loginData.password}
                                            >
                                                Iniciar sesión
                                            </Button>
                                        </div>
                                    </Form>
                                    <Card.Text>
                                        <Link to="/register">Crear una cuenta</Link>
                                    </Card.Text>
                                    <Card.Text>
                                        <Link to="/resetpassword">¿Olvidó su contraseña?</Link>
                                    </Card.Text>
                                {loginData.isError &&
                                    <FailAlert className="login-row">
                                        {loginData.errorMsg}
                                    </FailAlert>
                                }
                                {import.meta.env.DEV &&
                                    <Button
                                        variant="danger"
                                        onClick={handleSkipLogin}
                                    >
                                        Skip login
                                    </Button>

                                }
                            </Card.Body>
                        </Card>
                </Col>
            </Row>
        </Container>
    )
};


export { Login };