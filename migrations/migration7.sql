ALTER TABLE permissions
ALTER COLUMN discord_id TYPE bigint USING discord_id::bigint;

ALTER TABLE banned_phrases
ALTER COLUMN discord_id TYPE bigint USING discord_id::bigint,
ADD CONSTRAINT fk_discord_id_discord_id 
FOREIGN KEY (discord_id) REFERENCES permissions (discord_id)
ON DELETE CASCADE;
