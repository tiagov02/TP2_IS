import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

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


function StatisticsPerCountry() {
    const [countries, setCountries] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:20001/api/countries`)
          .then(res => res.json())
          .then(data => setCountries(data));
        setProcData(null);
        setGQLData(null);

        if (selectedCountry) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                setProcData(DEMO_TEAMS.filter(country => country.country === selectedCountry));
            }, 500);

            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_GRAPHQL_URL}`);
                setGQLData(DEMO_TEAMS.filter(country => country.country === selectedCountry));
            }, 1000);
        }
    }, [selectedCountry])

    return (
        <>
            <h1>More Suicides In Country</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e) => {
                                setSelectedCountry(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {countries.map(country => (
                                <MenuItem key={country.name} value={country.name}>
                                    {country.name}
                                </MenuItem>
                            ))}
                        </Select>
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
            </Container>
        </>
    );
}

export default StatisticsPerCountry;
