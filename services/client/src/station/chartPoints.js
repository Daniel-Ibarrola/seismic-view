import {COUNT_TO_GALS, UNITS, UNIT_DATA} from "../data/index.js";


export const parseMessage = (message) => {
    return JSON.parse(message);
};

export const getLabels = (count) => {
    return [...Array(count).keys()].map(num => (num + 1).toString());
};


export const COLORS = {
        min: {
            borderColor: 'rgb(203, 67, 53)',
            backgroundColor: 'rgba(203, 67, 53, 0.5)',
        },
        max: {
            borderColor: 'rgb(46, 134, 193)',
            backgroundColor: 'rgb(46, 134, 193, 0.5)',
        },
        mean: {
            borderColor: 'rgb(40, 180, 99)',
            backgroundColor: 'rgb(40, 180, 99, 0.5)',
        },
        trace: {
            borderColor: 'rgb(214, 137, 16)',
            backgroundColor: 'rgb(214, 137, 16, 0.5)',
        }
};


export const getChannelDataSets = (
    unit,
    minData = [],
    maxData = [],
    meanData = [],
    traceData = [],
) => {

    const unitName = UNIT_DATA[unit].name;
    if (!unitName)
        throw Error(`Undefined unit ${unitName}`);

    const dataSets = [];
    if (minData.length > 0) {
        dataSets.push({
            label: `Min (${unitName})`,
            data: minData,
            borderColor: COLORS.min.borderColor,
            backgroundColor: COLORS.min.backgroundColor,
            borderWidth: 1,
            pointRadius: 0
        });
    }
    if (maxData.length > 0) {
        dataSets.push({
            label: `Max (${unitName})`,
            data: maxData,
            borderColor: COLORS.max.borderColor,
            backgroundColor: COLORS.max.backgroundColor,
            borderWidth: 1,
            pointRadius: 0
        });
    }
    if (meanData.length > 0) {
        dataSets.push({
            label: `Promedio (${unitName})`,
            data: meanData,
            borderColor: COLORS.mean.borderColor,
            backgroundColor: COLORS.mean.backgroundColor,
            borderWidth: 1,
            pointRadius: 0
        });
    }
    if (traceData.length > 0) {
        dataSets.push({
            label: `Traza (${unitName})`,
            data: traceData,
            borderColor: COLORS.trace.borderColor,
            backgroundColor: COLORS.trace.backgroundColor,
            borderWidth: 1,
            pointRadius: 0
        });
    }
    return dataSets;
};

export const chartOptions = (title, yMin=-1, yMax=1) => {
    return {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: title,
            },
        },
        scales: {
            x: {
                display: false,
            },
            y: {
                grid: {
                    display: false
                },
                min: yMin,
                max: yMax
            }
        }
    };
};


export const initialChartPoints = () => {
    return {
        min: [],
        max: [],
        mean: [],
        trace: [],
        index: 0,
    };
};


export const addPoint = (prevPoints, newPoint, isSet) => {
    // Add a point to the array if the option is set
    if (isSet) {
        return [...prevPoints, newPoint];
    }
    return [];
};

export const addPointsWithRep = (prevPoints, newPoint, count, isSet) => {
    // Add a point for "count" times to the array if isSet is true
    if (isSet) {
        const repeated = Array.from({ length: count}, () => newPoint);
        return [...prevPoints, ...repeated];
    }
    return [];
};

export const replacePoint = (prevPoints, newPoint, index, isSet) => {
    // Replace a point in the array if isSet is true
    if (isSet) {
        const newPointsArr = [...prevPoints];
        newPointsArr[index] = newPoint;
        return newPointsArr;
    }
    return [];
}

export const insertAndReplace = (prevPoints, newPoints, maxPoints, index) => {
    // Replace multiple points in the array if the option is set
    const updated = [...prevPoints];
    let ii = 0;
    if (prevPoints.length < maxPoints){
        while (updated.length < maxPoints && ii < newPoints.length){
            updated.push(newPoints[ii]);
            ii++;
        }
        index = 0;
    }
    for (; ii < newPoints.length; ii++){
        if (index === maxPoints){
            index = 0;
        }
        updated[index] = newPoints[ii];
        index++;
    }
    return {
        data: updated,
        index: index
    };
};

export const insertAndReplaceWithRep = (prevPoints, newPoint, count, maxPoints, index, isSet) => {
    if (isSet) {
        const repeated = Array.from(
            { length: count}, () => newPoint);
        return insertAndReplace(prevPoints, repeated, maxPoints, index).data;
    }
    return [];
};

export const convertUnits = (newData, units, station) => {
    if (units === UNITS.COUNTS) {
        return newData;
    }
    else if (units === UNITS.GALS) {
        const convFactor = COUNT_TO_GALS[station];
        return {
            ...newData,
            min: newData.min * convFactor,
            max: newData.max * convFactor,
            mean: newData.mean * convFactor,
            trace: newData.trace.map(it => it * convFactor),
        };
    }
    else {
        throw new Error();
    }
};

export const updateChart = (
    prevPoints,
    newData,
    options,
    channel,
    station,
    maxPoints=50,
    units= UNITS.GALS
) => {
    newData = convertUnits(newData, units, station);

    if (newData.channel === channel) {
        const traceSet = options.trace;
        const length = Math.max(
            prevPoints.min.length,
            prevPoints.max.length,
            prevPoints.mean.length,
            prevPoints.trace.length
        );
        if (length < maxPoints && !traceSet) {
            // Append new points to the end of array
            return {
                min: addPoint(prevPoints.min, newData.min, options.min),
                max: addPoint(prevPoints.max, newData.max, options.max),
                mean: addPoint(prevPoints.mean, newData.mean, options.mean),
                trace: [],
                index: prevPoints.index + 1,
            }
        } else if (length === maxPoints && !traceSet) {
            // Replace old points with new ones
            let index = prevPoints.index;
            if (index >= maxPoints - 1){
                index = 0;
            }
            return {
                min: replacePoint(prevPoints.min, newData.min, index, options.min),
                max: replacePoint(prevPoints.max, newData.max, index, options.max),
                mean: replacePoint(prevPoints.mean, newData.mean, index, options.mean),
                trace: [],
                index: index + 1,
            }

        } else if (length + newData.trace.length < maxPoints) {
            // Append points with repetition
            const count = newData.trace.length;
            return {
                min: addPointsWithRep(prevPoints.min, newData.min, count, options.min),
                max: addPointsWithRep(prevPoints.max, newData.max, count, options.max),
                mean: addPointsWithRep(prevPoints.mean, newData.mean, count, options.mean),
                trace: [...prevPoints.trace, ...newData.trace],
                index: prevPoints.index + newData.trace.length,
            };
        } else if (length + newData.trace.length >= maxPoints) {
            // Replace and/or insert new points
            const count = newData.trace.length;
            const index = prevPoints.index
            const trace = insertAndReplace(prevPoints.trace, newData.trace, maxPoints, index)
            return {
                min: insertAndReplaceWithRep(
                    prevPoints.min, newData.min, count, maxPoints, index, options.min
                ),
                max: insertAndReplaceWithRep(
                    prevPoints.max, newData.max, count, maxPoints, index, options.max
                ),
                mean: insertAndReplaceWithRep(
                    prevPoints.mean, newData.mean, count, maxPoints, index, options.mean
                ),
                trace: trace.data,
                index: trace.index,
            }
        } else {
            throw new Error();
        }
    }
    return {...prevPoints};
}