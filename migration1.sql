CREATE TYPE t_match_type AS ENUM ('regex', 'word', 'word_part');
ALTER TABLE banned_phrases
	ADD COLUMN match_type t_match_type;
