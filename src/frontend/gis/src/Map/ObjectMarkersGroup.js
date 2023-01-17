import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";

async function requestEntities(bounds) {
    const url = 'http://localhost:20002/api/objects?bounds=${bounds.toBBoxString()}';
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    /* Updates the data for the current bounds */
    useEffect(async () => {
        console.log(`> getting data for bounds`, bounds);
        setGeom(await requestEntities(bounds));
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
