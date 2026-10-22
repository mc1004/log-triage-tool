print("Log triage tool starting")

#opens the file and closes it again automatically when it's finished.
#for line in f: goes through the file one line at a time.
#line.strip() removes the invisible newline at the end of each line, so you don't get blank gaps between them.
#split(maxsplit=4) cuts the line at spaces, but only 4 times.
#parts[2] is the third piece, because Python starts counting at 0.
#split(": ", 1) cuts the rest of the line at the first ": " only.
# That matters because some messages contain colons of their own, like the EXT4 line.
#f"..." is an f-string. Whatever is in the {} gets filled in with that variable's value.

with open("samples/sample.log") as f:
    for line in f:
        parts = line.strip().split(maxsplit=4)
        time = parts[2]
        host = parts[3]
        service, message = parts[4].split(": ", 1)
        print(f"{time} | {host} | {service} | {message}")

