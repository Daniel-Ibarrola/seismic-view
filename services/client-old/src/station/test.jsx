import { describe, expect, it } from "vitest";
import {
    addPoint,
    addPointsWithRep,
    convertUnits,
    getChannelDataSets,
    getLabels,
    insertAndReplace,
    insertAndReplaceWithRep,
    parseMessage,
    replacePoint,
    updateChart,
    COLORS,
} from "./chartPoints.js";
import {COUNT_TO_GALS, UNITS} from "../data/index.js";

describe("parseMessage", () => {
    it("parses data correctly", () => {
        const message = `{"min": -1.2, "max": 2.3, "mean": 6.4,
         "station": "C166", "channel": "HLN", "trace": [1, 2, 3]}`;
        const result = parseMessage(message);
        const expected = {
            min: -1.2,
            max: 2.3,
            mean: 6.4,
            station: "C166",
            channel: "HLN",
            trace: [1, 2, 3],
        };
        expect(result).toStrictEqual(expected);
    });
});


describe("getLabels", () => {
    it("gets correct labels", () => {
        const result = getLabels(5);
        expect(result).toStrictEqual(["1", "2", "3", "4", "5"]);
    });
});


describe("getChannelDatasets", () => {
    it("only min", () => {
        const minData = [1, 2, 3];
        const datasets = getChannelDataSets(UNITS.GALS, minData);
        expect(datasets).toStrictEqual([
           {
               label: "Min (Gals)",
               data: minData,
               borderColor: COLORS.min.borderColor,
               backgroundColor: COLORS.min.backgroundColor,
               borderWidth: 1,
               pointRadius: 0
           }
        ]);
    });

    it("only max", () => {
        const maxData = [1, 2, 3];
        const datasets = getChannelDataSets(UNITS.GALS, [], maxData);
        expect(datasets).toStrictEqual([
            {
                label: "Max (Gals)",
                data: maxData,
                borderColor: COLORS.max.borderColor,
                backgroundColor: COLORS.max.backgroundColor,
                borderWidth: 1,
                pointRadius: 0
            }
        ]);
    });

    it("only mean", () => {
        const meanData = [1, 2, 3];
        const datasets = getChannelDataSets(
            UNITS.GALS, [], [], meanData);
        expect(datasets).toStrictEqual([
            {
                label: "Promedio (Gals)",
                data: meanData,
                borderColor: COLORS.mean.borderColor,
                backgroundColor: COLORS.mean.backgroundColor,
                borderWidth: 1,
                pointRadius: 0
            }
        ]);
    });

    it("only trace", () => {
        const traceData = [1, 2, 3];
        const datasets = getChannelDataSets(
            UNITS.GALS, [], [], [], traceData);
        expect(datasets).toStrictEqual([
            {
                label: "Traza (Gals)",
                data: traceData,
                borderColor: COLORS.trace.borderColor,
                backgroundColor: COLORS.trace.backgroundColor,
                borderWidth: 1,
                pointRadius: 0
            }
        ]);
    });
})

describe("updateChart", () => {
    const initialPoints = {
        min: [],
        max: [],
        mean: [],
        trace: [],
        index: 0,
    };
    const newData = {
        min: -1.2,
        max: 2.3,
        mean: 6.4,
        station: "C166",
        channel: "HLN",
        trace: [1, 2, 3],
    };
    const options = {
        min: true,
        max: true,
        mean: true,
        trace: true,
    }

    it("Only updates if points are from selected channel", () => {
        const newPoints = updateChart(
            initialPoints, newData, options, "HLZ", "C166"
        );
        expect(newPoints).toStrictEqual({
            min: [],
            max: [],
            mean: [],
            trace: [],
            index: 0,
        });
    });

    it("Only updates set options", () => {
        const chartOptions = {
            ...options,
            mean: false,
            trace: false,
        };
        const newPoints = updateChart(
            initialPoints, newData, chartOptions,
            "HLN", "C166", 50, UNITS.COUNTS);
        expect(newPoints).toStrictEqual({
            min: [-1.2],
            max: [2.3],
            mean: [],
            trace: [],
            index: 1,
        });
    });

    it("If trace is set other values are upsampled to match num of points", () => {
        const newPoints = updateChart(
            initialPoints, newData, options,
            "HLN", "C166",50, UNITS.COUNTS);
        expect(newPoints).toStrictEqual({
            min: [-1.2, -1.2, -1.2],
            max: [2.3, 2.3, 2.3],
            mean: [6.4, 6.4, 6.4],
            trace: [1, 2, 3],
            index: 3,
        });
    });

    it("New points inserted at start if max capacity exceeded", () => {
        const chartOptions = {
            ...options,
            trace: false,
        };
        const prevPoints = {
            min: [1, 2],
            max: [3, 4],
            mean: [5, 6],
            trace: [],
            index: 2,
        };
        const newestData = {
            min: 3,
            max: 5,
            mean: 7,
            station: "C166",
            channel: "HLN",
            trace: [1, 2, 3],
        };

        const newPoints = updateChart(
            prevPoints, newestData, chartOptions,
            "HLN", "C166", 2, UNITS.COUNTS
        );
        expect(newPoints).toStrictEqual({
            min: [3, 2],
            max: [5, 4],
            mean: [7, 6],
            trace: [],
            index: 1,
        });
    });

    it("New points inserted at start if max capacity exceeded and trace option", () => {
        const prevPoints = {
            min: [1, 1],
            max: [3, 3],
            mean: [2, 2],
            trace: [1, 3],
            index: 2,
        };
        const newestData = {
            min: 4,
            max: 6,
            mean: 5,
            station: "C166",
            channel: "HLN",
            trace: [4, 6],
        };

        const newPoints = updateChart(
            prevPoints, newestData, options,
            "HLN", "C166", 3, UNITS.COUNTS);
        expect(newPoints).toStrictEqual({
            min: [4, 1, 4],
            max: [6, 3, 6],
            mean: [5, 2, 5],
            trace: [6, 3, 4],
            index: 1,
        });
    });
});


