import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";

import { Confirm } from "../Confirm.tsx";
import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";
import { BrowserRouter } from "react-router-dom";
import { waitForAuthFormSubmission } from "./submitAuthForm.ts";

describe("Confirm", () => {
  it("Successful confirmation displays alert", async () => {
    window.alert = vi.fn();

    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Confirm authClient={client} token="FakeToken" />
      </BrowserRouter>,
    );
    await waitForAuthFormSubmission(
      FakeUsers.Unconfirmed,
      "password",
      client.confirmUser,
    );

    expect(window.alert).toHaveBeenCalledTimes(1);
  });

  it("Already confirmed user displays alert", async () => {
    window.alert = vi.fn();

    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Confirm authClient={client} token="FakeToken" />
      </BrowserRouter>,
    );
    await waitForAuthFormSubmission(
      FakeUsers.Valid,
      "password",
      client.confirmUser,
    );

    expect(window.alert).toHaveBeenCalledTimes(1);
  });

  it("Invalid confirmation user or invalid link", async () => {
    window.alert = vi.fn();

    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Confirm authClient={client} token="FakeToken" />
      </BrowserRouter>,
    );

    await waitForAuthFormSubmission(
      FakeUsers.Invalid,
      "password",
      client.confirmUser,
    );
    expect(
      screen.queryByText(/link o usuario y contraseña inválido/),
    ).toBeInTheDocument();
  });
});
