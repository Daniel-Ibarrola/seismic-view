import axios from "axios";
import { describe, expect, it, vi } from "vitest";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import {ChangePass} from "./ChangePass.jsx";

vi.mock("axios");


describe("ChangePass", () => {

    const waitForFormSubmission = async (promise) => {
        fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
            target: {value: "6MonkeysRLooking^"}
        });
        fireEvent.change(screen.getByPlaceholderText("Nueva contraseña"), {
            target: {value: "6ElephantsRLooking^"}
        });
        fireEvent.click(screen.getByRole("button"));
        await waitFor(async () => await promise);
    }

    it("Successful password change displays message", async () => {
        const promise = Promise.resolve();
        axios.post.mockImplementationOnce(() => promise);

        render(<ChangePass />);

        await waitForFormSubmission(promise);
        expect(screen.queryByText(/se actualizó la contraseña/)).toBeInTheDocument();
    });

    it("Incorrect password displays error message", async () => {
        const promise = Promise.reject();
        axios.post.mockImplementationOnce(() => promise);

        render(<ChangePass />);

        try {
            await waitForFormSubmission(promise);
        } catch {
            expect(screen.queryByText(/contraseña incorrecta/)).toBeInTheDocument();
        }
    })

});
