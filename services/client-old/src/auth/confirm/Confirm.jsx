import {useEffect, useReducer, useState} from "react";
import {Link, useLocation, useParams} from "react-router-dom";
import Container from "react-bootstrap/Container";
import axios from "axios";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";

import {actions, formReducer} from "../state/formReducer.js";
import { FailAlert } from "../../alerts/index.js";
import {confirmUrl, reconfirmUrl} from "../../api.js";


const Confirm = () => {
    const { token } = useParams();
    const [loginData, dispatchLoginData] = useReducer(formReducer, {
        email: "",
        password: "",
        isError: false,
        errorMsg: null,
    });

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

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get(
                confirmUrl + token,
                {
                    auth: {
                        username: loginData.email,
                        password: loginData.password,
                    }
                }
            );
            if (response.data.confirmed === "user already confirmed"){
                alert("Este usuario ya ha sido confirmado");
            }
            else if (response.data.confirmed === "account confirmed"){
                alert("Su cuenta ha sido confirmada");
            }
            dispatchLoginData({type: actions.successLogin});
        } catch (err) {
            dispatchLoginData({
                type: actions.errorLogin,
                payload: <p><strong>Error:</strong> link inválido o expirado</p>
            })
        }
    }

    return (
        <Container>
            <Row className="justify-content-center">
                <Col md={{span: 6}}>
                    <Card className="login-card">
                        <Card.Title className="login-title">Confirmación de cuenta</Card.Title>
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
                                        Confirmar
                                    </Button>
                                </div>
                            </Form>
                            {loginData.isError &&
                                <FailAlert className="login-row">
                                    {loginData.errorMsg}
                                </FailAlert>
                            }
                            <Card.Text>
                                <Link to="/">Volver al inicio</Link>
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}

const Reconfirm = () => {

    const { state } = useLocation();
    const [confirmStatus, setConfirmStatus] = useState("");

    const requestConfirmation = async () => {
        if (state.email && state.password) {
            try {
                await axios.get(
                    reconfirmUrl,
                    {
                        auth: {
                            username: state.email,
                            password: state.password,
                        }
                    }
                );
                setConfirmStatus("Se ha enviado un email de confirmación");
            } catch (error) {
                setConfirmStatus("Error al enviar email de confirmación");
            }
        }
    };

    useEffect(() => {
        requestConfirmation();
    }, []);

    return (
        <Container>
            <h2>Confirmación de cuenta</h2>
            <p>{confirmStatus}</p>
            <Link to="/">Volver al inicio</Link>
        </Container>
    )

};


export { Confirm, Reconfirm };
