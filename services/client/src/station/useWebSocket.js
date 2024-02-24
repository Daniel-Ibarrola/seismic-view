import {useEffect, useRef, useReducer, useState} from "react";
import {initialChartPoints, parseMessage, updateChart} from "./chartPoints.js";
import { actions, stationChartReducer } from "./state/index.js";
import {UNITS, UNIT_DATA} from "../data/index.js";


export const useWebSocket = (
    url, selectedStation, selectedChannel, options,
) => {

    const [socket, setSocket] = useState(null);
    const [socketReady, setSocketReady] = useState(false);
    const [timeInterval, setTimeInterval] = useState(100 * 10);
    const [stationData, dispatchStationData] = useReducer(
        stationChartReducer,
        {
            station: selectedStation,
            channel: selectedChannel,
            chartPoints: initialChartPoints(),
            units: UNITS.GALS,
            options: options,
            accelMin: UNIT_DATA[UNITS.GALS].min,
            accelMax: UNIT_DATA[UNITS.GALS].step
        }
    );

    const pointsRef = useRef(stationData.chartPoints);
    const optionsRef = useRef(stationData.options);
    const stationRef = useRef(stationData.station);
    const channelRef = useRef(stationData.channel);
    const unitsRef = useRef(stationData.units);
    const timeRef = useRef(timeInterval);

    useEffect(() => {
        pointsRef.current = stationData.chartPoints
    }, [stationData.chartPoints]);

    useEffect(() => {
        optionsRef.current = stationData.options
    }, [stationData.options]);

    useEffect(() => {
        channelRef.current = stationData.channel
    }, [stationData.channel]);

    useEffect(() => {
        if (socket !== null && socket.readyState === WebSocket.OPEN){
            socket.close();
            dispatchStationData({
                type: actions.SET_POINTS,
                payload: initialChartPoints(),
            });
        }
        setSocket(new WebSocket(url));
        return () => {
            if (socket !== null) {
                socket.close();
            }
        }
    }, [stationData.station]);

    useEffect(() => {
        const onOpen = (event) => {
            console.log("Socket connected");
            setSocketReady(true);
            socket.send(stationData.station);
        };
        const onClose = (event) => {
            console.log("Socket closed");
            setSocketReady(false);
        };
        const onError = (event) => {
            console.log("Error: ", event);
            setSocketReady(false);
        };

        const messageListener = (event) => {
            processData(event.data);
        };

        if (socket !== null) {
            socket.addEventListener("open", onOpen);
            socket.addEventListener("close", onClose);
            socket.addEventListener("error", onError);
            socket.addEventListener("message", messageListener);
        }
        return () => {
            if (socket !== null){
                socket.removeEventListener("open", onOpen);
                socket.removeEventListener("close", onClose);
                socket.removeEventListener("error", onError);
                socket.removeEventListener("message", messageListener);
            }
        };
    }, [socket]);

    const processData = (message) => {
        const newData = parseMessage(message);
        if (newData.station === stationData.station
            && newData.channel === channelRef.current) {
            // console.log(channelRef.current);
            const newPoints = updateChart(
                pointsRef.current,
                newData,
                optionsRef.current,
                channelRef.current,
                stationRef.current,
                timeRef.current,
                unitsRef.current,
            );
            dispatchStationData({
                type: actions.SET_POINTS,
                payload: newPoints,
            });
        }
    };

    const onStationClick = (name) => {
        dispatchStationData({
            type: actions.SET_STATION,
            payload: name
        });
    };

    const onChannelClick = (name) => {
        dispatchStationData({
            type: actions.SET_CHANNEL,
            payload: name
        });
    };

    const onOptionClick = (option) => {
        dispatchStationData({
            type: actions.SET_OPTION,
            payload: option
        });
    };

    const onUnitClick = (unit) => {
        dispatchStationData({
            type: actions.SET_UNIT,
            payload: unit,
        });
        unitsRef.current = unit;
    }

    const onTimeIntervalChange = (event, interval) => {
        // 10 samples per second. Multiply by 10 to obtain seconds
        setTimeInterval(interval * 10);
        dispatchStationData({
            type: actions.SET_POINTS,
            payload: initialChartPoints()
        })
        timeRef.current = interval * 10;
    }

    const onAccelChange = (event, newAccel) => {
        dispatchStationData({
           type: actions.SET_ACCEL,
           payload: newAccel,
        });
    }

    return [
        socketReady,
        stationData,
        timeInterval,
        onStationClick,
        onChannelClick,
        onOptionClick,
        onUnitClick,
        onTimeIntervalChange,
        onAccelChange
    ];
};
