SELECT Name FROM Country 
WHERE (SELECT SUM(City.Population) FROM City 
WHERE City.CountryCode = Country.Code) <= Country.Population / 2 and Country.population != 0