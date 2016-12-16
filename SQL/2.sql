SELECT country.name, rate FROM Country
JOIN literacyrate ON Country.Code = literacyrate.CountryCode
group by country.name
order by rate desc