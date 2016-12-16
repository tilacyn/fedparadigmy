SELECT country.name,count(city.name) FROM City
JOIN Country ON Country.Code = City.CountryCode
where city.population > 1000000
group by country.code
order by count(city.name) desc