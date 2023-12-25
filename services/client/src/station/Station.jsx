import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

import { WebsocketUri } from "../api.js";
import { getLabels, chartOptions, getChannelDataSets } from "./chartPoints.js";
import { useWebSocket } from "./useWebSocket.js";
import { StationOptions } from "../stationOptions/index.js";
import { FailAlert } from "../alerts/alerts.jsx";
import "./style.css";
import {StationsList} from "../stationsList/index.js";


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const defaultOptions = {
    min: false,
    max: false,
    mean: false,
    trace: true,
};


const StationChart = ({ points, channel, units, timeInterval, accelMin, accelMax }) => {
    const options = chartOptions(
        channel, accelMin, accelMax);
    const labels = getLabels(timeInterval);
    const dataSet = {
        labels: labels,
        datasets: getChannelDataSets(
            units, points.min, points.max, points.mean, points.trace
        ),
    };

    return (
        <Card className="station-card">
            <Card.Body>
                <Line
                    data={dataSet}
                    options={options}
                />
            </Card.Body>
        </Card>
    );
};




const Station = () => {

    console.debug("API URL " + WebsocketUri);
    const [
        socketReady,
        stationData,
        timeInterval,
        onStationClick,
        onChannelClick,
        onOptionClick,
        onUnitClick,
        onTimeIntervalChange,
        onAccelChange
    ] = useWebSocket(
        WebsocketUri,
        "C166",
        "HLZ",
        defaultOptions,
        );


    return (
        <>
            <Container>
                <Row>
                    <Col md={3}>
                        <StationsList
                            onStationClick={onStationClick}
                        />
                    </Col>
                    <Col>
                        <Row>
                            <h2>{stationData.station}</h2>
                        </Row>
                        <Row>
                            {!socketReady &&
                                <FailAlert >
                                    <strong>Fallo la conexión!</strong>
                                </FailAlert>
                            }
                            {socketReady &&
                                <StationChart
                                    points={stationData.chartPoints}
                                    channel={stationData.channel}
                                    units={stationData.units}
                                    timeInterval={timeInterval}
                                    accelMin={stationData.accelMin}
                                    accelMax={stationData.accelMax}
                                />
                            }
                        </Row>
                        <Row>
                            <StationOptions
                                station={stationData.station}
                                stationOptions={stationData.options}
                                units={stationData.units}
                                onChannelClick={onChannelClick}
                                onOptionClick={onOptionClick}
                                onUnitClick={onUnitClick}
                                onTimeChange={onTimeIntervalChange}
                                onAccelChange={onAccelChange}
                            />
                        </Row>
                    </Col>
                </Row>
            </Container>
        </>

    );
};

export { Station };
