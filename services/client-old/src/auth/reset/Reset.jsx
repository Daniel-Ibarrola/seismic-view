import {useReducer} from "react";
import {Link} from "react-router-dom";
import axios from "axios";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import {actions, formReducer} from "../state/formReducer.js";
import {resetUrl} from "../../api.js";
import {FailAlert} from "../../alerts/index.js";

const Reset = () => {
    // Request a password reset
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
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await axios.post(
                resetUrl,
                {email: loginData.email}
            );
            alert("Se ha enviado un email de confirmación");
            dispatchLoginData({
                type: actions.successLogin
            })
        } catch (err) {
            dispatchLoginData({
                type: actions.errorLogin,
                payload: <p><strong>Error: </strong>email no pertenece a ninguna cuenta</p>
            });
        }
    }

    return (
        <Container>
            <Row className="justify-content-center">
                <Col md={{span: 6}}>
                    <Card className="login-card">
                        <Card.Title className="login-title">Recuperar contraseña</Card.Title>
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
                                <div className="d-grid gap-2 login-button">
                                    <Button
                                        type="submit"
                                        disabled={!loginData.email}
                                    >
                                        Continuar
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
};

export { Reset };
