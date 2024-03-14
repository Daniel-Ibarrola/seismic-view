import { fireEvent, screen, waitFor } from "@testing-library/react";
import { AuthResponse } from "../../services/AuthClient.ts";

export const waitForAuthFormSubmission = async (
  user: string,
  password: string,
  promise: (user: string, password: string) => Promise<AuthResponse>,
): Promise<void> => {
  // Submit login, register, confirm forms
  fireEvent.change(screen.getByPlaceholderText("Email"), {
    target: { value: user },
  });
  fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
    target: { value: password },
  });
  fireEvent.click(screen.getAllByRole("button")[0]);
  await waitFor(async () => promise);
};

export const waitForPasswordFormSubmission = async (
  password: string,
  promise: (password: string) => Promise<AuthResponse>,
): Promise<void> => {
  // Submit password for reset form
  fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
    target: { value: password },
  });
  fireEvent.click(screen.getByRole("button"));
  await waitFor(async () => promise);
};

export const waitForUserFormSubmission = async (
  user: string,
  promise: (password: string) => Promise<AuthResponse>,
): Promise<void> => {
  // Submit user for request reset form
  fireEvent.change(screen.getByPlaceholderText("Email"), {
    target: { value: user },
  });
  fireEvent.click(screen.getByRole("button"));
  await waitFor(async () => promise);
};
