CREATE TABLE IF NOT EXISTS boxscore (
	attendance VARCHAR(255),
	gid VARCHAR(255),
	home_league_id INT,
	start_time VARCHAR(255),
	venue_id INT,
	venue_name VARCHAR(255),
	weather VARCHAR(255),
	wind VARCHAR(255),
	PRIMARY KEY ( gid )
);
