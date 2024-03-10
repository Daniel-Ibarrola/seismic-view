import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";

import { Register } from "../Register.tsx";
import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";

import { BrowserRouter } from "react-router-dom";
import { waitForAuthFormSubmission } from "./submitAuthForm.ts";

describe("Register", () => {
  it("Email in use displays error message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Register authClient={client} />
      </BrowserRouter>,
    );

    await waitForAuthFormSubmission(
      FakeUsers.InUse,
      "password",
      client.register,
    );

    expect(screen.queryByText(/email en uso/)).toBeInTheDocument();
  });

  it("Invalid email displays error message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Register authClient={client} />
      </BrowserRouter>,
    );

    await waitForAuthFormSubmission(
      FakeUsers.Invalid,
      "password",
      client.register,
    );

    expect(screen.queryByText(/email inválido/)).toBeInTheDocument();
  });

  it("Successful registration displays message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Register authClient={client} />
      </BrowserRouter>,
    );

    await waitForAuthFormSubmission(
      FakeUsers.Valid,
      "password",
      client.register,
    );
    expect(screen.queryByText(/email de confirmación/)).toBeInTheDocument();
  });
});
