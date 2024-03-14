import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

import { RequestReset } from "../RequestReset.tsx";
import { FakeAuthClient, FakeUsers } from "./auth.mock.ts";
import { BrowserRouter } from "react-router-dom";
import { waitForUserFormSubmission } from "./submitAuthForm.ts";

describe("RequestReset", () => {
  it("Successful reset request displays alert", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <RequestReset authClient={client} />
      </BrowserRouter>,
    );

    await waitForUserFormSubmission(FakeUsers.Valid, client.requestReset);

    expect(window.alert).toHaveBeenCalledTimes(1);
  });

  it("Unsuccessful reset request displays message", async () => {
    const client = new FakeAuthClient();
    render(
      <BrowserRouter>
        <RequestReset authClient={client} />
      </BrowserRouter>,
    );

    await waitForUserFormSubmission(FakeUsers.Invalid, client.requestReset);

    expect(
      screen.queryByText(/email no pertenece a ninguna cuenta/),
    ).toBeInTheDocument();
  });
});
