import Card from "react-bootstrap/Card";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { STATIONS } from "../data/stations.js";
import "./style.css";

const StationsList = ({ onStationClick }) => {
    return (
        <Card className="station-card">
            <Card.Header>
                Estaciones
            </Card.Header>
            <List
                className="station-list"
                style={{maxHeight: '20rem', overflow: 'auto'}}
            >
                {STATIONS.map(st => (
                    <ListItem key={st.name}>
                        <ListItemButton onClick={() => onStationClick(st.name)}>
                            <ListItemText primary={st.name} />
                        </ListItemButton>
                    </ListItem>)
                )
                }
            </List>
        </Card>

    );
};

export { StationsList };
