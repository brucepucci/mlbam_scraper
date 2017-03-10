CREATE TABLE IF NOT EXISTS player (
    gid VARCHAR(255),
    id INTEGER,
    first VARCHAR(255),
    last VARCHAR(255),
    num INTEGER,
    boxname VARCHAR(255),
    rl VARCHAR(255),
    bats VARCHAR(255),
    position VARCHAR(255),
    team_abbv VARCHAR(255),
    team_id INTEGER,
    bat_order INTEGER,
    PRIMARY KEY ( gid, id )
);
