# Hashing - Crypto 101

Michael Bailey | 7/26/21

## Key Definitions

**Plaintext**: data before encryption or hashing, most of the time - text, but can be other files as well
**Encoding**: a form of data representation (i.e. base64, hexadecimal, utf-8, etc.)
**Hash**: output of a hash function
**Brute force**: attacking cryptography by trying different passwords or keys until a match is found
**Cryptanalysis**: attacking cryptography by finding weaknesses in the underlying math

### Questions

- Is base64 encryption or encoding? [_encoding_]

## Hash Functions

Hash functions are functions that take some input data and returns a "digest" of the data. The output is a fixed size, and it's hard to predict the output will be for any input and vice versa. Good functions will be fast to compute and slow to reverse. A small change in input would cause a large change in the hash.

Hash functions work differently from encryption as hashes use no keys and are (hopefully) made to make it extremely difficult to move back and forth between hashes and plaintext.

Hashes are very commonly used to secure stored passwords and other data.

Hash functions commonly return encoded (i.e. base64) versions of the hash

Hash collision can happen when 2 different inputs end up giving the same output. Hash functions try hard to avoid this, though all hash functions are technically susceptible to collisions due to the pigeonhole effect, meaning there are a set number of different output values for a hash function, but you can give it any size input. Since there are more inputs than outputs, some must share. Examples of hash functions that have had collision discovered include MD5 and SHA1. Hash functions that have had collision found should not be used for storing passwords and such.

### Questions

- What is the output size in bytes of the MD5 hash function? [`16`]
  - Google gave me [the wiki article](https://en.wikipedia.org/wiki/MD5)
  - It's 128 bit. 128 bits / 8 bits in a byte = 16 bytes
- Can you avoid hash collisions? [_No_]
- If you have an 8 bit hash output, how many possible hashes are there? [`256`]
  - Looked up 8-bit hashes, found [a wiki article](https://en.wikipedia.org/wiki/Pearson_hashing#Python,_8-bit_output) about Pearson hashing

## Hashing Uses

Hashing is mainly used to verify passwords and to verify the integrity of other data. Storing secure information like passwords in plaintext can be really bad and sometimes costly.

Hashing can be useful, though other security practices need attention as well due to rainbow tables, which are tables that match passwords with their hash. If someone is able to crack the word "password", then any user with that same hash would be screwed. Salts help defend against this. Salts (random strings added to the beginning or end of a password before hashing) help make the passwords more unique and much harder to rainbow table. Salts need to be specifically different to avoid rainbow tables. Salts are less sensitive than passwords. Hashing functions like bcrypt and she512crypt handle this automatically.

### Questions

- Crack the hash "d0199f51d2728db6011945145a1b607a" using the rainbow table manually. [`basketball`]
  - There was a table on the page
- Crack the hash "5b31f93c09ad1d065c0491b764d04933" using online tools [`tryhackme`]
  - Oddly enough, crackstation did not know what this hash was
- Should you encrypt passwords? [_No_]
  - Encryptions requires keys, which are sensitive and need to be stored somewhere

## Hash Recognition

Tools like [hashID](https://pypi.org/project/hashID/) exist, though for many formats they are unreliable. Though, some hashes have a set prefix which makes them easy to identify. Being able to see the context of the hash is important. Web apps, for example, wouldn't have NTLM hashes, which are usually found for Windows users.

Unix style password hashes have a specific format: `$format$rounds$salt$hash`

Prefix/Format | Algorithm
-------|----------
`$1$` |	md5crypt, used in Cisco stuff and older Linux/Unix systems
`$2$`, `$2a$`, `$2b$`, `$2x$`, `$2y$`	| Bcrypt (Popular for web applications)
`$6$`	| sha512crypt (Default for most Linux/Unix systems)

Linux passwords are stored on /etc/shadow, which usually only root can access. Windows passwords are stored in the SAM, which can be hard to dump, but tools like mimikatz can be helpful. Hashes in Windows are split between NT hashes and LM hashes.

[Hashcat](https://hashcat.net/wiki/doku.php?id=example_hashes) has a huge list of common hashes and their formats

### Questions

- How many rounds does sha512crypt ($6$) use by default? [`5000`]
  - https://blog.michael.franzl.name/2016/09/09/hashing-passwords-sha512-stronger-than-bcrypt-rounds/
- What's the hashcat example hash (from the website) for Citrix Netscaler hashes? [`1765058016a22f1b4e076dccd1c3df4e8e5c0839ccded98ea`]
- How long is a Windows NTLM hash, in characters? [`32`]

## Password Cracking

With salts, it can be hard to use the rainbow table method. Tools like Hashcat and John the Ripper are able to help.

These programs tend to use different methods of cracking. Hashcat usually uses the GPU while John uses the CPU. GPU cracking tends to be faster than CPU cracking depending on which GPUs and CPUs you have, unless a hash takes that into account (i.e. bcrypt)

On my VM, hashcat refuses to work for some reason. It's mainly a GPU cracker, but it's able to do CPU cracking. Seems like no one online from their project is interested in helping in that regard either, so John will be my main go to.

### Questions

For these, I used `john --wordlist=.../rockyou.txt crack_#.txt`

- Crack this hash: $2a$06$7yoU3Ng8dHTXphAg913cyO6Bjs3K5lBnwq5FJyA6d01pMSrddr1ZG [`85208520`]
  - bcrypt
- Crack this hash: 9eb7ee7f551d2f0ac684981bd1f1e2fa4a37590199636753efe614d4db30e8e1 [`halloween`]
  - Had to specifically format as Raw-SHA256 in John
- Crack this hash: $6$GQXVvW4EuM$ehD6jWiMsfNorxy5SINsgdlxmAEl3.yif0/c3NqzGLa0P.S7KRDYjycw5bnYkF5ZtB8wQy8KnskuWQS3Yr1wQ0 [`spaceman`]
  - sha512crypt
- Bored of this yet? Crack this hash: b6b0d451bbf6fed658659a9e7e5598fe [`funforyou`]
  - Ended up being MD5, but no hash was found with john initially. Had to use a different tool online

## Integrity Checking

Hashing can also be used to check the integrity of files and other data, to ensure they haven't been changed. Hashing can also be used to compare things like files and images

HMAC is the method of using hashes to check the authenticity/integrity of data. Authors use a secret key, and if the hash for the data matches what you get, then you know that the file is authentically from the author.

### Questions

- What's the SHA1 sum for the amd64 Kali 2019.4 ISO? http://old.kali.org/kali-images/kali-2019.4/ [`186c5227e24ceb60deb711f1bdc34ad9f4718ff9`]
- What's the hashcat mode number for HMAC-SHA512 (key = $pass)? [`1750`]

## Cracking /etc/shadow

To crack hashes from `/etc/shadow`, you have to combine the `/etc/passwd` and `/etc/shadow` files using `unshadow`

`unshadow /etc/passwd /etc/shadow > unshadowed.txt`
