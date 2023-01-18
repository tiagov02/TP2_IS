import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "country", label: "Country", Icon: FlagIcon},
    {"key": "med_tax", label: "Medium tax of suicides", Icon: ContactsIcon},
    {"key": "suicides_no", label: "No of suicides«", Icon: PictureInPictureAltIcon}
];

export function ObjectMarker({geoJSON}) {
    //debugger
    const properties = geoJSON.properties
    const {id, imgUrl, name} = properties;
    const coordinates = [geoJSON.geometry.coordinates[1],geoJSON.geometry.coordinates[0]];
    console.log(coordinates)

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: 'https://cdn-icons-png.flaticon.com/512/6349/6349523.png',
                iconRetinaUrl: 'https://cdn-icons-png.flaticon.com/512/6349/6349523.png',
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl}/>
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