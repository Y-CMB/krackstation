# PreReq's
- Must have python installed
- Put krack*server*.py in the same Windows directory as hashcat (i.e. "C:\hashcat\ ---> krackserver.py)
- Make the run_script.bat a startup script. (Super + S > Task Scheduler > Create Task)
    - Check: "Run whether user is logged on or not" & "Run with highest privileges"
    - For Triggers select "New" > "At startup"
    - For Actions > Start a program > select .bat
    - If you're on a laptop, you may want to select Conditions > "Start the task only if the computer is on AC power"
    - I suggest Settings > Restart the task if it fails
    - If the startup script doesn't work, sue me, I'm not a developer

# Usage
```bash
python3 ./krackclient.py -hash '<HASH>' -m <MODE NUMBER> -s <WINDOWS IP>
```


### TODO:
- make wordlist an arg
    - send dict with data

- make port an option

- automatic mode server side