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
	tweet_1_id integer not null,
	tweet_2_id integer not null,
	winner_id interger,
	comment text
);

