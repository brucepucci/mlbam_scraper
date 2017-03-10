INSERT IGNORE INTO boxscore (
	attendance,
	gid,
	home_league_id,
	start_time,
	venue_id,
	venue_name,
	weather,
	wind
) VALUES (
	"{attendance}",
	"{gid}",
	"{home_league_id}",
	"{start_time}",
	"{venue_id}",
	"{venue_name}",
	"{weather}",
	"{wind}"
);

