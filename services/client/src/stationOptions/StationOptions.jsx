import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import FormGroup from "@mui/material/FormGroup";
import Checkbox from "@mui/material/Checkbox";
import Slider from "@mui/material/Slider";

import {STATIONS} from "../data/stations.js";
import {UNITS, UNIT_DATA} from "../data/index.js";
import "./style.css";


const AccelSlider = ({ units, onAccelChange }) => {
    return (
        <Slider
            min={UNIT_DATA[units].step}
            max={UNIT_DATA[units].max}
            step={UNIT_DATA[units].step}
            defaultValue={UNIT_DATA[units].min}
            valueLabelDisplay="auto"
            onChange={onAccelChange}
            key={units}
            marks
        />
    );
};

const StationOptions = (
    {
        station,
        stationOptions,
        units,
        onOptionClick,
        onChannelClick,
        onAccelChange,
        onTimeChange,
        onUnitClick
    }) => {
    const channels = STATIONS.find(st => st.name === station).channels;

    return (
        <Card className="station-card">
            <Card.Body>
                <h3 className="options-title">
                    Opciones
                </h3>
                <Container>
                    <Row>
                        <Col>
                            <FormControl>
                                <FormLabel id="radio-buttons-channel">Canal</FormLabel>
                                <RadioGroup
                                    aria-labelledby="radio-buttons-channel"
                                    defaultValue={channels[0]}
                                    name="channel-buttons-group"
                                >
                                    {channels &&
                                        channels.map(ch =>
                                            <FormControlLabel
                                                control={<Radio />}
                                                key={ch}
                                                label={ch}
                                                value={ch}
                                                onClick={() => onChannelClick(ch)}
                                            />
                                        )
                                    }
                                </RadioGroup>
                            </FormControl>
                        </Col>
                        <Col>
                            <FormControl>
                                <FormLabel id="radio-units-buttons">Unidades</FormLabel>
                                <RadioGroup
                                    aria-labelledby="radio-units-buttons"
                                    defaultValue="gals"
                                    name="units-buttons-group"
                                >
                                    <FormControlLabel
                                        value="gals"
                                        control={<Radio />}
                                        label="Gals"
                                        onClick={() => onUnitClick(UNITS.GALS)}
                                    />
                                    <FormControlLabel
                                        value="counts"
                                        control={<Radio />}
                                        label="Cuentas"
                                        onClick={() => onUnitClick(UNITS.COUNTS)}
                                    />
                                </RadioGroup>
                            </FormControl>
                        </Col>
                    </Row>
                    <Row>
                        <p className="slider-title">Ver</p>
                        <FormGroup row>
                            <FormControlLabel
                                control={<Checkbox />}
                                label="Máximo"
                                onChange={() => onOptionClick({max: !stationOptions.max})}
                            />
                            <FormControlLabel
                                control={<Checkbox />}
                                label="Media"
                                onChange={() => onOptionClick({mean: !stationOptions.mean})}
                            />
                            <FormControlLabel
                                control={<Checkbox />}
                                label="Mínimo"
                                onChange={() => onOptionClick({min: !stationOptions.min})}
                            />
                            <FormControlLabel
                                control={<Checkbox defaultChecked/>}
                                label="Traza"
                                onChange={() => onOptionClick({trace: !stationOptions.trace})}
                            />
                        </FormGroup>
                    </Row>
                    <Row>
                        <p className="slider-title">Intervalo tiempo (segundos)</p>
                        <Slider
                            min={100}
                            max={1000}
                            step={100}
                            defaultValue={100}
                            valueLabelDisplay="auto"
                            onChange={onTimeChange}
                            marks
                        />
                    </Row>
                    <Row>
                        <p className="slider-title">
                            Intervalo aceleración ({UNIT_DATA[units].name})
                        </p>
                        {units === UNITS.GALS ?
                            <AccelSlider units={UNITS.GALS} onAccelChange={onAccelChange} />
                            :
                            <AccelSlider units={UNITS.COUNTS} onAccelChange={onAccelChange} />
                        }
                    </Row>
                </Container>
            </Card.Body>
        </Card>
    )
};

export { StationOptions };