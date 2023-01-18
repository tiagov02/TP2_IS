import StatisticsPerCountry from "../Procedures/StatisticsPerCountry";
import StatisticsPerYear from "../Procedures/StatisticsPerYear";
import StatisticsPerCountryYear from "../Procedures/StatisticsPerCountryYear";

const Sections = [

    {
        id: "statistics-country", //change
        label: "Top Suicides",
        content: <StatisticsPerCountry/>
    },

    {
        id: "statistics-year", //change
        label: "Top Suicides in Countries per Year",
        content: <StatisticsPerYear/>
    },
    {
        id: "statistics-year-country", //change
        label: "Top Suicides in Countries per Year",
        content: <StatisticsPerCountryYear/>
    }

];

export default Sections;