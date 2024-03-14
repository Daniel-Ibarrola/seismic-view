import { describe, expect, it, vi } from "vitest";
import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import axios from "axios";
import {Reset} from "./Reset.jsx";
import {BrowserRouter} from "react-router-dom";

vi.mock("axios");

describe("Reset", () => {
    const waitForFormSubmission = async (promise) => {
        fireEvent.change(screen.getByPlaceholderText("Email"), {
            target: {value: "triton@example.com"}
        });
        fireEvent.click(screen.getByRole("button"));
        await waitFor(async () => await promise);
    };

    it("Successful reset displays alert", async () => {
        const promise  = Promise.resolve();
        axios.post.mockImplementationOnce(() => promise);
        window.alert = vi.fn();

        render(<BrowserRouter><Reset /></BrowserRouter>);
        await waitForFormSubmission(promise);
        expect(window.alert).toHaveBeenCalledTimes(1);
    });

    it("Unsuccessful reset displays message", async () => {
        const promise  = Promise.reject();
        axios.post.mockImplementationOnce(() => promise);
        render(<BrowserRouter><Reset /></BrowserRouter>);

        try {
            await waitForFormSubmission(promise);
        } catch {
            expect(
                screen.queryByText(/email no pertenece a ninguna cuenta/)
            ).toBeInTheDocument();
        }
    });
});
