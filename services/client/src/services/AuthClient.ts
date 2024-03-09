interface Response {
  statusCode: number;
  message?: string;
}

export interface LoginResponse extends Response {
  token: string;
}

export abstract class AbstractAuthClient {
  abstract login(user: string, password: string): Promise<LoginResponse>;
}

export class AuthClient extends AbstractAuthClient {
  async login(user: string, password: string): Promise<LoginResponse> {
    console.log(user, password);
    return {
      statusCode: 200,
      message: "Login in mother fuckers",
      token: "token",
    };
  }
}
