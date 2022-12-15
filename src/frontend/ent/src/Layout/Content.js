import Players from "../Tables/Players";

function Content({selected}) {

    return (
        <div className={"Content"}>
            {
                {
                    "Players": <Players />,
                    "Teams": <h1>Teams - Work in progress</h1>,
                    "Countries": <h1>Countries - Work in progress</h1>
                }[selected]
            }
        </div>
    );
}

export default Content;
