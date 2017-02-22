CREATE TABLE IF NOT EXISTS atbat (
	away_team_runs INT,
	b INT,
	b_height VARCHAR(255),
	b_team VARCHAR(255),
	batter INT,
	des TEXT(65536),
	event VARCHAR(255),
	gid VARCHAR(255),
	home_team_runs INT,
	inn INT,
	inn_half VARCHAR(255),
	num INT,
	o INT,
	p_team VARCHAR(255),
	p_throws VARCHAR(255),
	pitcher INT,
	s INT,
	stand VARCHAR(255),
	start_tfs INT,
	PRIMARY KEY ( gid, num )
);

