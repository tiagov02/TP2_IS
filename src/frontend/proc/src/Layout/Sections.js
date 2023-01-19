import StatisticsPerCountry from "../Procedures/StatisticsPerCountry";
import StatisticsPerYear from "../Procedures/StatisticsPerYear";
import StatisticsPerCountryYear from "../Procedures/StatisticsPerCountryYear";
import GeneralData from "../Procedures/GeneralData";

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
    },
    {
        id: "general-data", //change
        label: "Top Suicides Data",
        content: <GeneralData/>
    }

];

export default Sections;