# PostgreSQL

## SQL Language

### Common statements

- CREATE TABLE
- INSERT INTO table [columns] VALUES (value1, value2)
- COPY table FROM
- SELECT columns FROM table WHERE condition ORDER BY columns
- SELECT columns FROM tableA JOIN tableB ON columnA = columnB
- SELECT columns FROM tableA,tableB WHERE columnA = columnB
- SELECT columns FROM table GROUP BY columns
- SELECT columns FROM table GROUP BY columns HAVING conditions
- SELECT columns FROM table WHERE conditions GROUP BY columns
- Limit aggregation range: SELECT columns, aggregation FILTER (WHERE condition), columns FROM table GROUP BY columns
- Window functions: SELECT columns, aggregation OVER (PARTITION BY condition [ORDER BY column]), columns FROM table GROUP BY columns
- UPDATE table SET column = value WHERE condition
- DELETE FROM table WHERE condition
- CREATE VIEW view AS SELECT
- Foreign key: references table(field) in CREATE TABLE
- BEGIN
- COMMIT
- SAVEPOINT savepoint
- ROLLBACK to savepoint
- Inheritance: CREATE TABLE table schema INHERITS table
- CREATE FUNCTION name(arguments) RETURNS type AS $$ BODY $$ LANGUAGE SQL IMMUTABLE STRICT
- ALTER TABLE table ADD COLUMN
- ALTER TABLE table DROP COLUMN
- ALTER TABLE table ADD CHECK
- ALTER TABLE table ADD CONSTRAINT
- ALTER TABLE table DROP CONSTRAINT
- ALTER TABLE table ALTER COLUMN
- ALTER TABLE table RENAME COLUMN
- ALTER TABLE table RENAME TO
- ALTER TABLE table OWNER TO role
- GRANT perms ON table TO role
- SELECT DISTINCT
- SELECT DISTINCT ON
- Common Table Expression: WITH name AS (query)

### Permissions

- SELECT
- INSERT
- UPDATE
- DELETE
- TRUNCATE
- REFERENCES
- TRIGGER
- CREATE
- CONNECT
- TEMPORARY
- EXECUTE
- USAGE
- SET
- ALTER SYSTEM

### Generated Columns

- Add computed columns
- Stored vs virtual

### Constraint

- Check constraints
- Not null
- Unique: allow multiple nulls
- Unique including null (NULLS NOT DISTINCT)
- Primary key
- Foreign key, on delete no action/restrict/cascade/set null
- Exclusion constraint

### Builtin variables/functions

- version()
- current_date

### Joins

- cross join: cartesian product
- inner join: `For each row R1 of T1, the joined table has a row for each row in T2 that satisfies the join condition with R1.`
- left outer join: `First, an inner join is performed. Then, for each row in T1 that does not satisfy the join condition with any row in T2, a joined row is added with null values in columns of T2. Thus, the joined table always has at least one row for each row in T1.`
- right outer join: `First, an inner join is performed. Then, for each row in T2 that does not satisfy the join condition with any row in T1, a joined row is added with null values in columns of T1. This is the converse of a left join: the result table will always have a row for each row in T2.`
- full outer join: `First, an inner join is performed. Then, for each row in T1 that does not satisfy the join condition with any row in T2, a joined row is added with null values in columns of T2. Also, for each row of T2 that does not satisfy the join condition with any row in T1, a joined row with null values in the columns of T1 is added.`

JOIN USING (a, b) means JOIN ON T1.a = T2.a AND T1.b = T2.b

evaluation order:

1. JOIN
2. WHERE
3. GROUP BY
4. HAVING

### Full text search

- Convert text to tsvector for searching: to_tsvector(lang, text)
- Check if text matches: to_tsvector(lang, text) @@ to_tsquery(query)
- Compute rank: ts_rank(tsvector, tsquery)
- Highlight match: ts_headline(lang, text, tsquery)
- Create inverted index (GIN, Generalized Inverted Index): CREATE INDEX index ON table USING GIN (to_tsvector(lang, text))

## Connection

- via unix socket: e.g. `/tmp/.s.PGSQL.5432`
- via tcp: e.g. `localhost:5432`

## Commands

- createdb [dbname]
- dropdb [dbname]
- psql [-U rolename] [dbname]
	- \h: help
	- \q: quit
	- \i: input from file
	- \s: single step mode
	- \dp: dump privilege

## Role management

- CREATE ROLE role [LOGIN] [SUPERUSER] [CREATEDB] [CREATEROLE] [PASSWORD password]
- CREATE USER role
- DROP ROLE role
- `createuser role`
- `dropuser role`
- SELECT * FROM pg_roles
- `\du` in psql cli
- GRANT group_role TO role
- REVOKE group_role FROM role
- SET ROLE role
- RESET ROLE
- ALTER TABLE table OWNER TO role
- REASSIGN OWNED BY roleA TO roleB
- DROP OWNED BY role
