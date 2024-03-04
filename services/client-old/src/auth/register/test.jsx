import axios from "axios";
import {describe, expect, it, vi} from "vitest";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import { Register } from "./Register.jsx";


vi.mock("axios");


const rejectedPromise = (statusCode) => {
    return Promise.reject({
        response: {
            status: statusCode,
        }
    });
}

const waitForFormSubmission = async (promise) => {
    fireEvent.change(screen.getByPlaceholderText("Email"), {
        target: {value: "triton@example.com"}
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
        target: {value: "6MonkeysRLooking^"}
    });
    fireEvent.click(screen.getByRole("button"));
    await waitFor(async () => await promise);
}

describe("Register", () => {

    it("Email in use displays error message", async () => {
        const promise = rejectedPromise(400);
        axios.post.mockImplementationOnce(() => promise);

        render(<Register/>);
        try {
            await waitForFormSubmission(promise);
        } catch (error) {
            expect(screen.queryByText(/email en uso/)).toBeInTheDocument();
        }
    });

    it("Invalid email displays error message", async () => {
        const promise = rejectedPromise(401);
        axios.post.mockImplementationOnce(() => promise);

        render(<Register/>);
        try {
            await waitForFormSubmission(promise);
        } catch (error) {
            expect(screen.queryByText(/email inválido/)).toBeInTheDocument();
        }
    });

    it("Successful registration displays message", async () => {
        const promise = Promise.resolve();
        axios.post.mockImplementationOnce(() => promise);

        render(<Register/>);
        await waitForFormSubmission(promise);
        expect(screen.queryByText(/email de confirmación/)).toBeInTheDocument();
    })
});
