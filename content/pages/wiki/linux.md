Title: Linux
Slug: wiki/linux

[TOC]

# UNIX

Primarily notes from chapter 1 of TLPI

* Originally a specific operating system, with the first version
  developed at Bell Labs by Ken Thompson in 1969
  - Came in versions
* Nowadays, UNIX more often denotes a "UNIX-like" operating system,
  such as Linux distributions, macOS and BSD variants.
* The Open Group owns the UNIX trademark
    - They issue certifications for conformance to the _Single Unix
      Specification_ (SUS), of which there are multiple versions
    - For example, macOS 14 (Sonoma) is a certified SUSv3 OS
    - No Linux distribution I know of is a certified UNIX product

# Fundamentals

Primarily notes from chapter 2 of TLPI.

## Kernel

* Resides at `/etc/vmlinuz`
    - The trailing `z` denotes that the file is compressed
* Tasks performed by the kernel include
    - Process scheduling (Linux employs
      [_preemptive multitasking_]({filename}terms.md), including cration and
      termination
    - Memory management
    - File system provisioning
    - Device access - devices are exposed as files in `/dev`
    - Networking
    - System call API
    - Multi-user enviroment - each user gets a _virtual private computer_
* Kernel mode vs user mode
    - Modern CPUs provide hardware instructions for allowing processes to
      operate in _kernel_ or _user_ mode.
    - Areas of memory can be marked for either mode.
        - _Kernel space_ and _user space_
        - Kernel mode processes can access everything, whereas user mode
          processes are limited to _user space_
        - Kernel-specific data structures will be marked for kernel mode, which
          user processes cannot access 

## Users and groups

* User consists of
    - Login name (username)
    - Numeric user ID (UID)
    - Group ID - the _first_ group the user belongs to
    - Home directory
    - Login shell
* Users are stored in the `/etc/passwd` file
    - For security reasons, passwords are usually stored in `/etc/shadow`
* Group consists of
    - Group name
    - Numeric group id (GID)
    - User list - comma separated list of usernames that belong to the group
* Superuser
    - UID=0
    - Login name is most often _root_

## Directory hierarchy

* Single tree structure (i.e. just one root)
    - Contrast this to Windows, where each device has it's own directory
      hierarchy (e.g. `C:`, `D:` etc)
    - Devices are _mounted_ into the single directory hierarchy
* Files
    - In Linux, "everything is a file"
    - Files have different types: regular file, directory, pipes,
      sockets symbolic links etc.
* Directory
    - A file whose contents is a list of other files
    - Always has at least two entries
        - `.` denotes itself
        - `..` denotes its parent (except for the root directory, where
          `. == ..`)
* (Hard) link
    - An association between a filename and a specific file
* Symbolic link
    - A file that contains a path to another file
    - Sometimes called a _soft_ link to contrast it with a normal (or hard)
      link
* Filenames
    - The name of a file in a directory
    - Recommended to keep to the _portable filename character set_ specified by
      SUSv3: `[-._a-zA-Z0-9]`.
        - Even if most modern systems can handle a large range of UTF8.
        - Characters that have special meaning must be escaped
        - Some environments/programs may not support escaping, and then you're
          kind of pooped
* Pathnames
    - A `/`-separated list of directory names, except for the final entry which
      may be any kind of file
    - Absolute pathnames start with `/`, relative pathnames do not
* Current working directory   
    - Every process has a current working directory
    - The working directory is inherited from the parent process, or explicitly
      specified when a new process is created
    - A login shell always starts in the home directory of the logged in user
* File permissions
    - Each file has an associated UID and GID
    - Each file has a set of permissions
        - _read_ (`r`) - allows a file to be read
        - _write_ (`w`) - allows a file to be written
        - _execute_ (`x`) - allows a file to be executed
        - Permission bits are in the order `rwx`, so e.g. `7` is all
          permissions, while `4` is only `r` permission.
    - There are 9 permission bits, 3 each for _owner_, _group_ and _other_
        - So e.g. `744` translates to `rwx` for the owner, and only `r` for
          group and other
    - Directories have a slightly different interpretation of permissions
        - read - allows the filenames in the directory to be listed
        - write - allows filenames to be added or removed
        - execute (or _search_) - allows files to be read and written as per
          the permissions on the files themselves
            - A file with `777` permissions in a directory that lacks `x` still
              cannot be read!

## File I/O
* _Universality of I/O_
    - All I/O is done through accessing files with system calls such as
      `open()`, `read()`, `write()` etc.
    - It doesn't matter if the file is a device or a regular file
    - There's only one type of file access: a stream of bytes that you can get
      to any point in with the `lseek()` system call.
* File descriptors
    - A per-process unique and non-negative integer denoting an open file
    - Each process has a table of open file descriptors
    - Normally a process inherits descriptors 0 (stdout), 1 (stdin) and 2
      (stderror) from the parent process

## Processes
* A process is an instance of an executing program
* Process memory layout:
    - _Text_ - program instructions
    - _Data_ - static variables
    - _Heap_ - dynamically allocated memory
    - _Stack_ - automatically allocated memory
* Processes are created with the _fork()_ system call
    - _fork()_ clones the currently running process and creates a _child
      process_
    - A child process inherits copies of the parent's data, stack and heap
    - The text segment is shared between parent and child process
    - The child process will often immediately execute the `execve()` system
      call to execute some new program
* Process ID (PID)
    - A small non-negative integer representing the process
* Parent process ID (PPID)
    - Process ID of the parent process
* Group process id (GPID)
    - Only for shells with job control
    - Each process in a process group has the same GPID
    - The process group leader has `PID == GPID`
* Termination status
    - A small non-negative integer that is "emitted" by as the program terminates
    - Non-zero termination status indicates an error
* Exit status
    - A special termination status that the process sets itself as it calls the
      `_exit()` system call
    - Note that `_exit()` is a system call - a process cannot terminate itself!
* Processes have user and group ids
    - Real UID and GID - denote the user and group to which the process belong
      (that started the process)
    - Effective UID and GID - denote the user and group with which privileges
      the process is executing.
      - Most often the same as real UID/GID, but can differ e.g. by using
        `setuid`
    - Supplementary GIDs - additional groups the process belongs to
* Privileged processes
    - Any process running with effective UID 0 (root)
    - Bypasses any normal permission checks
    - Either started by root, or uses setuid
* Capabilities
    - Introduced in Linux 2.2, allows a subset of superuser privileges to be
      allowed
    - The superuser represents _all_ capabilities
* The _init_ process
    - The first process started when the OS starts
    - The praent of all processes, has PID 1
    - Cannot be stopped (even by the superuser)
    - Derived from `/sbin/init`
* Daemon (service)
    - Long-lived process that runs in the background
    - Usually does not have any associated terminal
    - Usually starts at system start and is managed by something like `systemd`
* Environment list
    - A process has a list of environment variables
    - Inherited from the parent process and thus provides a way for a parent
      process to "pass arguments" to a child process
* Resource limits
    - The resources a process can use can be limited with the `setrlimit()`
      system call
    - _Soft limit_ - the current resource limit, can be adjusted by the process
      itself
    - _Hard limit_ - the absolute resource limit, the soft limit cannot be
      adjusted beyond this point

## Memory mappings
* The `mmap()` system call creates a memory mapping
* File mapping
    - Maps a region of a file into the process address space
* Anonymous mapping
    - Does not need a corresponding file
    - Initializes the memory to 0s
* Can be used e.g. for:
    - Initializing a process text
    - Allocation of new memory (filled with 0s)
    - Memory-mapped I/O
    - Communication between processes using shared mappings

## Libraries
* Static libraries
    - Bundle of compiled object modules
    - Statically linked to a program at compile time - the libraries are
      _copied_ into the program text
* Shared libraries
    - Linked by a dynamic linker when the program starts
    - Requires that the shared library is available on the system the program
      executes on

## Interprocess communication (IPC)
* Processes need to communicate with each other, and can do so with
    - signals - to indicate that something has occurred
    - pipes and FIFOs - to transfer data
    - sockets - to transfer data to a process that may not be on the same host
    - file locking - to disallow other processes from reading or writing part
      of a file
    - message queues - to exchange messages
    - semaphores - to synchronize concurrent actions
    - shared memory - to read and write to the same memory

## Signals
* Used as IPC
* Used by the kernel to control programs, and can be sent if e.g.
    - A user pressed CTRL-C (SIGINT)
    - A user used the `kill` command
    - A timer expired
    - A process behaved badly

## Threads
* A process has one or more threads
* Threads (of a process) share, among other things
    - Resource limits
    - Address space
    - Program code
* Threads have their own stack pointer

## Sessions
* A session is a collection of process groups
* Session leader - the process that created the session
* All processes in a session have the same session id
* All processes created by a job-control shell belong to the same session as
  the shell itself
* Usually associated with a _controlling terminal_
    - Established when the session leader opens a terminal device
    - Usually the terminal with which the user logged in
    - The session leader becomes the _controlling process_
    - The controlling process receives a SIGHUP if the terminal disconnects
* _Foreground process group_ - the current "focused" process group
* _Background process group_ - any process group that is not the foreground
  process group

# File I/O

* Each process has a file descriptor table
    - File descriptors 0, 1 and 2 are by convention assigned to stdin, stdout and stderr
    - This can be changed with the `freopen()` system call!



## Referenced from

* [Terms]({filename}terms.md)

## Refers to

* [Terms]({filename}terms.md)
