import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

//CHANGE THIS TWO FUNCTIONS
function present_result_rpc_less_more(data){
    return(
    <>
        <h3>Country with less suicides</h3>
        <li>Country: {data.less.country}</li>
        <li>Country: {data.less.suicides_no}</li>

        <h3>Country with More suicides</h3>
        <li>Country: {data.more.country}</li>
        <li>Country: {data.more.suicides_no}</li>
    </>
    )
}

function present_result_rpc_rich(data){
    debugger
    return(
    <>

                                    <li>Sex: {data.sex} --> Suicides Number:{data.suicides_no}</li>
                                    <li>Sex: {data.sex} --> Suicides Number:{data.suicides_no}</li>
    </>
    )
}

function GeneralData() {

    const [lessMore, setLessMore] = useState(null);
    const [richCountries, setRichCountries] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:20004/api/suicides_in_rich_countries`)
          .then(res => res.json())
          .then(data => setRichCountries(data).catch(error => {return}));
        fetch(`http://localhost:20004/api/country_less_more_suicides`)
            .then(res =>res.json())
            .then(data => setLessMore(data)).catch(error => {
            return
        });
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
                <h2>Did you know how many suicides have in rich countries? <small>(PROC)</small></h2>
                {
                    richCountries ?
                        <ul>
                            {
                                richCountries.map(data => {
                                    return present_result_rpc_rich(data)
                                })
                            }
                        </ul> :
                        <p></p>
                }
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Whats the country that have less and more suicides? <small>(PROC)</small></h2>
                {
                    lessMore ?
                        <ul>
                            {
                                lessMore.map(data => {
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
