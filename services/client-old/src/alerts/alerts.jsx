import Row from "react-bootstrap/Row";
import Alert from "react-bootstrap/Alert";


export const FailAlert = ({ children }) => {
    return (
        <Row>
            <Alert variant="danger" className="alert-msg">
                {children}
            </Alert>
        </Row>
    );
};


export const SuccessAlert = ({ children }) => {
    return (
        <Alert key="successAlert" variant="primary">
            {children}
        </Alert>
    );
};
