# File Upload Vulnerabilities

Michael Bailey | 7/22/21

IP: 10.10.34.150

Steps to run:

Run the following command:

```
echo "10.10.34.150    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm" | sudo tee -a /etc/hosts
```

At the end of the room, run:

```
sudo sed -i '$d' /etc/hosts
```

## Intro

It suggests that I go through the the CC:Pentesting room and the What The Shell room before doing this one.

I did them now, learned some!

## Overwriting Existing Files

If a system isn't well configured, then it's possible to upload a new image or file which overwrites the original file, if given the same name

### Questions

http://overwrite.uploadvulns.thm/

- What is the name of the image file which can be overwritten? [`mountains.jpg`]

```html
<body>
<img src="images/mountains.jpg" alt="">
<main>
```

- Overwrite the image. What is the flag you receive? [`THM{OTBiODQ3YmNjYWZhM2UyMmYzZDNiZjI5} `]

## Remote Code Execution

If files are not filtered, then they can be used as payloads for remote code execution. While most users that run the apps have no access to important files, they can still be dangerous

### Questions

Run a Gobuster scan on the website using the syntax from the screenshot above. What directory looks like it might be used for uploads? [`/resources`]

- `gobuster dir -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://shell.uploadvulns.thm/` 

Get either a web shell or a reverse shell on the machine. What's the flag in the /var/www/ directory of the server? [`THM{YWFhY2U3ZGI4N2QxNmQzZjk0YjgzZDZk}`]

- Used the [`basic-rev-shell.php`](../network_exploit_basics/revshell_files/basic-rev-shell.php) script
- Tried to reverse shell in, but the machine didn't have nc or socat
- Was able to traverse the file system and get the flag

## Filtering

Client and server-side filtering is usually done on files to ensure better security, through several different methods

- Extension Validation: checks the extension of the file passed through
- File Type Filtering: similar to extension checking, except actually looking at the contents/types of the file
  - Multipurpose Internet Mail Extension Validation (MIME Type Extension). The MIME type gets attached to the upload request and is used to check if the file matches
  - Magic Number Validation: checks the bytes at the top of a file to determine its type
- File Name Filtering: takes out any bad characters or checks if the file already exists
- File Content Filtering: actually scans the entire file, much harder to pass through

## General Plan of Attack

- Look at the website as a whole. Use Wappalyzer or take a look at the requests being sent out to see if headers make a determination of how the site is running
- When an upload page is found, take a look at any scripts which might be used for client-side filtering
- Do a happy path file upload using a file that makes sense (like a .png). Check from there to see if we can access it somewhere or see the result of it somehow. Gobuster can help with the `-x` command
- We can then start to attempt a malicious file upload and from there take into consideration any server-side filtering which may be happening
  - A successful upload with a bad extension (i.e. `.invalidending`) would mean that an extension blacklist may be at play. Otherwise, it's probably a whitelist
  - Then try changing the hex on the happy path file to magic numbers of a bad file like PHP. If it fails then magic number filters are in play
  - Also try changing the MIME type by intercepting the upload request using Burp Suite
  - Also see about file size limits, as they may be too small for certain files

### Client-Side CTF

Flag: `THM{NDllZDQxNjJjOTE0YWNhZGY3YjljNmE2}`

- Walked around the page some, gobuster found a `/images` and a `/assets` folder
- Looked into the source, in `/assets`, where was a client-side filtering JS file
- In it, it checks that the MIME type is `image/png`
- Running the happy path, I uploaded a PNG I had, which showed up in `/images`
- The route I went with was changing the response that the server was going to send back to the browser to no longer include the filter
- With the filter out, I was able to upload a [revshell PHP file](../network_exploit_basics/revshell_files/rev-shell-example.php). I started `pwncat` by activating the venv in it and running it with `-m`, then I ran the reverse shell file, navigated the local system and found the flag

They mentioned another route where you change the actual script itself to allow for PHP files to come in, but with the script being a static asset in another spot, that was going to be much harder than taking it off

### Server-Side Extensions CTF

Flag: `THM{MGEyYzJiYmI3ODIyM2FlNTNkNjZjYjFl}`

- The uploaded files were in `/privacy`
- I tried `.php`, didn't work, went through a few and found that `.php5` worked
- I just used the basic command script to just cat the flag

### Server-Side Magic Numbers CTF

Flag: `THM{MWY5ZGU4NzE0ZDlhNjE1NGM4ZThjZDJh}`

- On [the Wikipedia page](https://en.wikipedia.org/wiki/List_of_file_signatures), it notes that `47 49 46 38 37 61` is the file signature for GIFs, which are the only files allowed
- I tried to upload [one](./upload_vulns_files/shaggy.gif) manually but it was too big ☹️
- Files are in `/graphics`
- Using CyberChef, saw that the beginning of the PHP file needs to have `GIF87a`
- I was able to upload the file and go into it, got the flag.

### Final Upload Vuln CTF

Flag: `THM{NzRlYTUwNTIzODMwMWZhMzBiY2JlZWU2}`

- I feel like a dumbass...I want to cry...
- First step was to happy path it, looked fine, saw that the new files were under `/content` under a three letter code, same ones as in the wordlist provided
- Found a `/admin` page which ran modules. I tried running stuff but nothing happened
- Knowing it was JS I ~~was supposed to but took almost an entire day to figure out~~ found a JS reverse shell on PayloadAllTheThings the first time. Definitely the first time. Yep... 😭
- I was then supposed to save that JS file as a JPG, and (new knowledge time), change my Burp Suite filter to grab static JS files (I didn't think this was even possible, still a big ole dumbass...), in which I was able to change it to where no client-side filters remained
- Then, you go back to admin, and, of course, why wouldn't this be the case, it's just running JS files manually using node, meaning it just takes a path. Of course it does, that was very obvious and I definitely saw that like the big smart person I am. Yes, very obvious. Yes...
- I took a path to the JS/JPG file and turned on nc, and I was in...
- I'm gonna take a nap, fuck this entire world...
