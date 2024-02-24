import { describe, expect, it } from "vitest";
import { validateEmail, validatePassword } from "./validation.js";


describe("validateEmail", () => {

    it("No email", () => {
       expect(validateEmail("")).toBe("Requerido");
    });

    it("Invalid email", () => {
        expect(validateEmail("not-an-email")).toBe("Correo inválido")
    });

    it("Valid email", () => {
        expect(validateEmail("triton@example.com")).toBe("");
    })

});


describe("validatePassword", () => {

    it("No password", () => {
       expect(validatePassword("")).toBe("Requerido");
    });

    it("Small password", () => {
        expect(validatePassword("Dog$")).toBe("Entre 8 y 20 caractéres. ");
    })

    it("Very long password", () => {
        expect(
            validatePassword("6MonkeysRLooking^6MonkeysRLooking^6MonkeysRLooking^")
        ).toBe("Entre 8 y 20 caractéres. ");
    });

    it("No upper case", () => {
        expect(
            validatePassword("6monkeysrlooking^")
        ).toBe("Al menos una letra mayúscula. ");
    });

    it("No lower case", () => {
        expect(
            validatePassword(
                "6MONKEYSRLOOKIN$"
            )
        ).toBe("Al menos una letra minúscula. ");
    });

    it("Has spaces", () => {
        expect(
            validatePassword("6Monkeys R Looking^")
        ).toBe('No debe contener espacios. ');
    })

    it("No special characters", () => {
        expect(
            validatePassword("6MonkeysRLooking")
        ).toBe("Al menos un carácter especial. ")
    });

    it("Valid password", () => {
        expect(
            validatePassword("6MonkeysRLooking^")
        ).toBe("")
    });

});
