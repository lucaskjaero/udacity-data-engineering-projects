# DROP TABLES

songplay_table_drop = "DROP table songplays;"
user_table_drop = "DROP table users;"
song_table_drop = "DROP table songs;"
artist_table_drop = "DROP table artists;"
time_table_drop = "DROP table time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id serial,
start_time timestamp,
user_id int,
level varchar,
song_id varchar,
artist_id varchar,
session_id int,
location varchar,
user_agent varchar);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id int,
first_name varchar,
last_name varchar,
gender varchar,
level varchar);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar,
title varchar,
artist_id varchar,
year int,
duration float8);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar,
name varchar,
location varchar,
lattitude float8,
longitude float8);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time timestamp,
hour int,
day int,
week int,
month int,
year int,
weekday int);
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
