CREATE TABLE IF NOT EXISTS inningscore (
    gid VARCHAR(255),
    inning INTEGER,
    away_inning_runs INTEGER,
    home_inning_runs INTEGER,
    PRIMARY KEY ( gid, inning )
);
