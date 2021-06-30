drop table if exists tweets;
drop table if exists judgemement_results;

create table tweets (
	id integer primary key autoincrement,
	tweet_content text not null,
	tweet_likes integer not null,
	tweet_retweets integer not null,
	tweet_interactions integer not null
);

create table cj_results (
	id integer primary key autoincrement,
	winner_id interger not null,
	loser_id integer not null,
	comment text not null
);

