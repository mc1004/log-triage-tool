from collections import Counter
from datetime import datetime

print("Log triage tool starting")
PROBLEM_WORDS = ["error", "fail", "is down", "unreachable", "timed out"]
problem_count = 0
problems_by_source = Counter()
report_lines = []


#Each time you call report(""), it prints it and adds it to the report_lines list.
#text="" means calling report() on its own just adds a blank line.
def report(text=""):
    print(text)
    report_lines.append(text)

report("Log triage report for samples/sample.log")
#datetime.now():%Y-%m-%d %H:%M gives the current date and time, formatted like 2026-10-22 15:58.
report(f"Generated: {datetime.now():%Y-%m-%d %H:%M}")
report()

#opens the file and closes it again automatically when it's finished.
#for line in f: goes through the file one line at a time.
#line.strip() removes the invisible newline at the end of each line, so you don't get blank gaps between them.
#split(maxsplit=4) cuts the line at spaces, but only 4 times.
#parts[2] is the third piece, because Python starts counting at 0.
#split(": ", 1) cuts the rest of the line at the first ": " only.
# That matters because some messages contain colons of their own, like the EXT4 line.
#f"..." is an f-string. Whatever is in the {} gets filled in with that variable's value.
#message.lower() makes the message lower case so ERROR and error both match.
#any(...) is True if at least one of the words appears in the message.
#problem_count += 1 adds 1 to the counter each time a line matches.
#service.split("[")[0] turns sshd[1234] into sshd. 
#The number in brackets is the process ID, which changes every time.
#(host, service_name) uses the pair as the key, 
#so sshd on web01 is counted separately from sshd on another host.


with open("samples/sample.log") as f:
    for line in f:
        parts = line.strip().split(maxsplit=4)
        time = parts[2]
        host = parts[3]
        service, message = parts[4].split(": ", 1)
        if any(word in message.lower() for word in PROBLEM_WORDS):
            problem_count += 1
            service_name = service.split("[")[0]
            problems_by_source[(host, service_name)] += 1
            report(f"PROBLEM: {time} | {host} | {service} | {message}")

report(f"\n{problem_count} problem lines found")
report("\nProblems by host and service:")
for (host, service_name), count in problems_by_source.most_common():
    report(f"  {host} {service_name}: {count}")

#opens the file for writing. It creates the file, or overwrites it if it's already there.
#"\n".join(report_lines) glues all the lines together with a line break between each one.
with open("report.txt", "w") as out:
    out.write("\n".join(report_lines) + "\n")

print("\nReport saved to report.txt")