import subprocess


# subprocess.run("ls -la")
# entire command "ls -lah" won't work
"""
Traceback (most recent call last):
  File "/home/andy/labs/run_cmds.py", line 5, in <module>
    s1 = subprocess.run("ls -la")
  File "/usr/lib/python3.10/subprocess.py", line 503, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib/python3.10/subprocess.py", line 971, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.10/subprocess.py", line 1863, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ls -la'
"""

s1 = subprocess.run("ls")
"""
output.txt  run_cmds.py  venv
"""

print(s1)
"""
CompletedProcess(args='ls', returncode=0) returncode=0 means no error
"""

print(s1.stdout) # None
print(s1.stderr) # None

# Use list and break each into string for entire command
subprocess.run(["ls", "-la"])
"""
total 28
drwxr-xr-x  4 andy andy 4096 Jan 20 23:56 .
drwxr-x--- 12 andy andy 4096 Jan 21 00:15 ..
drwxr-xr-x  8 andy andy 4096 Jan 21 00:15 .git
-rw-r--r--  1 andy andy 1830 Jan 20 23:57 .gitignore
-rw-r--r--  1 andy andy  367 Jan 23 20:21 output.txt
-rw-r--r--  1 andy andy 2196 Jan 23 20:22 run_cmds.py
drwxr-xr-x  5 andy andy 4096 Dec 22 21:15 venv
"""

# shell=True allows the entire commands
subprocess.run("ls -lh", shell=True)
"""
total 12K
-rw-r--r-- 1 andy andy  367 Jan 23 20:21 output.txt
-rw-r--r-- 1 andy andy 2.2K Jan 23 20:22 run_cmds.py
drwxr-xr-x 5 andy andy 4.0K Dec 22 21:15 venv
"""

# Capture standout output
s4 = subprocess.run(["ps", "-a"], capture_output=True, text=True)
print(s4.stdout) # b'/home/andy/labs/venv/bin/python\n'

# Capture standout to a file.
with open("output.txt", "w") as f:
    s5 = subprocess.run(["ps", "-a"], stdout=f, text=True)

# Run bad command and capture error
s6 = subprocess.run(["ls", "-la", "notexit.txt"], capture_output=True, text=True)
"""
CompletedProcess(args=['ls', '-la', 'notexit.txt'], returncode=2, stdout='', stderr="ls: cannot access 'notexit.txt': No such file or directory\n")
"""

print(s6)
print(s6.stderr) # ls: cannot access 'notexit.txt': No such file or directory

# check=True to see the traceback error. WILL STOP THE PROGRAM
# s7 = subprocess.run(["ls", "-la", "notexit.txt"], capture_output=True, text=True, check=True)
"""
Traceback (most recent call last):
  File "/home/andy/labs/run_cmds.py", line 72, in <module>
    s7 = subprocess.run(["ls", "-la", "notexit.txt"], capture_output=True, text=True, check=True)
  File "/usr/lib/python3.10/subprocess.py", line 526, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['ls', '-la', 'notexit.txt']' returned non-zero exit status 2.
"""

# Ignore the error using devnull
s8 = subprocess.run(["ls", "-la", "notexit.txt"], stderr=subprocess.DEVNULL)
print(s8) # CompletedProcess(args=['ls', '-la', 'notexit.txt'], returncode=2)
print(s8.stderr) # None

# Run command with the input from s4 variable
s9 = subprocess.run(["grep", "-n", "python"], capture_output=True, text=True, input=s4.stdout)
print(s9.stdout) # 11:  11042 pts/6    00:00:00 python