describe('addPoint', () => {
    it('should add a point to the array if isSet is true', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const isSet = true;

        const result = addPoint(prevPoints, newPoint, isSet);

        expect(result).toStrictEqual([1, 2, 3, 4]);
    });

    it('should return an empty array if isSet is false', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const isSet = false;

        const result = addPoint(prevPoints, newPoint, isSet);

        expect(result).toStrictEqual([]);
    });

    it('should return an empty array if prevPoints is empty and isSet is false', () => {
        const prevPoints = [];
        const newPoint = 4;
        const isSet = false;

        const result = addPoint(prevPoints, newPoint, isSet);

        expect(result).toStrictEqual([]);
    });
});

describe('addPointsWithRep', () => {
    it('should add the newPoint multiple times to the array if isSet is true', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const count = 3;
        const isSet = true;

        const result = addPointsWithRep(prevPoints, newPoint, count, isSet);

        expect(result).toStrictEqual([1, 2, 3, 4, 4, 4]);
    });

    it('should return an empty array if isSet is false', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const count = 3;
        const isSet = false;

        const result = addPointsWithRep(prevPoints, newPoint, count, isSet);

        expect(result).toStrictEqual([]);
    });

    it('should return an empty array if prevPoints is empty and isSet is false', () => {
        const prevPoints = [];
        const newPoint = 4;
        const count = 3;
        const isSet = false;

        const result = addPointsWithRep(prevPoints, newPoint, count, isSet);

        expect(result).toStrictEqual([]);
    });
});

describe('replacePoint', () => {
    it('should replace the point at the specified index if isSet is true', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const index = 1;
        const isSet = true;

        const result = replacePoint(prevPoints, newPoint, index, isSet);

        expect(result).toStrictEqual([1, 4, 3]);
    });

    it('should return an empty array if isSet is false', () => {
        const prevPoints = [1, 2, 3];
        const newPoint = 4;
        const index = 1;
        const isSet = false;

        const result = replacePoint(prevPoints, newPoint, index, isSet);

        expect(result).toStrictEqual([]);
    });

    it('should return an empty array if prevPoints is empty and isSet is false', () => {
        const prevPoints = [];
        const newPoint = 4;
        const index = 0;
        const isSet = false;

        const result = replacePoint(prevPoints, newPoint, index, isSet);

        expect(result).toStrictEqual([]);
    });
});


describe("insertAndReplace", () => {
    it("should insert new points if original array has not exceeded capacity", () => {
        const prevPoints = [1, 2, 3];
        const newPoints = [4, 5, 6];
        const maxPoints = 5
        const index = 2

        const result = insertAndReplace(prevPoints, newPoints, maxPoints, index);
        expect(result.data).toStrictEqual([6, 2, 3, 4, 5]);
        expect(result.index).toBe(1);
    });

    it("should only replace new points if original array has exceeded capacity", () => {
        const prevPoints = [1, 2, 3, 4, 5];
        const newPoints = [6, 7, 8];
        const maxPoints = 5
        const index = 3

        const result = insertAndReplace(prevPoints, newPoints, maxPoints, index);
        expect(result.data).toStrictEqual([8, 2, 3, 6, 7]);
        expect(result.index).toBe(1);
    });

});

describe('insertAndReplaceWithRep', () => {
    it('should replace multiple points with the new point if isSet is true', () => {
        const prevPoints = [1, 2, 3, 4, 5];
        const newPoint = 10
        const count = 3;
        const maxPoints = 5
        const index = 3
        const isSet = true;

        const result = insertAndReplaceWithRep(prevPoints, newPoint, count, maxPoints, index, isSet);
        expect(result).toStrictEqual([10, 2, 3, 10, 10]);
    });

    it('should return an empty array if isSet is false', () => {
        const prevPoints = [1, 2, 3, 4, 5];
        const newPoint = 6;
        const count = 2
        const maxPoints = 5
        const index = 3
        const isSet = false;

        const result = insertAndReplaceWithRep(prevPoints, newPoint, count, maxPoints, index, isSet);
        expect(result).toStrictEqual([]);
    });
});


describe("convertUnits", () => {
    const data = {
        min: -1000000,
        max: 1000000,
        mean: 500000,
        station: "C166",
        channel: "HLN",
        trace: [-1000000, 0, 1000000],
    }

    it("Counts should return the same data", () => {
        const result = convertUnits(data, UNITS.COUNTS, "C166");
        expect(result).toStrictEqual(data);
    });

    it("Gals should convert data", () => {
        const result = convertUnits(data, UNITS.GALS, "C166");
        const convFactor = COUNT_TO_GALS["C166"];
        expect(result).toStrictEqual({
            min: data.min * convFactor,
            max: data.max * convFactor,
            mean: data.mean * convFactor,
            station: "C166",
            channel: "HLN",
            trace: [
                data.trace[0] * convFactor,
                data.trace[1] * convFactor,
                data.trace[2] * convFactor,
            ],
        });
    });
})