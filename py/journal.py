# The Python script prompts you to write a line of text which later gets appended to a text file with the format [YYYY-MM-DD].txt with Y being year, M being month and D being day. There will also be a time header above the newly written line if the .txt file is empty or if the last line in the file was written more than 10 minutes ago.
# notify_sound() may not work if the file in it's command string is missing
#
# Written by jnk181
# Tested Python versions: Python 3.13.1

import os
import datetime
import re
import math
import sys

new_header=False
if(len(sys.argv)>1):
    if(sys.argv[1]=="-n"):
        new_header=True

txt_directory="my_journal_txt"
new_date_header_after=21 #minutes

def minutes_passed_since(timestamp):
    try:
        time_object = datetime.datetime.strptime(timestamp, "%H:%M:%S").time()
        now = datetime.datetime.now().time()
        dummy_date = datetime.date.today()
        time_object_with_date = datetime.datetime.combine(dummy_date, time_object)
        now_with_date = datetime.datetime.combine(dummy_date, now)
        time_difference = now_with_date - time_object_with_date
        return math.floor(time_difference.seconds / 60)

    except ValueError:
        print("Invalid timestamp format. Please use HH:MM:SS")
        return None

def notify_sound():
    os.system("play -q ~/meet-message-sound-1.mp3 &")

date_string = datetime.date.today().strftime("%Y-%m-%d")
time_string = datetime.datetime.now().strftime("%H:%M:%S")

txt_filename=f"[{date_string}].txt"
if not os.path.exists(txt_directory):
    os.makedirs(txt_directory)

if os.path.exists(f"{txt_directory}/{txt_filename}"):
    txt_file_exists=True
    with open(f"{txt_directory}/{txt_filename}") as f: s = f.read()
    timestamp_headers=(re.findall(r'(^|\n)---- (\d{2}:\d{2}:\d{2}) ----($|\n)',s))
    recently_written=( minutes_passed_since(timestamp_headers[-1][1]) < new_date_header_after )
else:
    txt_file_exists=False
    recently_written=False

notify_sound()
print("Write a line to echo to the journal .txt file:")
txt_toappend=input()

with open(f"{txt_directory}/{txt_filename}", "a") as myfile:
    if(txt_file_exists):
        myfile.write(f"""\n""")
    if( (not recently_written) or new_header):
        myfile.write(f"""\n---- {time_string} ----\n""")
    myfile.write(f"""{txt_toappend}""")
