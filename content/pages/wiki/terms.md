Title: Terms
Slug: wiki/terms

This is my (currently not so) big list of software engineering terminology and
definitions, in alphabetical order.

* Cooperative multitasking
    - Tasks run and yield control to other tasks of their own volition
    - Common in event loops, such as `asyncio` in `Python`
* Exit status
    - A special termination status that the process sets itself as it calls the
      `_exit()` system call
    - Note that `_exit()` is a system call - a process cannot terminate itself!
* File descriptor
    - Unique integer denoting an open file
    - Sometimes referred to as a _file handle_
* Group process id (GPID)
    - Only for shells with job control
    - Each process in a process group has the same GPID
    - The process group leader has `PID == GPID`
* Kernel space
    - Area of virtual memory that can only be accessed in kernel mode
* Parent process ID (PPID)
    - Process ID of the parent process
* Preemptive multitasking
    - A scheduler (such as an OS kernel) decides when and how tasks (e.g.
      processes) run.
    - See [Linux]({filename}linux.md)
* Process
    - A running instance of a program
* Process group
    - A collection of related processes
    - Sometimes called a _job_
    - Requires a shell with _job control_
* Process ID (PID)
    - A small non-negative integer representing the process
* Root (username)
    - The (most common) login name of the superuser on a *NIX system
* Root (hierarchy)
    - The topmost element of some hierarchy, usually a tree
* Session (UNIX)
    - A collection of process groups
    - Used primarily by job-control shells
* Session leader (UNIX)
    - Process that created its session
* Static library
    - A library that is statically linked with (i.e. copied into) a program at
      compile time
* Shared library
    - A library that is dynamically linked with a program as it is loaded
* Single UNIX Specification (SUS)
    - Standards for UNIX operating systems
    - Various versions, the most important one is SUSv3.
* Termination status
    - A small non-negative integer that is "emitted" by as the program terminates
    - Non-zero termination status indicates an error
* User space
    - Area of virtual memory that is allocated for a user mode process
* UNIX
    - Originally an operating system, now a set of standards
    - See [Linux]({filename}linux.md)
* Virtual private computer
    - Multi-user operating systems provide each user with a (mostly) private
      computer experience



## Referenced from

* [Linux]({filename}linux.md)

## Refers to

* [Linux]({filename}linux.md)
