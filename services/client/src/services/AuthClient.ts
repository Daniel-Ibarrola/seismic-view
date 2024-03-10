export interface AuthResponse {
  statusCode: number;
  message?: string;
  token?: string;
}

export abstract class AbstractAuthClient {
  abstract login(user: string, password: string): Promise<AuthResponse>;
}

export class AuthClient extends AbstractAuthClient {
  async login(user: string, password: string): Promise<AuthResponse> {
    console.log(user, password);
    return {
      statusCode: 200,
      message: "Login in mother fuckers",
      token: "token",
    };
  }
}
