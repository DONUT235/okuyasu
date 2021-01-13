CREATE TABLE Permissions (
	discord_id character varying PRIMARY KEY,
	can_kill boolean NOT NULL
);

INSERT INTO Permissions (discord_id, can_kill)
SELECT DISTINCT discord_id, FALSE FROM banned_phrases;
