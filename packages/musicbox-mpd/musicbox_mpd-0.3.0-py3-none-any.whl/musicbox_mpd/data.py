import sqlite3


def in_memory_db():
    connection = sqlite3.connect(
        'file::memory:?cache=shared', uri=True,  check_same_thread=False)
    connection.row_factory = sqlite3.Row

    create_sql = """
        create table library
        (
            id INTEGER PRIMARY KEY, 
            file text, 
            title text, 
            artist text, 
            album text, 
            albumartist text, 
            tracknumber int, 
            duration int, 
            year text,
            radio int
        )
        """

    connection.execute(create_sql)

    return connection


def get_uri(con, id):
    curs = con.execute(
        "select file from library where id = ?", (id,))
    result = curs.fetchone()
    if result == None:
        return None
    return result[0]


def get_id(con, uri):
    curs = con.execute(
        "select id from library where file = ?", (uri,))
    result = curs.fetchone()
    if result == None:
        return 0
    return result[0]


def search(con, search):
    include_songs = len(search) > 1
    x = f"%{search}%"

    sql = """
        select album, 
        case when count(*) > 1 then 'Various' else max(albumartist) end artist, 
        null as title, 
        0 as id, 
        0 as duration,
        path
        from (
            select distinct coalesce(albumartist, artist) as albumartist, album,rtrim(file, replace(file, '/', '')) as path
            from library 
            where album like ? or artist like ? or albumartist like ? or year like ?
        ) sq 
        group by album, path     
    """

    if include_songs:
        sql += """
            union 
            select album, artist, title, id, duration, rtrim(file, replace(file, '/', '')) as path
            from library
            where title like ?"""

    sql += "order by title, artist;"

    if include_songs:
        return query(con, sql, (x, x, x, x, x))
    else:
        return query(con, sql, (x, x, x, x))


def get_album(con, path):
    sql = "select * from library where rtrim(file, replace(file, '/', '')) = ? order by artist, album, cast(tracknumber as INT), file"
    return query(con, sql, (path,))


def get_random_songs(con, number):
    sql = f"select file from library order by random() limit {number}"
    return query(con, sql, ())


def add_radio_stations(con, stations):
    sql = "insert into library(file,title,artist, album, albumartist, tracknumber, duration, year, radio) values (?,?,?,?,?,?,?,?,1)"
    count = 1
    for station in stations:
        url = station.get("url")
        name = station.get("name")
        params = (url, name, url, name, "Radio", count, 0, 0)
        con.execute(sql, params)
        count += 1


def query(con, sql, params):
    res = con.execute(sql, params)
    rows = res.fetchall()
    return [dict(row) for row in rows]
