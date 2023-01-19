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

function GeneralData() {
    const [years, setYears] = useState([]);
    const [selectedYear, setSelectedYear] = useState("");

    const [procData, setProcData] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:20001/api/years`)
          .then(res => res.json())
          .then(data => setYears(data));
        setProcData(null);

        if (selectedYear) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                fetch(`http://localhost:20004/api/suicides_per_year/${selectedYear}`)
                    .then(res => res.json())
                    .then(data => {
                        debugger
                        setProcData(data)
                    });
            }, 500);
        }
    }, [selectedYear])

    return (
        <>
            <h1>More Suicides In Country</h1>


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
                        selectedYear ? <CircularProgress/> : "--"
                }
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
                        selectedYear ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default GeneralData;
