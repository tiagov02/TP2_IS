import {Tab, Tabs} from "@mui/material";


function Menu({selectedTab = "Players", changeSelectedTab}) {

    return (
        <div className={"Menu"}>
            <div className={"Logo"}>
                <img src={"logo512.png"} alt={""}/>
                <div className={"Title"}>
                    Systems Integration
                </div>
            </div>
            <Tabs value={selectedTab} orientation={"vertical"} centered onChange={changeSelectedTab}>
                <Tab value={"Players"} label="Players"/>
                <Tab value={"Teams"} label="Teams"/>
                <Tab value={"Countries"} label="Countries"/>
            </Tabs>
        </div>
    );
}

export default Menu;
