import {useContext, useState} from "react";
import axios from "axios";
import {useFormik} from "formik";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import {FailAlert, SuccessAlert} from "../../alerts/index.js";
import {changePasswordUrl} from "../../api.js";
import {formPasswordValidation} from "../validate/validation.js";
import AuthContext from "../context/AuthProvider.jsx";

const ChangePass = () => {
    const [response, setResponse] = useState({
        error: false,
        msg: null,
    });

    const { token } = useContext(AuthContext);

    const handleSubmit = async (values) => {
        try {
            await axios.post(
                changePasswordUrl,
                {
                    old: values.oldPassword,
                    new: values.password,
                },
                {headers: {Authorization: `Bearer ${token}`}}
            );
            setResponse({
                error: false,
                msg: <p><strong>Éxito: </strong>se actualizó la contraseña</p>
            })
        } catch {
            setResponse({
                error: true,
                msg: <p><strong>Error: </strong>contraseña incorrecta</p>
            });
        }

    }

    const formik = useFormik({
        initialValues: {
            oldPassword: "",
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
                        <Card.Title className="login-title">Cambiar contraseña</Card.Title>
                        <hr />
                        <Card.Body className="login-body">
                            <Form noValidate onSubmit={formik.handleSubmit}>
                                <Form.Group>
                                    <Form.Label htmlFor="email">Contraseña actual</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Contraseña"
                                        id="oldPassword"
                                        className="login-row"
                                        onChange={formik.handleChange}
                                        value={formik.values.oldPassword}
                                    />
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label htmlFor="password">Nueva contraseña</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Nueva contraseña"
                                        id="password"
                                        className="login-row"
                                        onChange={formik.handleChange}
                                        value={formik.values.password}
                                        isValid={formik.touched.password
                                            && !formik.errors.password}
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
                                        Cambiar contraseña
                                    </Button>
                                </div>
                                {(response.error && response.msg) && <FailAlert>{response.msg}</FailAlert>}
                                {(!response.error && response.msg) && <SuccessAlert>{response.msg}</SuccessAlert>}
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
};

export { ChangePass };
