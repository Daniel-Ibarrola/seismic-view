import { BrowserRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";
import { Reset } from "../Reset.tsx";
import { waitForPasswordFormSubmission } from "./submitAuthForm.ts";

describe("Reset", () => {
  it("Successful reset displays alert", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Reset authClient={client} token="FakeToken" />
      </BrowserRouter>,
    );

    await waitForPasswordFormSubmission(FakeUsers.Valid, client.resetPassword);

    expect(screen.queryByText(/reseteado la contraseña/)).toBeInTheDocument();
  });

  it("Unsuccessful reset displays message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <Reset authClient={client} token="FakeToken" />
      </BrowserRouter>,
    );

    await waitForPasswordFormSubmission(
      FakeUsers.Invalid,
      client.resetPassword,
    );

    expect(screen.queryByText(/link invalido o expirado/)).toBeInTheDocument();
  });
});
