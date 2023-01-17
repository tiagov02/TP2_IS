import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";


/*
link for icon
https://cdn-icons-png.flaticon.com/512/6349/6349523.png
 */

async function requestEntities(bounds) {
    const response = await fetch(`http://localhost:20002/api/tile/${bounds._southWest.lng}/${bounds._southWest.lat}/${bounds._northEast.lng}/${bounds._northEast.lat}`);
    return await response.json();
}

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState(...[]);
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
