--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Raspbian 11.7-0+deb10u1)
-- Dumped by pg_dump version 11.7 (Raspbian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: t_match_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_match_type AS ENUM (
    'regex',
    'word',
    'word_part'
);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: banned_phrases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.banned_phrases (
    value character varying,
    discord_id character varying,
    id integer NOT NULL,
    match_type public.t_match_type NOT NULL
);


--
-- Name: banned_phrases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.banned_phrases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: banned_phrases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.banned_phrases_id_seq OWNED BY public.banned_phrases.id;


--
-- Name: banned_phrases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.banned_phrases ALTER COLUMN id SET DEFAULT nextval('public.banned_phrases_id_seq'::regclass);


--
-- Name: banned_phrases banned_phrases_discord_id_value_match_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.banned_phrases
    ADD CONSTRAINT banned_phrases_discord_id_value_match_type_key UNIQUE (discord_id, value, match_type);


--
-- Name: banned_phrases banned_phrases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.banned_phrases
    ADD CONSTRAINT banned_phrases_pkey PRIMARY KEY (id);


--
-- Name: banned_phrases_discord_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX banned_phrases_discord_id_idx ON public.banned_phrases USING btree (discord_id);


--
-- PostgreSQL database dump complete
--

