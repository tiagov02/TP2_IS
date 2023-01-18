import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";



async function getCountry(){
        await fetch('http://localhost:20002/api/countries')
        .then(response => response.json())
        .then(data => {
            debugger
            // Update the state with the received data
            return data;
        });
}
const DEMO_TEAMS = [
    {"team": "Manchester United", country: "UK"},
    {"team": "Manchester City", country: "UK"},
    {"team": "Chelsea", country: "UK"},
    {"team": "Tottenham", country: "UK"},
    {"team": "Fulham", country: "UK"},
    {"team": "Sporting", country: "Portugal"},
    {"team": "Porto", country: "Portugal"},
    {"team": "Benfica", country: "Portugal"},
    {"team": "Braga", country: "Portugal"},
    {"team": "PSG", country: "France"},
    {"team": "Lyon", country: "France"},
    {"team": "Olympique de Marseille", country: "France"}
];

const COUNTRIES = [...new Set(DEMO_TEAMS.map(team => team.country))];


async function StatisticsPerCountry() {

    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);
    const countries = await getCountry();

    useEffect(() => {
        //!FIXME: this is to simulate how to retrieve data from the server
        //!FIXME: the entities server URL is available on process.env.REACT_APP_API_ENTITIES_URL
        setProcData(null);
        setGQLData(null);

        if (selectedCountry) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                setProcData(DEMO_TEAMS.filter(t => t.country === selectedCountry));
            }, 500);
        }
    }, [selectedCountry])

    return (
        <>
            <h1>Top Countries</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <select id="country-select" value={selectedCountry}
                                onChange={e => setSelectedCountry(e.target.value)}>
                            <option value="" disabled>Select a country</option>
                            {
                                countries.map(country => (
                                    <option key={country.name} value={country.name}>
                                        {country.name}
                                    </option>
                                ))
                            }
                        </select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default StatisticsPerCountry;
