import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";

/*Icon Suicides
https://cdn-icons-png.flaticon.com/512/6349/6349523.png
 */

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    useEffect(() => {
        const {_northEast: {lat: neLat, lng: neLng}, _southWest: {lat: swLat, lng: swLng}} = bounds;


        fetch(`http://localhost:20002/api/tile/${bounds._southWest.lng}/${bounds._southWest.lat}/${bounds._northEast.lng}/${bounds._northEast.lat}`)
    .then(response => response.json())
    .then(geoJSON => {
        //console.log(geoJSON);
        //console.log(geoJSON)
        //debugger
        setGeom(geoJSON)
    })
    .catch(err => console.log(err));
    }, [bounds])

    return (
        <LayerGroup>
            {
                Array.isArray(geom) && geom.map(geoJSON => <ObjectMarker key={geoJSON[0].properties.id} geoJSON={geoJSON[0]}/>)
            }
    </LayerGroup>
    );
}

export default ObjectMarkersGroup;
