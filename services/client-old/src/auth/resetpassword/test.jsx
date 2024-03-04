import axios from "axios";
import {useParams} from "react-router-dom";
import {describe, expect, it, vi} from "vitest";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";

import { ResetPassword } from "./ResetPassword.jsx";


vi.mock("axios");
vi.mock("react-router-dom");


describe("ResetPassword", () => {
    const waitForFormSubmission = async (promise) => {
        fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
            target: {value: "6MonkeysRLooking^"}
        });
        fireEvent.click(screen.getByRole("button"));
        await waitFor(async () => await promise);
    };

    const getMocks = (promise) => {
        axios.post.mockImplementationOnce(() => promise);
        useParams.mockImplementation(() => ({
           token: "testToken",
        }));
    };

    it("Successful reset displays alert", async () => {
        const promise  = Promise.resolve();
        getMocks(promise);

        render(<ResetPassword />);
        await waitForFormSubmission(promise);
        expect(screen.queryByText(/reseteado la contraseña/)).toBeInTheDocument();
    });

    it("Unsuccessful reset displays message", async () => {
        const promise  = Promise.reject();
        getMocks(promise);
        render(<ResetPassword />);

        try {
            await waitForFormSubmission(promise);
        } catch {
            expect(
                screen.queryByText(/link invalido o expirado/)
            ).toBeInTheDocument();
        }
    });
})
