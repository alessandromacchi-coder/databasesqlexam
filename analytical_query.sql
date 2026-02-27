select drivers.name, drivers.surname, drivers.nationality, SUM(results.points) AS seasonpoints from drivers
inner join results on results.driverid = drivers.driverid
inner join races on races.raceid = results.raceid
WHERE races.year=2018
group by drivers.driverid
order by seasonpoints DESC


