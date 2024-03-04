import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { StationsList } from "./StationsList.jsx";


describe("StationsTable", () => {
    it("renders all stations", () => {
        expect(screen.queryAllByRole("link").length).toBe(0);
        render(<StationsList />);
        // Each station should have a link. In total there must be 42 stations links +
        // navbar home link
        expect(screen.queryAllByRole("button").length).toBe(43);
        expect(screen.queryByText("C166")).toBeInTheDocument();
        expect(screen.queryByText("S160")).toBeInTheDocument();
    });
});
