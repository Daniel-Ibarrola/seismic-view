import React from "react";
import { AbstractAuthClient } from "../services/AuthClient.ts";

type Props = {
  authClient: AbstractAuthClient;
};

export const Reset: React.FC<Props> = () => {
  return <h1>Reset Page</h1>;
};
