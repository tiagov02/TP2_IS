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

function StatisticsPerCountryYear() {
    const [countries, setCountries] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);

    const [years, setYears] = useState([]);
    const [selectedYear, setSelectedYear] = useState("");

    const[hasError, setHasError] = useState(false);

    //useEffect(() => {hasError.current = false});
    useEffect(() => {
        fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/years`)
          .then(res => res.json())
          .then(data => setYears(data));
        setProcData(null);

        fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/countries`)
          .then(res => res.json())
          .then(data => setCountries(data));
        setProcData(null);

        if (selectedYear && selectedCountry) {
            setTimeout(() => {
                setHasError(false);
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/suicides_per_year_country/${selectedYear}/${selectedCountry}`)
                    .then(res => res.json())
                    .then(data => {
                        setProcData(data)
                        setHasError(false);
                    }).catch(error =>  setHasError(true));
            }, 500);
        }
    }, [selectedYear,selectedCountry])

    return (
        <>
            <h1>Suicides By Country and year</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="countries-simple-select"
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
                    <br/>
                    <FormControl fullWidth style={{marginTop:'1rem'}}>
                        <InputLabel id="years-select-label">Years</InputLabel>
                        <Select
                            labelId="years-select-label"
                            id="years-simple-select"
                            value={selectedYear}
                            label="Country"
                            onChange={(e) => {
                                console.log(e.target.value)
                                setSelectedYear(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {years.map(year => (
                                <MenuItem key={year.year} value={year.year}>
                                    {year.year}
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
                        (selectedYear && selectedCountry) && !hasError ? <CircularProgress/> : "--"
                }
                {
                    hasError ?
                        <h3 style={{color: '#880808'}}>There are no suicides matching the data that you search!</h3>
                        : <p></p>
                }
            </Container>
        </>
    );
}

export default StatisticsPerCountryYear;
