#!/usr/bin/env python3

import sqlalchemy as sqla
import sqlalchemy.orm as orm

engine = sqla.create_engine("sqlite+pysqlite:///:memory:", echo=True)

with engine.connect() as conn:
    conn.execute(sqla.text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
            sqla.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
            )
    conn.commit()

with engine.begin() as conn:
    conn.execute(
            sqla.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
            )

with engine.connect() as conn:
    result = conn.execute(sqla.text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")

with engine.connect() as conn:
    result = conn.execute(sqla.text("select x, y from some_table where y > :y"), {"y": 2})
    for x, y in result:
        print(f"x: {x} y: {y}")

with engine.connect() as conn:
    conn.execute(
            sqla.text("insert into some_table (x, y) values (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y":14}],
            )
    conn.commit()

stmt = sqla.text("select x, y from some_table where y > :y order by x, y")
with orm.Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for x, y in result:
        print(f"x: {x} y: {y}")

with orm.Session(engine) as session:
    result = session.execute(
            sqla.text("update some_table set y=:y where x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y":15}],
            )
    session.commit()
