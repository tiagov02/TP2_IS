import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import HomeIcon from '@mui/icons-material/Home';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";


const LIST_PROPERTIES = [
    {"key": "home", Icon: HomeIcon},
    ];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties
    const { img, home} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: img,
                iconRetinaUrl: img,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={home} src={img}/>
                        </ListItemIcon>
                        <ListItemText primary={home}/>
                    </ListItem>
                    {
                        LIST_PROPERTIES
                            .map(({key, label, Icon}) =>
                                <ListItem key={key}>
                                    <ListItemIcon>
                                        <Icon style={{color: "black"}}/>
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={<span>
                                        {properties[key]}

                                    </span>}
                                    />
                                </ListItem>
                            )
                    }
                </List>
            </Popup>
        </Marker>
    )
}