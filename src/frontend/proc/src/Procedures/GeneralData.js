import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

//CHANGE THIS TWO FUNCTIONS
function present_result_rpc_less_more(data){
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

function present_result_rpc_rich(data){
    return(
    <>

                                    <li>Sex: {data.per_sex[0].sex} --> Suicides Number:{data.per_sex[0].suicides_no}</li>
                                    <li>Sex: {data.per_sex[1].sex} --> Suicides Number:{data.per_sex[1].suicides_no}</li>
    </>
    )
}

function GeneralData() {

    const [lessMore, setLessMore] = useState(null);
    const [richCountries, setRichCountries] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:20004/api/suicides_in_rich_countries`)
          .then(res => res.json())
          .then(data => setRichCountries(data));
        fetch(`http://localhost:20004/api/country_less_more_suicides`)
            .then(res =>res.json())
            .then(data => setLessMore(data));
    }, [])

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
                <h2>Results of suicides in rich countries<small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => {
                                    return present_result_rpc_rich(data)
                                })
                            }
                        </ul> :
                        <p></p>
                }

                <h2>Whats the country that have less and lore suicides?<small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => {
                                    return present_result_rpc_less_more(data)
                                })
                            }
                        </ul> :
                        <p></p>
                }
            </Container>
        </>
    );
}

export default GeneralData;
