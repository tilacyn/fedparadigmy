SELECT City.Name FROM City
WHERE City.Id = (
  SELECT Capital.CityId from Capital
  where Capital.CountryCode = (
	 Select Country.Code from Country
	 where Country.name = "Malaysia"
  )
);