Title: Adding guardrails to psql for PostgreSQL
Date: 2024-02-24
Author: Simon Larsén
Tags: postgresql,psql,database
Slug: psql-guardrails

I've been using `psql` for many years to interface with PostgreSQL databases.
It's simple, pretty much always available as it's usually bundled with
PostgreSQL and just does what it's supposed to. It does, however, have some
pretty dangerous defaults. Not only are writes allowed, but it also
automatically commits any statements executed outside of explicit transactions.
Let's fix that.

# Configuring `psql` with `.psqlrc`
The [`.psqlrc`
file](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-FILES-PSQLRC)
can be used to set defaults for new connections made with `psql`. It should be
placed in your home directory (i.e. `~/.psqlrc`) and most often contains `\set`
and `SET` commands.

The difference between `\set` and `SET` commands is a bit subtle. A [`SET`
command](https://www.postgresql.org/docs/current/sql-set.html) sets a session
variable inside of the PostgreSQL server, whereas a [`\set`
command](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMAND-SET)
sets configuration in the `psql` client itself.

## Making the default transaction read-only
PostgreSQL executes all statements as transactions. If you don't start an
explicit transaction for a statement, [PostgreSQL automatically wraps the
statement in a
transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html).
By default transactions are both readable and writable, which isn't necessarily
desirable. To make transactions read-only by default, you can set the following
session variable inside of PostgreSQL.

```sql
SET default_transaction_read_only="on";
```

You can do this in any PostgreSQL session. It can also be configured on the
database server, but here we assume it isn't. If you after having done that try
to execute a statement that writes to the database, you'll get an error.

```sql
test_db=# CREATE TABLE test_table (id serial);
ERROR:  cannot execute CREATE TABLE in a read-only transaction
```

However, it's still possible to create an explicit transaction that's allowed
to write, so it doesn't hinder you if you do need to write.

```sql
test_db=# BEGIN READ WRITE;
BEGIN
test_db=*# CREATE TABLE test_table (id serial);
CREATE TABLE
test_db=*# COMMIT;
COMMIT
```

To set this in `.psqlrc`, simply add the exact same line you'd use in an
interactive session to `~/.psqlrc`. When you connect to a database, any `SET`
command in `.psqlrc` is automatically executed.

> **Pitfall:** `SET` commands in `.psqlrc` are only executed when you
> first establish a connection to the database server. If you _switch_ database
> after having connected with `\c`, the `SET` command is _not_ executed again.
> Keep that in mind.

## Disabling autocommit
[`psql` automatically
commits](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-FILES-PSQLRC)
the implicit transaction created when you execute a statement outside of an
explicit transaction. This can be altered such that `psql` implicitly creates a
transaction without automatically committing it by setting the `AUTOCIMMIT` variable to `off`. This is a `psql` variable, so we use `\set` to set it.

```sql
\set AUTOCOMMIT false
```

To validate that it's working as expected, you should look for the `*` in the
`psql` prompt.

```sql
test_db=# CREATE TABLE test_table (id serial);
CREATE TABLE
test_db=*# ROLLBACK; # <--- * in the prompt signifies transaction
ROLLBACK
```

Do note that this transaction is _writable_ regardless of the value set on
`default_transaction_read_only`. In other words, it isn't meaningful to use
both, but it's important to know that one makes the other one meaningless.

# Summary
When connecting to any database that you for some reason don't want to
accidentally write to, you should have guardrails. Many graphical PostgreSQL
clients that I've seen my colleagues use have such guardrails by default in
that an explicit commit must be issued by clicking a button. `psql` does not.

Which of the two options in this article to use is a bit circumstantial. I
personally prefer disabling `AUTOCOMMIT` in `psql` as that is a client-side
setting. Setting `default_transaction_read_only` to on is a bit precarious as
it doesn't get reapplied if you change database with `\c`. The latter can
however be configured on the server itself, which is always a nice safety net
to have as it reduces the risk of errant commits due to client
misconfiguration. 

But this article was about `psql` in particular and in that context disabling
`AUTOCOMMIT` seems like the clear winner in terms of guardrails.
