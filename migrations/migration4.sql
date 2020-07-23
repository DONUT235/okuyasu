ALTER TABLE banned_phrases
	DROP CONSTRAINT banned_phrases_discord_id_value_key,
	ADD UNIQUE (discord_id, value, match_type);
