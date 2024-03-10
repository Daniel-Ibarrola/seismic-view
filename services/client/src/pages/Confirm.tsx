import React from "react";
import { AbstractAuthClient } from "../services/AuthClient.ts";

type Props = {
  authClient: AbstractAuthClient;
};

export const Confirm: React.FC<Props> = () => {
  return <h1>Confirm Page</h1>;
};
