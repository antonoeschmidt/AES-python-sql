DROP TABLE IF EXISTS testResults;
DROP TABLE IF EXISTS headers;

CREATE TABLE testResults (
	ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	CPRnummer TEXT,
	Fornavn TEXT,
	Efternavn TEXT,
	Data BLOB
);

CREATE TABLE headers (
	ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Headers TEXT
);