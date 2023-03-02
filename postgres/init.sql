BEGIN;
CREATE SCHEMA IF NOT EXISTS content;
--
-- Create model League
--
CREATE TABLE "content"."league" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL);
--
-- Create model Map
--
CREATE TABLE "content"."map" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL);
--
-- Create model Player
--
CREATE TABLE "content"."player" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL, "birthday" date NULL, "hometown" varchar(512) NULL, "nationality" varchar(512) NULL);
--
-- Create model Serie
--
CREATE TABLE "content"."serie" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL, "tier" varchar(512) NULL);
--
-- Create model Team
--
CREATE TABLE "content"."team" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL, "location" varchar(512) NULL);
--
-- Create model Tournament
--
CREATE TABLE "content"."tournament" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(512) NULL, "prizepool" varchar(512) NULL);
--
-- Create model Stat
--
CREATE TABLE "content"."stat" ("id" bigserial NOT NULL PRIMARY KEY, "adr" double precision NOT NULL, "kills" integer NOT NULL, "assists" integer NOT NULL, "deaths" integer NOT NULL, "first_kills_diff" integer NOT NULL, "flash_assists" integer NOT NULL, "headshots" integer NOT NULL, "k_d_diff" integer NOT NULL, "kast" double precision NOT NULL, "rating" double precision NOT NULL, "game_id" integer NOT NULL, "player_id" integer NOT NULL);
--
-- Create model Round
--
CREATE TABLE "content"."round" ("id" bigserial NOT NULL PRIMARY KEY, "outcome" varchar(512) NULL, "round" integer NOT NULL, "ct_id" integer NOT NULL, "game_id" integer NOT NULL, "t_id" integer NOT NULL, "winner_team_id" integer NOT NULL);
--
-- Create model Game
--
CREATE TABLE "content"."game" ("id" integer NOT NULL PRIMARY KEY, "match_id" integer NOT NULL, "begin_at" timestamp with time zone NOT NULL, "league_id" integer NOT NULL, "map_id" integer NOT NULL, "serie_id" integer NOT NULL, "team1_id" integer NOT NULL, "team2_id" integer NOT NULL, "tournament_id" integer NOT NULL);
ALTER TABLE "content"."stat" ADD CONSTRAINT "stat_game_id_2fb4af11_fk_map_id" FOREIGN KEY ("game_id") REFERENCES "content"."map" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."stat" ADD CONSTRAINT "stat_player_id_31640b4d_fk_player_id" FOREIGN KEY ("player_id") REFERENCES "content"."player" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "stat_game_id_2fb4af11" ON "content"."stat" ("game_id");
CREATE INDEX "stat_player_id_31640b4d" ON "content"."stat" ("player_id");
ALTER TABLE "content"."round" ADD CONSTRAINT "round_ct_id_7883a710_fk_team_id" FOREIGN KEY ("ct_id") REFERENCES "content"."team" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."round" ADD CONSTRAINT "round_game_id_e1f39007_fk_map_id" FOREIGN KEY ("game_id") REFERENCES "content"."map" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."round" ADD CONSTRAINT "round_t_id_272d524a_fk_team_id" FOREIGN KEY ("t_id") REFERENCES "content"."team" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."round" ADD CONSTRAINT "round_winner_team_id_aa1d227f_fk_team_id" FOREIGN KEY ("winner_team_id") REFERENCES "content"."team" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "round_ct_id_7883a710" ON "content"."round" ("ct_id");
CREATE INDEX "round_game_id_e1f39007" ON "content"."round" ("game_id");
CREATE INDEX "round_t_id_272d524a" ON "content"."round" ("t_id");
CREATE INDEX "round_winner_team_id_aa1d227f" ON "content"."round" ("winner_team_id");
ALTER TABLE "content"."game" ADD CONSTRAINT "game_league_id_6ee36d94_fk_league_id" FOREIGN KEY ("league_id") REFERENCES "content"."league" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."game" ADD CONSTRAINT "game_map_id_5b3eb405_fk_map_id" FOREIGN KEY ("map_id") REFERENCES "content"."map" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."game" ADD CONSTRAINT "game_serie_id_2590bef4_fk_serie_id" FOREIGN KEY ("serie_id") REFERENCES "content"."serie" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."game" ADD CONSTRAINT "game_team1_id_f1ceffbf_fk_team_id" FOREIGN KEY ("team1_id") REFERENCES "content"."team" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."game" ADD CONSTRAINT "game_team2_id_06710dec_fk_team_id" FOREIGN KEY ("team2_id") REFERENCES "content"."team" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "content"."game" ADD CONSTRAINT "game_tournament_id_e1e96683_fk_tournament_id" FOREIGN KEY ("tournament_id") REFERENCES "content"."tournament" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "game_league_id_6ee36d94" ON "content"."game" ("league_id");
CREATE INDEX "game_map_id_5b3eb405" ON "content"."game" ("map_id");
CREATE INDEX "game_serie_id_2590bef4" ON "content"."game" ("serie_id");
CREATE INDEX "game_team1_id_f1ceffbf" ON "content"."game" ("team1_id");
CREATE INDEX "game_team2_id_06710dec" ON "content"."game" ("team2_id");
CREATE INDEX "game_tournament_id_e1e96683" ON "content"."game" ("tournament_id");
COMMIT;