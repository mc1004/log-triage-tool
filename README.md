# log-triage-tool
Log triage tool in Python. 

## Why I built it
To help me analyse log data

## What it does
- reads syslog-style logs
- picks out errors and repeated failures
- writes a short summary report. 

## How to run it
```
py triage.py
```
Requires Python 3 to be installed.

## Example output
```
Log triage report for samples/sample.log
Generated: 2026-10-22 16:02

PROBLEM: 09:14:02 | web01 | sshd[1234] | Failed password for invalid user admin from 203.0.113.5 port 52211 ssh2
PROBLEM: 09:14:05 | web01 | sshd[1234] | Failed password for invalid user admin from 203.0.113.5 port 52212 ssh2
PROBLEM: 09:15:10 | db01 | kernel | EXT4-fs error (device sda1): ext4_find_entry: reading directory lblock 0
PROBLEM: 09:16:00 | web01 | nginx[880] | [error] upstream timed out while reading response header
PROBLEM: 09:17:30 | stor01 | multipathd[512] | sdb: path failed, checker reported path is down
PROBLEM: 09:21:05 | db01 | backup.sh[2202] | ERROR: backup target /mnt/nas unreachable

6 problem lines found

Problems by host and service:
  web01 sshd: 2
  db01 kernel: 1
  web01 nginx: 1
  stor01 multipathd: 1
  db01 backup.sh: 1
```
## How it works
- splits each line into fields,
- checks the message against a keyword list,
- tallies by host and service.

## What I learned
- The sample log wouldn't upload. The Python .gitignore template ignores every *.log file. You added !samples/*.log as an exception.
- 7 problems were flagged instead of 6. I spotted that "Started Daily apt download activities" wasn't a real problem. It was a false positive, because "download" contains "down".
- I fixed it by changing the keyword to "is down".
- splitting log lines into fields and using Counter to tally problems by host and service.

## What I'd improve next
- Choosing which log file to read. At the moment it always reads samples/sample.log. Being able to run something like py triage.py /var/log/syslog would make it useful on real logs.
- Spotting repeats over time. For example, flag it if the same host gets more than 3 failed SSH logins in a minute, which looks like a brute-force attempt rather than a typo.
- Simple tests. A couple of automated checks, for example that a normal line isn't flagged and an error line is.
- Handling messy lines. A blank or oddly formatted line may currently crash it
