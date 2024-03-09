import React from "react";
import { AbstractAuthClient } from "../services/AuthClient.ts";

type Props = {
  authClient: AbstractAuthClient;
};

export const Login: React.FC<Props> = () => {
  return <h1>Login Page</h1>;
};
