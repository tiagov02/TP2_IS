import React, {useEffect, useState} from "react";


function StatisticsPerCountry() {
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:20001/api/countries`)
      .then(res => res.json())
      .then(data => setCountries(data));
  }, []);



  return (
    <div>
      <label>Select a country:</label>
      <select>
        {countries.map(country => (
          <option key={country.id} value={country.name}>
            {country.name}
          </option>
        ))}
      </select>
    </div>
  );
}


export default StatisticsPerCountry;