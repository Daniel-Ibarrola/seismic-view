import {UNIT_DATA} from "../../data/index.js";

export const actions = {
    SET_OPTION: 0,
    SET_CHANNEL: 1,
    SET_STATION: 2,
    SET_POINTS: 3,
    SET_UNIT: 4,
    SET_ACCEL: 5
};

const restorePoints = () => {
    return {
        min: [],
        max: [],
        mean: [],
        trace: [],
        index: 0,
    }
}

export const stationChartReducer = (state, action) => {
    switch (action.type) {
        case actions.SET_OPTION:
            return {
                ...state,
                chartPoints: restorePoints(),
                options: {
                    ...state.options,
                    ...action.payload
                }
            };
        case actions.SET_CHANNEL:
            if (state.channel === action.payload){
                return {
                    ...state
                };
            }
            return {
                ...state,
                channel: action.payload,
                chartPoints: restorePoints(),
            };
        case actions.SET_STATION:
            if (state.station === action.payload){
                return {
                    ...state
                };
            }
            return {
                ...state,
                station: action.payload,
                chartPoints: restorePoints(),
            };
        case actions.SET_POINTS:
            return {
                ...state,
                chartPoints: action.payload,
            };
        case actions.SET_UNIT:
            return {
                ...state,
                units: action.payload,
                chartPoints: restorePoints(),
                accelMin: UNIT_DATA[action.payload].min,
                accelMax: UNIT_DATA[action.payload].step
            };
        case actions.SET_ACCEL:
            return {
                ...state,
                accelMin: -1 * action.payload,
                accelMax: action.payload
            }
        default:
            throw new Error();
    }
};
