import React from "react";
import { AbstractAuthClient } from "../services/AuthClient.ts";

type Props = {
  authClient: AbstractAuthClient;
};

export const RequestReset: React.FC<Props> = () => {
  return <h1>Request Reset</h1>;
};
