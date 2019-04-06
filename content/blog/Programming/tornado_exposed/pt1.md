Title: TornadoFX+Exposed pt. 1: Project and database setup
Date: 2018-12-25T22:42:36Z
Modified: 2018-12-30T14:53:11Z
Author: Simon Larsén
Tags: kotlin,tornadofx,exposed,kuizzy
Category: Programming

I recently got it into my head that I'd like to make a quiz game with a GUI,
which felt like a simple enough diversion during the holidays. Since I already
have this site to maintain in terms of web development, I figured that desktop
app development in Kotlin using the TornadoFX framework would be a nice change
of pace. _Kuizzy_, which is what I call the project, will obviously need some
kind of data storage for questions and the like, so I settled on usind
JetBrains' framework Exposed with a sqlite database. Starting out, I had
trouble figuring out how to use TornadoFX and Exposed together, and therefore
decided to write this three-part series of articles on how I managed to make it
work. I won't dive deep into either, but rather show by example how to perform
some elementary tasks. In the end, we'll have a small piece of the database
admin part of Kuizzy up and running.

> The full source code is available
> [on GitHub](https://github.com/slarse/tornadofx-exposed-example/tree/part_1)

# Article index

1. Project and database setup -- This part!
2. [Showing a database table]({filename}pt2.md)
3. [Adding, editing and removing]({filename}pt3.md)

# Getting started
In this first article, we will be concerned only with getting everything set up.
This includes getting the dependencies and setting up the database with a table.
I will assume that you know how to use Kotlin, and how to handle dependencies
(e.g. by using a build system like Gradle, or just doing it manually). These are
things that I will not explain, as there are plenty of resources for that
available elsewhere. It's also important to note that these articles are not
meant to be seen as _the_ way to do this. In order to keep the articles
reasonably focused and short, I take tons of shortcuts, completely eschew error
handling and create very specialized functionality. The point of this article
series is to show you how to get started with TornadoFX+Exposed, and you are
meant to develop it further on your own.

## What are we aiming for?
I think it helps tremendously when reading something to have the end goal in
sight. What we're shooting for here is an interface that looks something like
this:

![Final app]({static}/images/tornado_exposed/final_gui.jpg)

We will be able to create and delete rows, as well as edit rows directly in
the table. It's not
pretty and it's not very user friendly, but it conveys an idea and has all the
basic functionality required do administrate a single-table database.
Now that you have a rough idea of what we're trying to accomplish, let's
have a look at what libraries and tools we need to make it happen.

## Preliminaries
Before we can get started, we need to make sure all dependencies are accounted
for. Here's a complete list of the libraries and frameworks I'll be using
throughout this series:

* Java 8 and openjfx 8
    - Note that if you install Oracle's JDK, JavaFX is included. You only need
      openjfx if you use openjdk.
* Kotlin 1.3.0
    - 1.2+ should work fine
* [TornadoFX 1.7.17](https://mvnrepository.com/artifact/no.tornado/tornadofx/1.7.17)
* [Exposed 0.11.2](https://mvnrepository.com/artifact/org.jetbrains.exposed/exposed/0.11.2)
* [xerial-sqlite-jdbc 3.25.2](https://mvnrepository.com/artifact/org.xerial/sqlite-jdbc/3.25.2)
    - I'll be using sqlite, but using any other SQL database supported by
      Exposed only requires changing a line or two of code.
* Gradle 5.0
    - Any reasonably up-to-date version should work. You can also just use
      whatever way you see fit to handle the dependencies.

Here's my `build.gradle`:

```json
plugins {
    id 'org.jetbrains.kotlin.jvm' version '1.3.0'
}

group 'se.slarse'
version '0.0.1'

repositories {
    mavenCentral()
    jcenter()
}

dependencies {
    compile 'org.jetbrains.kotlin:kotlin-stdlib-jdk8'
    compile 'no.tornado:tornadofx:1.7.17'
    compile 'org.jetbrains.exposed:exposed:0.11.2'
    compile 'org.xerial:sqlite-jdbc:3.25.2'
}

compileKotlin {
    kotlinOptions.jvmTarget = "1.8"
}

compileTestKotlin {
    kotlinOptions.jvmTarget = "1.8"
}
```

## Setting up the database
Any quiz game worth it's salt has categories, and that's the part of the
database that we'll develop. Exposed allows us to interact with a SQL database
in two different ways: through the SQL Domain Specific Language (DSL), or
through the Data Access Object (DAO) pattern. I'll use the DAO, as I thought it
meshed nicely with TornadoFX. You can read about both of them on the
[Exposed GitHub page](https://github.com/JetBrains/Exposed). We will put all of
the database code in a file called `database.kt`. Let's first define the table
for categories.

```kotlin
import org.jetbrains.exposed.dao.*
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.TransactionManager
import org.jetbrains.exposed.sql.transactions.transaction
import java.sql.Connection

object Categories : IntIdTable() {
    val name = varchar("name", 64).uniqueIndex()
    val description = varchar("description", 128)
}
```

Note that we don't explicitly define the primary key, that's all handled in the
background. Along with the table (which is a singleton object), we also need to
represent rows.

```kotlin
class Category(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<Category>(Categories)

    var name by Categories.name
    var description by Categories.description

    override fun toString(): String {
        return "Category(name=\"$name\", description=\"$description\")"
    }
}
```

The `Category` class is what we'll use to create DAOs, with which we can
create, modify and delete rows in the `Categories` table. Finally, let's create
the table and add some rows to it. We won't actually touch the `Categories`
object directly at all.

```kotlin
fun main(args: Array<String>) {
    // "connect" to database file called data.sqlite in the current working directory
    // (creates the file if it does not exist)
    Database.connect("jdbc:sqlite:file:data.sqlite", driver = "org.sqlite.JDBC")
    // this isolation level is required for sqlite, may not be applicable to other DBMS
    TransactionManager.manager.defaultIsolationLevel = Connection.TRANSACTION_SERIALIZABLE

    transaction {
        addLogger(StdOutSqlLogger)
        // create the table
        SchemaUtils.create(Categories)

        // add some entries
        Category.new {
            name = "java"
            description = "The Java programming language"
        }

        Category.new {
            name = "cpp"
            description = "The C++ programming language"
        }
    }

    // new transaction to check the results
    transaction {
        Category.all().forEach { println(it) }
    }
}
```

Note how all interactions with the database are conducted inside of a
`transaction` (which is a function taking a lambda, that abstracts a database
transaction). You'll see this several times throughout these articles. That's
it for database setup! If you run main function, you'll get output that looks
something like this:

```bash
SQL: CREATE TABLE IF NOT EXISTS Categories (id INTEGER PRIMARY KEY, name VARCHAR(64) NOT NULL, description VARCHAR(128) NOT NULL)
SQL: CREATE UNIQUE INDEX Categories_name ON Categories (name)
SQL: INSERT INTO Categories (description, name) VALUES ('The Java programming language', 'java')
SQL: INSERT INTO Categories (description, name) VALUES ('The C++ programming language', 'cpp')
Category(name="java", description="The Java programming language")
Category(name="cpp", description="The C++ programming language")
```

If you run the main function again, it will fail the unique constraint on the
`name` attribute and crash. And that's it for part 1. In the next part, we'll
look at how to create a read-only view of the `Categories` table. You can
find
[part 2 here]({filename}pt2.md).
