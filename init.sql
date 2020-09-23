create database cyclone;

\c cyclone

create table if not exists cyclone_history(
	time timestamp,
	lat decimal,
	long decimal,
	intensity int,
	primary key(time, lat, long)
	
);

create table if not exists cyclone_forecast(
	hour int,
	lat decimal,
	long decimal,
	intensity int,
	primary key(hour, lat, long)
);
