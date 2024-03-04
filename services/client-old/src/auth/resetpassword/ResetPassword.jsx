import {useState} from "react";
import {Link, useParams} from "react-router-dom";
import axios from "axios";
import {useFormik} from "formik";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import {formPasswordValidation} from "../validate/validation.js";
import {resetPasswordUrl} from "../../api.js";
import {FailAlert, SuccessAlert} from "../../alerts/index.js";


const ResetPassword = () => {
    const [response, setResponse] = useState({
        error: false,
        msg: "",
    });
    const { token } = useParams();

    const handleSubmit = async (values) => {
        try {
            await axios.post(
                resetPasswordUrl + token,
                {
                    password: values.password,
                }
            );
            setResponse({
                error: false,
                msg: <p>Se ha reseteado la contraseña.</p>
            })
        } catch (err) {
            setResponse({
                error: true,
                msg: <p><strong>Error:</strong> link invalido o expirado</p>
            });
        }
    }

    const formik = useFormik({
        initialValues: {
            password: "",
        },
        validate: formPasswordValidation,
        onSubmit: async (values) => await handleSubmit(values),
    })

    return (
        <Container>
            <Row className="justify-content-center">
                <Col md={{span: 6}}>
                    <Card className="login-card">
                        <Card.Title className="login-title">Resetear Contraseña</Card.Title>
                        <hr />
                        <Card.Body className="login-body">
                            <Form noValidate onSubmit={formik.handleSubmit}>
                                <Form.Group>
                                    <Form.Label htmlFor="password">Nueva contraseña</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Contraseña"
                                        id="password"
                                        className="login-row"
                                        onChange={formik.handleChange}
                                        value={formik.values.password}
                                        isValid={formik.touched.password && !formik.errors.password}
                                        isInvalid={formik.errors.hasOwnProperty("password")}
                                    />
                                    <Form.Control.Feedback className="form-error" type="invalid">
                                        {formik.errors.password}
                                    </Form.Control.Feedback>
                                </Form.Group>
                                <div className="d-grid gap-2 login-button">
                                    <Button
                                        type="submit"
                                    >
                                        Resetear contraseña
                                    </Button>
                                </div>
                                {(response.error && response.msg) && <FailAlert>{response.msg}</FailAlert>}
                                {(!response.error && response.msg) && <SuccessAlert>{response.msg}</SuccessAlert>}
                            </Form>
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

export { ResetPassword };