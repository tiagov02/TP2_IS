import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


function Suicides(){
    const SIZE_PAGE = 20;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);

      useEffect(() => {
        setData(null);
        setTimeout(() => {
            fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/suicides/per_page/${page}/${SIZE_PAGE}`)
            .then(response => response.json())
            .then(jsonData => setData(jsonData));
        }, 500);
    }, [page])

    useEffect(() => {
        setTimeout(() => {
            fetch(`http://${process.env.REACT_APP_API_ENTITIES_URL}/api/suicides/number`)
            .then(response => response.json())
            .then(jsonData => setMaxDataSize(jsonData));
        }, 500);
    }, [])

    return (
        <>
            <h1>Suicides</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Country Name</TableCell>
                            <TableCell align="center">Year</TableCell>
                            <TableCell align="center">GDP per capita</TableCell>
                            <TableCell align="center">Sex</TableCell>
                            <TableCell align="center">Number of Suicides</TableCell>
                            <TableCell align="center">Tax of Suicides</TableCell>
                            <TableCell align="center">Generation</TableCell>
                            <TableCell align="center">Min Age</TableCell>
                            <TableCell align="center">Max Age</TableCell>
                            <TableCell align="center">Number Population</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" scope="row">
                                            {row.country.name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.year}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.gdp_per_capita}
                                        </TableCell>
                                         <TableCell component="td" align="center" scope="row">
                                            {row.sex}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.suicides_no}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.tax} %
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.generation}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.min_age}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.max_age}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.population_no}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={10}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / SIZE_PAGE)}
                    />
                </div>
            }
        </>
    );
}
export default Suicides;
