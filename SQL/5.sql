select governmentform, sum(surfacearea) as SummaryS from country
group by governmentform
order by sum(surfacearea) desc
limit 1