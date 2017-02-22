CREATE TABLE IF NOT EXISTS linescore (
	away_team_errors INT,
	away_team_hits INT,
	away_team_runs INT,
	gid VARCHAR(255),
	home_team_errors INT,
	home_team_hits INT,
	home_team_runs INT,
	PRIMARY KEY ( gid )
);
