import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { Login } from "../Login.jsx";
import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";
import { localStorageMock } from "../../test/mocks.ts";
import { waitForAuthFormSubmission } from "./submitAuthForm.ts";

Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
});

describe("Login", () => {
  it("Successful login redirects to stations page", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Login authClient={client} />
      </BrowserRouter>,
    );

    await waitForAuthFormSubmission(FakeUsers.Valid, "password", client.login);

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

    await waitForAuthFormSubmission(
      FakeUsers.Invalid,
      "password",
      client.login,
    );

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

    await waitForAuthFormSubmission(
      FakeUsers.Unconfirmed,
      "password",
      client.login,
    );
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
      await waitForAuthFormSubmission(
        FakeUsers.Unconfirmed,
        "password",
        client.login,
      );
    } catch (error) {
      expect(screen.queryByText(/Error al iniciar/)).toBeInTheDocument();
    }
  });
});
