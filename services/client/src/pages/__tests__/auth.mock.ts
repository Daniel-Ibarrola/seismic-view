import { AbstractAuthClient, AuthResponse } from "../../services/AuthClient.ts";

export enum FakeUsers {
  Invalid = "Invalid",
  Valid = "Valid",
  Unconfirmed = "Unconfirmed",
  Error = "Error",
  InUse = "InUse",
}

export class FakeAuthClient extends AbstractAuthClient {
  async login(user: string, password: string): Promise<AuthResponse> {
    void password;
    if (user === FakeUsers.Invalid) {
      return {
        token: "",
        statusCode: 403,
        message: "Invalid username or password",
      };
    } else if (user === FakeUsers.Unconfirmed) {
      return {
        token: "",
        statusCode: 401,
        message: "User is not confirmed",
      };
    } else if (user === FakeUsers.Valid) {
      return {
        token: "FakeToken",
        statusCode: 200,
        message: "Login successful",
      };
    } else {
      throw new Error("Invalid user");
    }
  }
}
