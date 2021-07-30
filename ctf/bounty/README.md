# Bounty Hunters

Michael Bailey | 7/27/21

[Rustscan](./logs/portscan_init.log)

[Gobuster](./logs/gobuster.log)

[Nikto](./logs/nikto.log)

FTP has anonymous access, files pulled down and put in `/ftp`

[Task File](./ftp/task.txt) - Potential username: `lin`

[Locks File](./ftp/locks.txt) - Wordlist of potential passwords

Going back in notes, `hydra` can brute force passwords for SSH logins

[Hydra log](./logs/hydra_lin_ssh.log) - lin:RedDr4gonSynd1cat3

Logged into SSH - user.txt found in ~/Desktop - `THM{CR1M3_SyNd1C4T3}`

Checked sudo, lin doesn't seem to have it. Checked for other users, only one is lin. Checked for SUID bit files, that was a dead end.

Found that the `00-header` script could be edited and is owned by root, but that one is weird and seems to be a dead end as well.

After looking at a writeup, it suggests running `sudo -l`, which lists `tar` as a runnable command as root

[GTFOBins has a privesc page for tar](https://gtfobins.github.io/gtfobins/tar/).

After running the script they suggest, I was in as root: `sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh`

Went to /root, got the flag there - `THM{80UN7Y_h4cK3r}`
