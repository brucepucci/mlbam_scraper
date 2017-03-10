CREATE TABLE IF NOT EXISTS team (
	gid VARCHAR(255),
	id INT,
	losses INT,
	team_code VARCHAR(255),
	team_flag VARCHAR(255),
	wins INT,
	PRIMARY KEY ( gid, team_code )
);
