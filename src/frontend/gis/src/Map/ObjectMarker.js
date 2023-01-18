import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import PercentIcon from '@mui/icons-material/Percent';
import FaceRetouchingOffIcon from '@mui/icons-material/FaceRetouchingOff'
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "country", label: "Country", Icon: FlagIcon},
    {"key": "med_tax", label: "Medium tax of suicides", Icon: PercentIcon},
    {"key": "suicides_no", label: "Nº of suicides", Icon: FaceRetouchingOffIcon}
];

export function ObjectMarker({geoJSON}) {
    //debugger
    const properties = geoJSON.properties
    console.log(properties)
    const {id, imgurl, name} = properties;
    const coordinates = [geoJSON.geometry.coordinates[1],geoJSON.geometry.coordinates[0]];


    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgurl,
                iconRetinaUrl: imgurl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgurl}/>
                        </ListItemIcon>
                        <ListItemText primary={name}/>
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
                                        {properties[key]}<br/>
                                        <label style={{fontSize: "xx-small"}}>({label})</label>
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