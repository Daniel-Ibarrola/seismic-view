import {describe, expect, it, vi} from "vitest";
import axios from "axios";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import {useLocation, useParams} from "react-router-dom";
import {Confirm, Reconfirm} from "./Confirm.jsx";

vi.mock("axios");
vi.mock("react-router-dom");


describe("Reconfirm", () => {

    const getMocks = (promise) => {
        axios.get.mockImplementationOnce(() => promise);
        useLocation.mockImplementation(() => ({
            state: {
                email: "triton@example.com",
                password: "dog",
            }
        }));
    }

    it("Successful reconfirmation displays message", async () => {
        const promise = Promise.resolve();
        getMocks(promise);

        render(<Reconfirm />);
        await waitFor(async () => await promise);

        expect(screen.queryByText(/enviado un email de confirmación/)).toBeInTheDocument();
    });

    it("Unsuccessful reconfirmation displays error message", async () => {
        const promise = Promise.reject();
        getMocks(promise);

        render(<Reconfirm />);

        try {
            await waitFor(async () => await promise);
        } catch {
            expect(screen.queryByText(/Error al enviar email/)).toBeInTheDocument();
        }
    });

});

describe("Confirm", () => {

    const getMocks = (promise) => {
        axios.get.mockImplementationOnce(() => promise);
        useParams.mockImplementation(() => ({
            token: "testToken"
        }));
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

    it("Successful confirmation displays alert", async () => {
        const promise = Promise.resolve({
            data: {
                "confirmed": "account confirmed"
            }
        });
        getMocks(promise);
        window.alert = vi.fn();

        render(<Confirm />);
        await waitForFormSubmission(promise);

        expect(window.alert).toHaveBeenCalledTimes(1);
    });

    it("Already confirmed user displays alert", async () => {
        const promise = Promise.resolve({
            data: {
                "confirmed": "user already confirmed"
            }
        });
        getMocks(promise);
        window.alert = vi.fn();

        render(<Confirm />);
        await waitForFormSubmission(promise);

        expect(window.alert).toHaveBeenCalledTimes(1);
    });

    it("Invalid confirmation link", async () => {
        const promise = Promise.reject();
        getMocks(promise);

        render(<Confirm />);

        try {
            await waitForFormSubmission(promise);
        } catch {
            expect(screen.queryByText(/link inválido/)).toBeInTheDocument();
        }
    });
});
