import axios from "axios";
import { describe, expect, it, vi } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { Login } from "../Login.jsx";
import { localStorageMock } from "../../test/mocks.ts";

Object.defineProperty(window, "localStorage", { value: localStorageMock });

vi.mock("axios", () => ({
  post: vi.fn(),
}));

interface SuccessResponse {
  data: { token: string; expiration: number };
}

describe("Login", () => {
  const rejectedPromise = (statusCode: number): Promise<never> => {
    return Promise.reject({
      response: {
        status: statusCode,
      },
    });
  };

  const successPromise = (): Promise<SuccessResponse> => {
    return Promise.resolve({
      data: {
        token: "FakeToken",
        expiration: 3600,
      },
    });
  };

  const waitForFormSubmission = async (
    promise: Promise<never | SuccessResponse>,
  ): Promise<void> => {
    fireEvent.change(screen.getByPlaceholderText("Email"), {
      target: { value: "triton@example.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
      target: { value: "6MonkeysRLooking^" },
    });
    fireEvent.click(screen.getAllByRole("button")[0]);
    await waitFor(async () => await promise);
  };

  it("Successful login redirects to stations page", async () => {
    const promise = successPromise();
    vi.spyOn(axios, "post").mockImplementationOnce(() => promise);

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );
    expect(screen.queryAllByText(/Iniciar/)[0]).toBeInTheDocument();

    const button = screen.queryByRole("button");
    expect(button).not.toBeNull();

    await waitFor(async () => fireEvent.click(button as HTMLElement));
    await waitFor(async () => await promise);

    const token = window.localStorage.getItem("token");
    expect(token).not.toBeNull();
    expect(token).toBe("FakeToken");
  });

  it("Invalid credentials display error", async () => {
    const promise = rejectedPromise(401);
    vi.spyOn(axios, "post").mockImplementationOnce(() => promise);

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    try {
      await waitForFormSubmission(promise);
    } catch (error) {
      expect(
        screen.queryByText(/Usuario o contraseña inválidos/),
      ).toBeInTheDocument();
    }
  });

  it("Unconfirmed user displays re-send confirmation link", async () => {
    const promise = rejectedPromise(400);
    vi.spyOn(axios, "post").mockImplementationOnce(() => promise);

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    try {
      await waitForFormSubmission(promise);
    } catch (error) {
      expect(screen.queryByText(/no confirmado/)).toBeInTheDocument();
      expect(
        screen.queryByText(/reenviar email de confirmación/),
      ).toBeInTheDocument();
    }
  });
});
