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


const Players = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('path/to/your/json/file')
            .then(response => response.json())
            .then(data => setData(data))
    }, []);

    return (
        <table>
            <thead>
                <tr>
                    <th>Country Name</th>
                    <th>GDP for year</th>
                    <th>GDP per capita</th>
                    <th>Generation</th>
                    <th>HDI for year</th>
                    <th>Population</th>
                    <th>Sex</th>
                    <th>Suicides no</th>
                    <th>Tax</th>
                    <th>Year</th>
                </tr>
            </thead>
            <tbody>
                {data.map(row => (
                    <tr key={row.id}>
                        <td>{row.country.name}</td>
                        <td>{row.gdp_for_year}</td>
                        <td>{row.gdp_per_capita}</td>
                        <td>{row.generation}</td>
                        <td>{row.hdi_for_year}</td>
                        <td>{row.population_no}</td>
                        <td>{row.sex}</td>
                        <td>{row.suicides_no}</td>
                        <td>{row.tax}</td>
                        <td>{row.year}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
/*
function Players(){
    const SIZE_PAGE = 20;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);

      useEffect(() => {
        setData(null);
        setTimeout(() => {
            fetch(`http://localhost:20001/api/suicides/per_page/${page}/${SIZE_PAGE}`)
            .then(response => response.json())
            .then(jsonData => setData(jsonData));
        }, 500);
    }, [page])

    useEffect(() => {
        setTimeout(() => {
            fetch(`http://localhost:20001/api/suicides/number`)
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
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Country Name</TableCell>
                            <TableCell align="center">GDP per capita</TableCell>
                            <TableCell align="center">Sex</TableCell>
                            <TableCell align="center">Number of Suicides</TableCell>
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
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {row.country.name}
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
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={5}>
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


*/

export default Players;
