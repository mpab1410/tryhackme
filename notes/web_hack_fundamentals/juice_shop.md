# Juice Shop

Michael Bailey | 7/22/21

IP: 10.10.33.136 | 10.10.248.221

## Task 1 - Reconnaissance

- What's the Administrator's email address? [`admin@juice-sh.op`]
  - Found under the Apple Juice item
- What parameter is used for searching? [`q`]
  - `http://10.10.33.136/#/search?q=apple`
- What show does Jim reference in his review? [`Star Trek`]
  - Jim's review is under the Green Smoothie item. He mentioned a `replicator`, which Google says is from Star Trek

## Task 2 - Injection

- Log into the administrator account. What is the flag? [`32a5e0f21372bcc1000a6088b93b458e41f0e02a`]
  - Used SQL injection on `/rest/user/login`
  - email: `' OR 1=1--`
- Log into the Bender account. What is the flag? [`fb364762a3c102b2db932069c0e6b78e738d4066`]
  - email: `bender@juice-sh.op'--`
  - Password check would be commented out behind it

## Task 3 - Broken Authentication

- Bruteforce the Administrator account's password. What is the flag? [`c2110d06dc6f81c67cd8099ff0ba601241f1ac0e`]
  - Tried using a different wordlist and Burp Suite, but it was horrendously slow
  - Made [a python script](./juice_shop_files/bruteforce.py) that went through the `best1050.txt` under `/usr/share/seclists`
  - It found `admin123` as the password
- Reset Jim's password. What is the flag? [`094fbc9b48e525150ba97d05b942bbf114987257`]
  - Ok, so the room had something very specific for this one, I guess just to show another exploit
  - Using the password reset link from the login page, we get a prompt for an email, a security answer, and a new password
  - Using info from earlier, Jim likes Star Trek. Jim Star Trek in Google leads to the James T Kirk page.
  - James T Kirk has a brother with the middle name Samuel. Which happens to be the security question
  - Inserted it, it liked it, changed the password to `password`, got the flag, cool...
  - I didn't like this one, would have liked something a bit more inquisitive or something. Or some kind of file lookup or something

## Task 4 - Sensitive Data Exposure

- Access the Confidential Document. What's the flag? [`edf9281222395a1c5fee9b89e32175f1ccf50c5b`]
  - When going to download [the legal doc](./juice_shop_files/legal.md) from the `About Us` page, it shows that it's coming from a `/ftp`
  - On `/ftp` there's several files. I tried to download some but it said I could only download `.md|.pdf` files, so I did
  - One was a test order PDF I made, the other was a confidential Markdown file
  - I reloaded the home page and got a key. Nifty
- Log into MC SafeSearch's account. What's the flag? [`66bdcffad9e698fd534003fbb3cc7e2b7b55d7f0`]
  - There's an old CollegeHumor video in the room about safe passwords
  - The challenge is to login using the info in the video
  - I logged in. Shocking, I know...
- Download the Backup file. What's the flag? [`bfc1e6b4a16579e85e06fee4c36ff8c02fb13795`]
  - This one was cool!
  - There's something called a `Poison Null Byte`, which is represented as `%00` (url-encoded as `%2500`)
    - Gives me `\0` vibes from C
    - What it is: A Poison Null Byte is actually a NULL terminator. By placing a NULL character in the string at a certain byte, the string will tell the server to terminate at that point, nulling the rest of the string.
  - There's a `package.json.bak` file. Using the poison null byte, I changed the url ending to `package.json.bak%2500.md` which would trick the system into thinking it's a `.md` file
  - I reloaded the page, and got a key

## Task 5 - Broken Access Control

Types of privilege escalation:

- Horizontal: when a user can perform actions of another user on the same authorization level as them
- Vertical: when a user can perform actions of another user with higher authorization levels as them

- Access the administration page. What is the flag? [`946a799363226a24822008503f5d1324536629a0`]
  - In the source code (`main-es2015.js`) there's a mention of a `path:administration`
  - Logged in as the admin and went to `http://10.10.248.221/#/administration`, it gave me the flag
- View another user's shopping basket. What is the flag? [`41b997a36cc33fbe4f0ba018474e19ae5ce52121`]
  - In Burp Suite, found `/rest/basket/1` when I went to the admin basket
  - Put it into Repeater, changed it to `rest/basket/2` (for jim) and it opened it, got the flag on reload
- Remove all 5-star reviews. What is the flag? [`50c97bcce0b895e446d61c83a21df371ac2266ef`]
  - Went back to the admin page and deleted the 5 star review

## Task 6 - XSS

- Perform a DOM XSS. What is the flag? [`9aaf4bbea5c30d00a1f5bbcfce4db6d4b0efe0bf`]
  - In the search bar, it suggested using an `<iframe>` (called XFS or Cross Frame Scripting). I did an `alert()` in it. It gave me a flag
- Perform a persistent XSS. What is the flag? [`149aa8ce13d7a4a8a931472308e269c94dc5f156`]
  - In the `Last Login IP` page, it shows the last IP you logged in as, which is given in the `rest/saveLoginIp` call on logout through a `True-Client-IP` header
  - Added another XFS load and got the flag
- Perform a reflected XSS. What is the flag? [``]
  - Went to order history, clicked on the truck icon, the order page takes the ID directly from the params and sends it to the server and back
  - Put in `<iframe src="javascript:alert(``xss``)">` (with just one backtick around xss, markdown is weird), refreshed, got a flag

## Scoreboard

- Find the scoreboard under `/#/score-board`. What is the flag? [`7efd3174f9dd5baa03a7882027f2824d2f72d86e`]

## Bonus

All the ones I decide to do on my own go here. May do some more later on.
