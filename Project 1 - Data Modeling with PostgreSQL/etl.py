import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = (df["song_id"][0], df["title"][0], df["artist_id"]
                 [0], int(df["year"][0]), float(df["duration"][0]))
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = (df["artist_id"][0], df["artist_name"][0], df["artist_location"]
                   [0], float(df["artist_latitude"][0]), float(df["artist_longitude"][0]))
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    df.ts = pd.to_datetime(df.ts, unit="ms")

    # insert time data records
    time_data = (df.ts, df.ts.dt.hour, df.ts.dt.day, df.ts.dt.week,
                 df.ts.dt.month, df.ts.dt.year, df.ts.dt.weekday)
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.concat(time_data, axis=1)

    # Perhaps unneccesary but it helps readability.
    time_df.columns = column_labels

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (row["ts"], row["userId"], row["level"], songid,
                         artistid, row["sessionId"], row["location"], row["userAgent"])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
