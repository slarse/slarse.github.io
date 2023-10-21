Title: Databases
Slug: wiki/databases

## Common problems with databases

> Note: Most of this paraphrased from the fantastic book [Designing Data-Intensive
Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/).

```
P1 = process 1
P2 = process 2
```

* Dirty read - P1 reads a value that P2 has written but not yet committed
    - Solution: Read committed isolation level or stronger.
* Dirty write - P1 overwrites a value that P2 has written but not yet committed
    - Solution: Any reasonable implementation of transactions.
* Read skew - P1 reads more than one row from the database, and gets rows from
  different points in time.
    - Solution: Snapshot isolation (e.g. Read Committed isolation level or stronger).
* Write skew - P1 reads a value V and then writes something W based o V.
  In the time between P1 reading V and writing W, P2 overwrites V with V'
  such that the premise of writing W is no longer true.
    - Solution: Serializable isolation level.
* Lost updates - Both P1 and P2 read and write to the same row, causing updates
  to be lost. The classic concurrent counter increment, for example.
    - Solution: Some implementations of snapshot isolation, otherwise row
      locking (e.g `SELECT FOR UPDATE`).
* Phantoms - P1 reads rows matching some search condition (e.g. "all dogs
  belonging to X"), and P2 concurrently writes something that changes the
  result of that search (e.g. "add new dog for X" or "remove dog from X").
    - Solution: There are many ways in which phantoms can manifest. Some can be
      prevented by snapshot isolation, but when combined with write skew you
      need something stronger like index-range locks.
* Deadlock - P1 locks row R1 and P2 locks row R2. P1 then tries to lock R2 and
  P2 tries to lock R1. P1 is waits for P2 to release the lock on R2, and P2
  waits for P1 to release the lock on R1.
    - Solution: The only surefire way to avoid deadlocking is to run
      transactions serially. Under normal operations with concurrent
      transaction execution deadlocks can occur, and the database should then
      abort one or both transactions that are part of the deadlock.


