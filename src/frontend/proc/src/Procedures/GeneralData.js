import React, {useEffect, useState} from "react";
import {CircularProgress, Container} from "@mui/material";

//CHANGE THIS TWO FUNCTIONS
function present_result_rpc_less_more(data){

    return(
    <>
        <h3>Country with less suicides</h3>
        <li>Country: {data[0].less.country}</li>
        <li>Nº of suicides: {data[0].less.suicides_no}</li>

        <h3>Country with More suicides</h3>
        <li>Country: {data[0].more.country}</li>
        <li>Nº of suicides: {data[0].more.suicides_no}</li>
    </>
    )
}

function present_result_rpc_rich(data){
    debugger
    return(
    <>

                                    <li>Sex: {data[0].sex} --> Suicides Number:{data[0].suicides_no}</li>
                                    <li>Sex: {data[1].sex} --> Suicides Number:{data[1].suicides_no}</li>
    </>
    )
}

function GeneralData() {

    const [lessMore, setLessMore] = useState(null);
    const [richCountries, setRichCountries] = useState(null);

    useEffect(() => {
        fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/suicides_in_rich_countries`)
          .then(res => res.json())
          .then(data => setRichCountries(data));
        fetch(`http://${process.env.REACT_APP_API_PROC_URL}/api/country_less_more_suicides`)
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
                <h2>Did you know how many suicides have in rich countries? <small>(PROC)</small></h2>
                {
                    richCountries ?
                        <ul>
                            {
                                present_result_rpc_rich(richCountries)
                            }
                        </ul> :
                        <CircularProgress/>
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
                                present_result_rpc_less_more(lessMore)
                            }
                        </ul> :
                        <CircularProgress/>
                }
            </Container>
        </>
    );
}

export default GeneralData;
