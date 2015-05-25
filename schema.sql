drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title text not null,
	text text not null
);

drop table if exists users;
create table users (
	email TEXT NOT NULL,
	password TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL, 
	profilepic_path TEXT NOT NULL,
    activated INTEGER NOT NULL,
	PRIMARY KEY(email)
);

drop table if exists tweets;
CREATE TABLE tweets (
	owner TEXT NOT NULL,
    tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_text VARCHAR(140) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    pic_path TEXT
);

drop table if exists subscriptions;
CREATE TABLE subscriptions (
	user TEXT NOT NULL,
	subscribed_user TEXT NOT NULL
);

drop table if exists sessions;
CREATE TABLE sessions (
	user TEXT NOT NULL,
	session TEXT NOT NULL,
	FOREIGN KEY(user) REFERENCES users(email),
	PRIMARY KEY(session)
);