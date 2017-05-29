-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table Players {

	player_id serial primary key
	player_name varchar(100)

};

create table Matches {

	match_id serial primary key,
	winner_id integer REFRENCES Players(player_id),
	looser_id integer REFRENCES Players(player_id)

};

create view standings AS
select Players.player_id,Players.player_name,count(Matches.winner_id)
AS wins from Players left join Matches ON Players.player_id = Matches.winner_id
GROUP BY player_id
ORDER BY wins desc;

create view standingsAll AS
select Players.player_id,Players.player_name,count(Matches.match_id)
AS total_matches from Players left join Matches ON Players.player_id = Matches.winner_id
OR Players.player_id = Matches.looser_id 
GROUP BY Players.player_id

