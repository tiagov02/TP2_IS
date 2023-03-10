import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";


function present_result_rpc(data){
    return(
    <>
                                    <li>Suicides in childerns: {data.children}</li>
                                    <li>Suicides in old people: {data.olders}</li>
                                    <h3>Number of suicides by sex</h3>
                                    <li>Sex: {data.per_sex[0].sex} --> Suicides Number:{data.per_sex[0].suicides_no}</li>
                                    <li>Sex: {data.per_sex[1].sex} --> Suicides Number:{data.per_sex[1].suicides_no}</li>
    </>
    )
}

function StatisticsPerCountry() {
    const [countries, setCountries] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);

    useEffect(() => {
        fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/countries`)
          .then(res => res.json())
          .then(data => setCountries(data));
        setProcData(null);

        if (selectedCountry) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/suicides_per_country/${selectedCountry}`)
                    .then(res => res.json())
                    .then(data => {
                        debugger
                        setProcData(data)
                    });
            }, 500);
        }
    }, [selectedCountry])

    return (
        <>
            <h1>Suicides By Country</h1>

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
                                console.log(e.target.value)
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
                                procData.map(data => {
                                    return present_result_rpc(data)
                                })
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default StatisticsPerCountry;
