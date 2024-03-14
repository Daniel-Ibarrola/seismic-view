import axios from "axios";
import { describe, expect, it, vi } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { Login } from "./Login.jsx";


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
    fireEvent.click(screen.getAllByRole("button")[0]);
    await waitFor(async () => await promise);
}


describe("Login", () => {
    // it("Successful login redirects to stations page", async () => {
    //     const promise = Promise.resolve({
    //         data: {
    //             token: "FakeToken",
    //             expiration: 3600,
    //         }});
    //     axios.post.mockImplementationOnce(() => promise);
    //
    //     const routes = [
    //         {
    //             path: "/login",
    //             element: <AuthProvider><login /></AuthProvider>,
    //         },
    //         {
    //             path: "/stations",
    //             element: <Stations />
    //         }
    //     ]
    //     const router = createMemoryRouter(routes, {
    //        initialEntries: ["/login"],
    //        initialIndex: 0,
    //     });
    //
    //     render(<RouterProvider router={router} />);
    //     expect(screen.queryAllByText(/Iniciar/)[0]).toBeInTheDocument();
    //
    //     await waitFor(async () =>  fireEvent.click(
    //         screen.queryByRole("button"))
    //     );
    //     await waitFor(async () => await promise);
    //     expect(screen.queryByText("Estaciones")).toBeInTheDocument();
    // });

    it("Invalid credentials display error", async () => {
        const promise = rejectedPromise(401);
        axios.post.mockImplementationOnce(() => promise);

        render(<BrowserRouter><Login /></BrowserRouter>);

        try {
            await waitForFormSubmission(promise);
        } catch (error) {
            expect(screen.queryByText(/Usuario o contraseña inválidos/)).toBeInTheDocument();
        }
    });

    it("Unconfirmed user displays re-send confirmation link", async () => {
        const promise = rejectedPromise(400);
        axios.post.mockImplementationOnce(() => promise);

        render(<BrowserRouter><Login /></BrowserRouter>);

        try {
            await waitForFormSubmission(promise);
        } catch (error) {
            expect(screen.queryByText(/no confirmado/)).toBeInTheDocument();
            expect(screen.queryByText(/reenviar email de confirmación/)).toBeInTheDocument();
        }
    });

});
