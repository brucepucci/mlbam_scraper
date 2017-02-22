INSERT IGNORE INTO linescore (
	away_team_errors,
	away_team_hits,
	away_team_runs,
	gid,
	home_team_errors,
	home_team_hits,
	home_team_runs
) VALUES (
	"{away_team_errors}",
	"{away_team_hits}",
	"{away_team_runs}",
	"{gid}",
	"{home_team_errors}",
	"{home_team_hits}",
	"{home_team_runs}"
);
