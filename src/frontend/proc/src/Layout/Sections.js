import StatisticsPerCountry from "../Procedures/StatisticsPerCountry";

const Sections = [

    {
        id: "statistics-country", //change
        label: "Top Suicides",
        content: <StatisticsPerCountry/>
    },

    {
        id: "top-scorers", //change
        label: "Top Suicides in Countries per Age",
        content: <h1>Top Scorers - Work in progresss</h1>
    }

];

export default Sections;