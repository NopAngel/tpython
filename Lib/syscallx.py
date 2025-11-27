import ctypes
import os
import sys
from ctypes import c_int, c_void_p, c_char_p, c_size_t, c_ssize_t

libc = ctypes.CDLL("libc.so.6")

class Timespec(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_long),
        ("tv_nsec", ctypes.c_long)
    ]

class Stat(ctypes.Structure):
    _fields_ = [
        ("st_dev", ctypes.c_ulong),
        ("st_ino", ctypes.c_ulong),
        ("st_mode", ctypes.c_uint),
        ("st_nlink", ctypes.c_ulong),
        ("st_uid", ctypes.c_uint),
        ("st_gid", ctypes.c_uint),
        ("st_rdev", ctypes.c_ulong),
        ("st_size", ctypes.c_ulong),
        ("st_blksize", ctypes.c_ulong),
        ("st_blocks", ctypes.c_ulong),
        ("st_atime", ctypes.c_ulong),
        ("st_mtime", ctypes.c_ulong),
        ("st_ctime", ctypes.c_ulong)
    ]

class Syscallx:
    def __init__(self):
        # Syscall numbers x86_64
        self.SYS_READ = 0
        self.SYS_WRITE = 1
        self.SYS_OPEN = 2
        self.SYS_CLOSE = 3
        self.SYS_STAT = 4
        self.SYS_FSTAT = 5
        self.SYS_LSTAT = 6
        self.SYS_POLL = 7
        self.SYS_LSEEK = 8
        self.SYS_MMAP = 9
        self.SYS_MPROTECT = 10
        self.SYS_MUNMAP = 11
        self.SYS_BRK = 12
        self.SYS_RT_SIGACTION = 13
        self.SYS_RT_SIGPROCMASK = 14
        self.SYS_IOCTL = 16
        self.SYS_PREAD64 = 17
        self.SYS_PWRITE64 = 18
        self.SYS_READV = 19
        self.SYS_WRITEV = 20
        self.SYS_ACCESS = 21
        self.SYS_PIPE = 22
        self.SYS_SELECT = 23
        self.SYS_SCHED_YIELD = 24
        self.SYS_MREMAP = 25
        self.SYS_MSYNC = 26
        self.SYS_MINCORE = 27
        self.SYS_MADVISE = 28
        self.SYS_SHMGET = 29
        self.SYS_SHMAT = 30
        self.SYS_SHMCTL = 31
        self.SYS_DUP = 32
        self.SYS_DUP2 = 33
        self.SYS_PAUSE = 34
        self.SYS_NANOSLEEP = 35
        self.SYS_GETITIMER = 36
        self.SYS_ALARM = 37
        self.SYS_SETITIMER = 38
        self.SYS_GETPID = 39
        self.SYS_SENDFILE = 40
        self.SYS_SOCKET = 41
        self.SYS_CONNECT = 42
        self.SYS_ACCEPT = 43
        self.SYS_SENDTO = 44
        self.SYS_RECVFROM = 45
        self.SYS_SENDMSG = 46
        self.SYS_RECVMSG = 47
        self.SYS_SHUTDOWN = 48
        self.SYS_BIND = 49
        self.SYS_LISTEN = 50
        self.SYS_GETSOCKNAME = 51
        self.SYS_GETPEERNAME = 52
        self.SYS_SOCKETPAIR = 53
        self.SYS_SETSOCKOPT = 54
        self.SYS_GETSOCKOPT = 55
        self.SYS_CLONE = 56
        self.SYS_FORK = 57
        self.SYS_VFORK = 58
        self.SYS_EXECVE = 59
        self.SYS_EXIT = 60
        self.SYS_WAIT4 = 61
        self.SYS_KILL = 62
        self.SYS_UNAME = 63
        self.SYS_SEMGET = 64
        self.SYS_SEMOP = 65
        self.SYS_SEMCTL = 66
        self.SYS_SHMDT = 67
        self.SYS_MSGGET = 68
        self.SYS_MSGSND = 69
        self.SYS_MSGRCV = 70
        self.SYS_MSGCTL = 71
        self.SYS_FCNTL = 72
        self.SYS_FLOCK = 73
        self.SYS_FSYNC = 74
        self.SYS_FDATASYNC = 75
        self.SYS_TRUNCATE = 76
        self.SYS_FTRUNCATE = 77
        self.SYS_GETDENTS = 78
        self.SYS_GETCWD = 79
        self.SYS_CHDIR = 80
        self.SYS_FCHDIR = 81
        self.SYS_RENAME = 82
        self.SYS_MKDIR = 83
        self.SYS_RMDIR = 84
        self.SYS_CREAT = 85
        self.SYS_LINK = 86
        self.SYS_UNLINK = 87
        self.SYS_SYMLINK = 88
        self.SYS_READLINK = 89
        self.SYS_CHMOD = 90
        self.SYS_FCHMOD = 91
        self.SYS_CHOWN = 92
        self.SYS_FCHOWN = 93
        self.SYS_LCHOWN = 94
        self.SYS_UMASK = 95
        self.SYS_GETTIMEOFDAY = 96
        self.SYS_GETRLIMIT = 97
        self.SYS_GETRUSAGE = 98
        self.SYS_SYSINFO = 99
        self.SYS_TIMES = 100
        self.SYS_PTRACE = 101
        self.SYS_GETUID = 102
        self.SYS_SYSLOG = 103
        self.SYS_GETGID = 104
        self.SYS_SETUID = 105
        self.SYS_SETGID = 106
        self.SYS_GETEUID = 107
        self.SYS_GETEGID = 108
        self.SYS_SETPGID = 109
        self.SYS_GETPPID = 110
        self.SYS_GETPGRP = 111
        self.SYS_SETSID = 112
        self.SYS_SETREUID = 113
        self.SYS_SETREGID = 114
        self.SYS_GETGROUPS = 115
        self.SYS_SETGROUPS = 116
        self.SYS_SETRESUID = 117
        self.SYS_GETRESUID = 118
        self.SYS_SETRESGID = 119
        self.SYS_GETRESGID = 120
        self.SYS_GETPGID = 121
        self.SYS_SETFSUID = 122
        self.SYS_SETFSGID = 123
        self.SYS_GETSID = 124
        self.SYS_CAPGET = 125
        self.SYS_CAPSET = 126
        self.SYS_RT_SIGPENDING = 127
        self.SYS_RT_SIGTIMEDWAIT = 128
        self.SYS_RT_SIGQUEUEINFO = 129
        self.SYS_RT_SIGSUSPEND = 130
        self.SYS_SIGALTSTACK = 131
        self.SYS_UTIME = 132
        self.SYS_MKNOD = 133
        self.SYS_USELIB = 134
        self.SYS_PERSONALITY = 135
        self.SYS_USTAT = 136
        self.SYS_STATFS = 137
        self.SYS_FSTATFS = 138
        self.SYS_SYSFS = 139
        self.SYS_GETPRIORITY = 140
        self.SYS_SETPRIORITY = 141
        self.SYS_SCHED_SETPARAM = 142
        self.SYS_SCHED_GETPARAM = 143
        self.SYS_SCHED_SETSCHEDULER = 144
        self.SYS_SCHED_GETSCHEDULER = 145
        self.SYS_SCHED_GET_PRIORITY_MAX = 146
        self.SYS_SCHED_GET_PRIORITY_MIN = 147
        self.SYS_SCHED_RR_GET_INTERVAL = 148
        self.SYS_MLOCK = 149
        self.SYS_MUNLOCK = 150
        self.SYS_MLOCKALL = 151
        self.SYS_MUNLOCKALL = 152
        self.SYS_VHANGUP = 153
        self.SYS_MODIFY_LDT = 154
        self.SYS_PIVOT_ROOT = 155
        self.SYS__SYSCTL = 156
        self.SYS_PRCTL = 157
        self.SYS_ARCH_PRCTL = 158
        self.SYS_ADJTIMEX = 159
        self.SYS_SETRLIMIT = 160
        self.SYS_CHROOT = 161
        self.SYS_SYNC = 162
        self.SYS_ACCT = 163
        self.SYS_SETTIMEOFDAY = 164
        self.SYS_MOUNT = 165
        self.SYS_UMOUNT2 = 166
        self.SYS_SWAPON = 167
        self.SYS_SWAPOFF = 168
        self.SYS_REBOOT = 169
        self.SYS_SETHOSTNAME = 170
        self.SYS_SETDOMAINNAME = 171
        self.SYS_IOPL = 172
        self.SYS_IOPERM = 173
        self.SYS_CREATE_MODULE = 174
        self.SYS_INIT_MODULE = 175
        self.SYS_DELETE_MODULE = 176
        self.SYS_GET_KERNEL_SYMS = 177
        self.SYS_QUERY_MODULE = 178
        self.SYS_QUOTACTL = 179
        self.SYS_NFSSERVCTL = 180
        self.SYS_GETPMSG = 181
        self.SYS_PUTPMSG = 182
        self.SYS_AFS_SYSCALL = 183
        self.SYS_TUXCALL = 184
        self.SYS_SECURITY = 185
        self.SYS_GETTID = 186
        self.SYS_READAHEAD = 187
        self.SYS_SETXATTR = 188
        self.SYS_LSETXATTR = 189
        self.SYS_FSETXATTR = 190
        self.SYS_GETXATTR = 191
        self.SYS_LGETXATTR = 192
        self.SYS_FGETXATTR = 193
        self.SYS_LISTXATTR = 194
        self.SYS_LLISTXATTR = 195
        self.SYS_FLISTXATTR = 196
        self.SYS_REMOVEXATTR = 197
        self.SYS_LREMOVEXATTR = 198
        self.SYS_FREMOVEXATTR = 199
        self.SYS_TKILL = 200
        self.SYS_TIME = 201
        self.SYS_FUTEX = 202
        self.SYS_SCHED_SETAFFINITY = 203
        self.SYS_SCHED_GETAFFINITY = 204
        self.SYS_SET_THREAD_AREA = 205
        self.SYS_IO_SETUP = 206
        self.SYS_IO_DESTROY = 207
        self.SYS_IO_GETEVENTS = 208
        self.SYS_IO_SUBMIT = 209
        self.SYS_IO_CANCEL = 210
        self.SYS_GET_THREAD_AREA = 211
        self.SYS_LOOKUP_DCOOKIE = 212
        self.SYS_EPOLL_CREATE = 213
        self.SYS_EPOLL_CTL_OLD = 214
        self.SYS_EPOLL_WAIT_OLD = 215
        self.SYS_REMAP_FILE_PAGES = 216
        self.SYS_GETDENTS64 = 217
        self.SYS_SET_TID_ADDRESS = 218
        self.SYS_RESTART_SYSCALL = 219
        self.SYS_SEMTIMEDOP = 220
        self.SYS_FADVISE64 = 221
        self.SYS_TIMER_CREATE = 222
        self.SYS_TIMER_SETTIME = 223
        self.SYS_TIMER_GETTIME = 224
        self.SYS_TIMER_GETOVERRUN = 225
        self.SYS_TIMER_DELETE = 226
        self.SYS_CLOCK_SETTIME = 227
        self.SYS_CLOCK_GETTIME = 228
        self.SYS_CLOCK_GETRES = 229
        self.SYS_CLOCK_NANOSLEEP = 230
        self.SYS_EXIT_GROUP = 231
        self.SYS_EPOLL_WAIT = 232
        self.SYS_EPOLL_CTL = 233
        self.SYS_TGKILL = 234
        self.SYS_UTIMES = 235
        self.SYS_VSERVER = 236
        self.SYS_MBIND = 237
        self.SYS_SET_MEMPOLICY = 238
        self.SYS_GET_MEMPOLICY = 239
        self.SYS_MQ_OPEN = 240
        self.SYS_MQ_UNLINK = 241
        self.SYS_MQ_TIMEDSEND = 242
        self.SYS_MQ_TIMEDRECEIVE = 243
        self.SYS_MQ_NOTIFY = 244
        self.SYS_MQ_GETSETATTR = 245
        self.SYS_KEXEC_LOAD = 246
        self.SYS_WAITID = 247
        self.SYS_ADD_KEY = 248
        self.SYS_REQUEST_KEY = 249
        self.SYS_KEYCTL = 250
        self.SYS_IOPRIO_SET = 251
        self.SYS_IOPRIO_GET = 252
        self.SYS_INOTIFY_INIT = 253
        self.SYS_INOTIFY_ADD_WATCH = 254
        self.SYS_INOTIFY_RM_WATCH = 255
        self.SYS_MIGRATE_PAGES = 256
        self.SYS_OPENAT = 257
        self.SYS_MKDIRAT = 258
        self.SYS_MKNODAT = 259
        self.SYS_FCHOWNAT = 260
        self.SYS_FUTIMESAT = 261
        self.SYS_NEWFSTATAT = 262
        self.SYS_UNLINKAT = 263
        self.SYS_RENAMEAT = 264
        self.SYS_LINKAT = 265
        self.SYS_SYMLINKAT = 266
        self.SYS_READLINKAT = 267
        self.SYS_FCHMODAT = 268
        self.SYS_FACCESSAT = 269
        self.SYS_PSELECT6 = 270
        self.SYS_PPOLL = 271
        self.SYS_UNSHARE = 272
        self.SYS_SET_ROBUST_LIST = 273
        self.SYS_GET_ROBUST_LIST = 274
        self.SYS_SPLICE = 275
        self.SYS_TEE = 276
        self.SYS_SYNC_FILE_RANGE = 277
        self.SYS_VMSPLICE = 278
        self.SYS_MOVE_PAGES = 279
        self.SYS_UTIMENSAT = 280
        self.SYS_EPOLL_PWAIT = 281
        self.SYS_SIGNALFD = 282
        self.SYS_TIMERFD_CREATE = 283
        self.SYS_EVENTFD = 284
        self.SYS_FALLOCATE = 285
        self.SYS_TIMERFD_SETTIME = 286
        self.SYS_TIMERFD_GETTIME = 287
        self.SYS_ACCEPT4 = 288
        self.SYS_SIGNALFD4 = 289
        self.SYS_EVENTFD2 = 290
        self.SYS_EPOLL_CREATE1 = 291
        self.SYS_DUP3 = 292
        self.SYS_PIPE2 = 293
        self.SYS_INOTIFY_INIT1 = 294
        self.SYS_PREADV = 295
        self.SYS_PWRITEV = 296
        self.SYS_RT_TGSIGQUEUEINFO = 297
        self.SYS_PERF_EVENT_OPEN = 298
        self.SYS_RECVMMSG = 299
        self.SYS_FANOTIFY_INIT = 300
        self.SYS_FANOTIFY_MARK = 301
        self.SYS_PRLIMIT64 = 302
        self.SYS_NAME_TO_HANDLE_AT = 303
        self.SYS_OPEN_BY_HANDLE_AT = 304
        self.SYS_CLOCK_ADJTIME = 305
        self.SYS_SYNCFS = 306
        self.SYS_SENDMMSG = 307
        self.SYS_SETNS = 308
        self.SYS_GETCPU = 309
        self.SYS_PROCESS_VM_READV = 310
        self.SYS_PROCESS_VM_WRITEV = 311
        self.SYS_KCMP = 312
        self.SYS_FINIT_MODULE = 313
        self.SYS_SCHED_SETATTR = 314
        self.SYS_SCHED_GETATTR = 315
        self.SYS_RENAMEAT2 = 316
        self.SYS_SECCOMP = 317
        self.SYS_GETRANDOM = 318
        self.SYS_MEMFD_CREATE = 319
        self.SYS_KEXEC_FILE_LOAD = 320
        self.SYS_BPF = 321
        self.SYS_EXECVEAT = 322
        self.SYS_USERFAULTFD = 323
        self.SYS_MEMBARRIER = 324
        self.SYS_MLOCK2 = 325
        self.SYS_COPY_FILE_RANGE = 326
        self.SYS_PREADV2 = 327
        self.SYS_PWRITEV2 = 328
        self.SYS_PKEY_MPROTECT = 329
        self.SYS_PKEY_ALLOC = 330
        self.SYS_PKEY_FREE = 331
        self.SYS_STATX = 332
        self.SYS_IO_PGETEVENTS = 333
        self.SYS_RSEQ = 334
        self.SYS_PIDFD_SEND_SIGNAL = 424
        self.SYS_IO_URING_SETUP = 425
        self.SYS_IO_URING_ENTER = 426
        self.SYS_IO_URING_REGISTER = 427
        self.SYS_OPEN_TREE = 428
        self.SYS_MOVE_MOUNT = 429
        self.SYS_FSOPEN = 430
        self.SYS_FSCONFIG = 431
        self.SYS_FSMOUNT = 432
        self.SYS_FSPICK = 433
        self.SYS_PIDFD_OPEN = 434
        self.SYS_CLONE3 = 435
        self.SYS_CLOSE_RANGE = 436
        self.SYS_OPENAT2 = 437
        self.SYS_PIDFD_GETFD = 438
        self.SYS_FACCESSAT2 = 439
        self.SYS_PROCESS_MADVISE = 440
        self.SYS_EPOLL_PWAIT2 = 441
        self.SYS_MOUNT_SETATTR = 442
        self.SYS_QUOTACTL_FD = 443
        self.SYS_LANDLOCK_CREATE_RULESET = 444
        self.SYS_LANDLOCK_ADD_RULE = 445
        self.SYS_LANDLOCK_RESTRICT_SELF = 446
        self.SYS_MEMFD_SECRET = 447
        self.SYS_PROCESS_MRELEASE = 448
        self.SYS_FUTEX_WAITV = 449
        self.SYS_SET_MEMPOLICY_HOME_NODE = 450

    def syscall(self, num, *args):
        return libc.syscall(num, *args)

    def getpid(self):
        return self.syscall(self.SYS_GETPID)

    def gettid(self):
        return self.syscall(self.SYS_GETTID)

    def fork(self):
        return self.syscall(self.SYS_FORK)

    def exit(self, status):
        self.syscall(self.SYS_EXIT, status)

    def open(self, pathname, flags, mode=0o644):
        return self.syscall(self.SYS_OPEN, pathname.encode(), flags, mode)

    def close(self, fd):
        return self.syscall(self.SYS_CLOSE, fd)

    def read(self, fd, buf, count):
        return self.syscall(self.SYS_READ, fd, buf, count)

    def write(self, fd, buf, count):
        return self.syscall(self.SYS_WRITE, fd, buf, count)

    def brk(self, addr=0):
        return self.syscall(self.SYS_BRK, addr)

    def mmap(self, addr, length, prot, flags, fd=-1, offset=0):
        return self.syscall(self.SYS_MMAP, addr, length, prot, flags, fd, offset)

    def munmap(self, addr, length):
        return self.syscall(self.SYS_MUNMAP, addr, length)

    def mprotect(self, addr, length, prot):
        return self.syscall(self.SYS_MPROTECT, addr, length, prot)

    def nanosleep(self, req, rem=None):
        if rem is None:
            rem = Timespec()
        return self.syscall(self.SYS_NANOSLEEP, ctypes.byref(req), ctypes.byref(rem))

    def gettimeofday(self, tv, tz=None):
        return self.syscall(self.SYS_GETTIMEOFDAY, tv, tz)

    def kill(self, pid, sig):
        return self.syscall(self.SYS_KILL, pid, sig)

    def uname(self, buf):
        return self.syscall(self.SYS_UNAME, buf)

    def ioctl(self, fd, request, arg=0):
        return self.syscall(self.SYS_IOCTL, fd, request, arg)

    def socket(self, domain, type, protocol):
        return self.syscall(self.SYS_SOCKET, domain, type, protocol)

    def bind(self, sockfd, addr, addrlen):
        return self.syscall(self.SYS_BIND, sockfd, addr, addrlen)

    def connect(self, sockfd, addr, addrlen):
        return self.syscall(self.SYS_CONNECT, sockfd, addr, addrlen)

    def listen(self, sockfd, backlog):
        return self.syscall(self.SYS_LISTEN, sockfd, backlog)

    def accept(self, sockfd, addr, addrlen):
        return self.syscall(self.SYS_ACCEPT, sockfd, addr, addrlen)

    def clone(self, fn, child_stack, flags, arg):
        return self.syscall(self.SYS_CLONE, fn, child_stack, flags, arg)

    def execve(self, filename, argv, envp):
        return self.syscall(self.SYS_EXECVE, filename, argv, envp)

    def wait4(self, pid, wstatus, options, rusage):
        return self.syscall(self.SYS_WAIT4, pid, wstatus, options, rusage)

    def getrandom(self, buf, buflen, flags):
        return self.syscall(self.SYS_GETRANDOM, buf, buflen, flags)

    def memfd_create(self, name, flags):
        return self.syscall(self.SYS_MEMFD_CREATE, name.encode(), flags)

    def pidfd_open(self, pid, flags):
        return self.syscall(self.SYS_PIDFD_OPEN, pid, flags)

    def process_vm_readv(self, pid, local_iov, liovcnt, remote_iov, riovcnt, flags):
        return self.syscall(self.SYS_PROCESS_VM_READV, pid, local_iov, liovcnt, remote_iov, riovcnt, flags)

    def process_vm_writev(self, pid, local_iov, liovcnt, remote_iov, riovcnt, flags):
        return self.syscall(self.SYS_PROCESS_VM_WRITEV, pid, local_iov, liovcnt, remote_iov, riovcnt, flags)
