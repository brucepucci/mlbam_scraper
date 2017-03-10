CREATE TABLE IF NOT EXISTS inning_line_score (
	away INT,
	gid VARCHAR(255),
	home INT,
	inning INT,
	PRIMARY KEY ( gid, inning )
);
