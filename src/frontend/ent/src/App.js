import './App.css';
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import {useState} from "react";
import Menu from "./Layout/Menu";
import Content from "./Layout/Content";

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});


function App() {
    const [selectedTab, setSelectedTab] = useState("Players");

    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline/>
            <div className="App">
                <Menu selectedTab={selectedTab} changeSelectedTab={(e, v) => setSelectedTab(v)}/>
                <Content selected={selectedTab}/>
            </div>
        </ThemeProvider>

    );
}

export default App;
