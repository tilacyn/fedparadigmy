SELECT city.name as "City", city.population,country.name as "Country" FROM City
JOIN Country ON Country.Code = City.CountryCode
order by cast(city.population as real)/cast(country.population as real) desc
