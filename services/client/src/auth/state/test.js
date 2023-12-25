import {describe, expect, it} from "vitest";
import {actions, formReducer} from "./formReducer.js";


describe("loginReducer", () => {
    it("Sets email", () => {
        const initialState = {
            email: "",
            password: "dog",
            isError: false,
            errorMsg: "",
        };
        const newState = formReducer(initialState, {
            type: actions.setEmail,
            payload: "triton@example.com"
        });

        const expectedState = {
            email: "triton@example.com",
            password: "dog",
            isError: false,
            errorMsg: "",
        }
        expect(newState).toStrictEqual(expectedState);
    });

    it("Sets password", () => {
        const initialState = {
            email: "triton@example.com",
            password: "",
            isError: false,
            errorMsg: "",
        };
        const newState = formReducer(initialState, {
            type: actions.setPassword,
            payload: "dog"
        });

        const expectedState = {
            email: "triton@example.com",
            password: "dog",
            isError: false,
            errorMsg: "",
        }
        expect(newState).toStrictEqual(expectedState);
    });

    it("login success", () => {
        const initialState = {
            email: "triton@example.com",
            password: "dog",
            isError: false,
            errorMsg: "",
        };
        const newState = formReducer(initialState, {
            type: actions.successLogin
        });

        const expectedState = {
            email: "",
            password: "",
            isError: false,
            errorMsg: "",
        }
        expect(newState).toStrictEqual(expectedState);
    });

    it("login fail", () => {
        const initialState = {
            email: "triton@example.com",
            password: "dog",
            isError: false,
            errorMsg: "",
        };
        const newState = formReducer(initialState, {
            type: actions.errorLogin,
            payload: "Usuario o contraseña invalidos"
        });

        const expectedState = {
            email: "",
            password: "",
            isError: true,
            errorMsg: "Usuario o contraseña invalidos",
        };
        expect(newState).toStrictEqual(expectedState);
    });
});
