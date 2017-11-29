#!/bin/bash -eux

# Assumes that current user can access 
# pgSQL DB.
# Strips out any command that sqlite3 cannot process

pg_dump -Ox  --inserts | \
	 grep -v '^SET.*' | \
	 grep -v '^COMMENT.*' | \
	 grep -v '.*EXTENSION.*' | \
	 grep -v 'ALTER TABLE ONLY' | \
	 grep -v 'ALTER SEQUENCE' | \
	 grep -v 'ADD CONSTRAINT' | \
	 grep -v 'CREATE INDEX' | \
	 grep -v setval | \
	 grep -v '^CREATE SEQUENCE.*$' | \
	 grep -v '^    START WITH 1.*$' | \
	 grep -v '^    INCREMENT BY 1.*$' | \
	 grep -v '^    NO MINVALUE.*$' | \
	 grep -v '^    NO MAXVALUE.*$' | \
	 grep -v '^    CACHE 1;.*$'
