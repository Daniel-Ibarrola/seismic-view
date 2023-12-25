import {describe, expect, it} from "vitest";
import {actions, stationChartReducer} from "./stationChartReducer.js";
import {UNITS, UNIT_DATA} from "../../data/index.js";


describe("stationChartReducer", () => {

    const points = {
        min: [1],
        max: [3],
        mean: [],
        trace: [],
        index: 1,
    };

    const emptyPoints = {
        min: [],
        max: [],
        mean: [],
        trace: [],
        index: 0,
    }

    const initialState = {
        station: "C166",
        channel: "HLZ",
        chartPoints: points,
        units: UNITS.COUNTS,
        options: {
            min: true,
            max: true,
            mean: false,
            trace: false,
        },
        accelMin: -1,
        accelMax: 1
    };

    it("Setting option reset points", () => {
        const action = {
            type: actions.SET_OPTION, payload: {mean: true}
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: emptyPoints,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: true,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting same channel doesn't alter state", () => {
        const action = {
            type: actions.SET_CHANNEL, payload: "HLZ"
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: points,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting different channel reset points", () => {
        const action = {
            type: actions.SET_CHANNEL, payload: "HLN"
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLN",
            chartPoints: emptyPoints,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting same station doesn't alter", () => {
        const action = {
            type: actions.SET_STATION, payload: "C166"
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: points,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Setting different station reset points", () => {
        const action = {
            type: actions.SET_STATION, payload: "S160"
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "S160",
            channel: "HLZ",
            chartPoints: emptyPoints,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Set chart points", () => {
        const points = {
            min: [1, -1.2],
            max: [3, 2.3],
            mean: [],
            trace: [],
            index: 2,
        };
        const action = {
            type: actions.SET_POINTS, payload: points
        };
        const newState = stationChartReducer(initialState, action);

        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: points,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -1,
            accelMax: 1
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Sets unit reset points", () => {
        const action = {
            type: actions.SET_UNIT, payload: UNITS.GALS
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: emptyPoints,
            units: UNITS.GALS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: UNIT_DATA[UNITS.GALS].min,
            accelMax: UNIT_DATA[UNITS.GALS].step
        };
        expect(newState).toStrictEqual(expectedState);
    });

    it("Set acceleration min and max", () => {
        const action = {
            type: actions.SET_ACCEL, payload: 100
        };
        const newState = stationChartReducer(initialState, action);
        const expectedState = {
            station: "C166",
            channel: "HLZ",
            chartPoints: points,
            units: UNITS.COUNTS,
            options: {
                min: true,
                max: true,
                mean: false,
                trace: false,
            },
            accelMin: -100,
            accelMax: 100
        };
        expect(newState).toStrictEqual(expectedState);
    });
});