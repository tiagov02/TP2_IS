import StatisticsPerCountry from "../Procedures/StatisticsPerCountry";
import StatisticsPerYear from "../Procedures/StatisticsPerYear";
import StatisticsPerCountryYear from "../Procedures/StatisticsPerCountryYear";
import GeneralData from "../Procedures/GeneralData";

const Sections = [

    {
        id: "statistics-country", //change
        label: "Suicides per country",
        content: <StatisticsPerCountry/>
    },

    {
        id: "statistics-year", //change
        label: "Suicides per year",
        content: <StatisticsPerYear/>
    },
    {
        id: "statistics-year-country", //change
        label: "Top Suicides in Countries per Year",
        content: <StatisticsPerCountryYear/>
    },
    {
        id: "general-data", //change
        label: "Insights about suicides",
        content: <GeneralData/>
    }

];

export default Sections;