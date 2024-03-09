import { describe, expect, it } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { Login } from "../Login.jsx";
import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";
import { localStorageMock } from "../../test/mocks.ts";

Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
});

describe("Login", () => {
  const waitForFormSubmission = async (
    user: string,
    password: string,
    client: FakeAuthClient,
  ): Promise<void> => {
    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: user },
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
      target: { value: password },
    });
    fireEvent.click(screen.getAllByRole("button")[0]);
    await waitFor(async () => client.login);
  };

  it("Successful login redirects to stations page", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Login authClient={client} />
      </BrowserRouter>,
    );

    await waitForFormSubmission(FakeUsers.Valid, "password", client);

    const token = window.localStorage.getItem("token");
    expect(token).not.toBeNull();
    expect(token).toBe("FakeToken");
  });

  it("Invalid credentials display error", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Login authClient={client} />
      </BrowserRouter>,
    );

    await waitForFormSubmission(FakeUsers.Invalid, "password", client);

    expect(
      screen.queryByText(/Usuario o contraseña inválidos/),
    ).toBeInTheDocument();
  });

  it("Unconfirmed user displays re-send confirmation link", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Login authClient={client} />
      </BrowserRouter>,
    );

    await waitForFormSubmission(FakeUsers.Unconfirmed, "password", client);
    expect(screen.queryByText(/no confirmado/)).toBeInTheDocument();
    expect(
      screen.queryByText(/reenviar email de confirmación/),
    ).toBeInTheDocument();
  });

  it("Login service error displays error message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Login authClient={client} />
      </BrowserRouter>,
    );

    try {
      await waitForFormSubmission(FakeUsers.Unconfirmed, "password", client);
    } catch (error) {
      expect(screen.queryByText(/Error al iniciar/)).toBeInTheDocument();
    }
  });
});
