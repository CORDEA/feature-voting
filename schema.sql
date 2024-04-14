DROP TABLE IF EXISTS Features;
CREATE TABLE Features
(
    ID        INTEGER PRIMARY KEY AUTOINCREMENT,
    CreatedAt DATETIME,
    Title     TEXT,
    Body      TEXT,
    Votes     INTEGER
);
