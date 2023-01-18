import StatisticsPerCountry from "../Procedures/StatisticsPerCountry";
import StatisticsPerYear from "../Procedures/StatisticsPerYear";

const Sections = [

    {
        id: "statistics-country", //change
        label: "Top Suicides",
        content: <StatisticsPerCountry/>
    },

    {
        id: "top-scorers", //change
        label: "Top Suicides in Countries per Year",
        content: <StatisticsPerYear/>
    }

];

export default Sections;