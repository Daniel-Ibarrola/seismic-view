import React from "react";
import { AbstractAuthClient } from "../services/AuthClient.ts";

type Props = {
  authClient: AbstractAuthClient;
};

export const Register: React.FC<Props> = () => {
  return <h1>Register Page</h1>;
};
