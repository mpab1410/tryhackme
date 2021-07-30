# Encryption - Crypto 101

Michael Bailey | 7/28/21

## Key Terms

**Cipher**: A method of encrypting or decrypting data. Modern ciphers are usually cryptographic but others like Caesar are not

**Encryption**: Transforming data using a cipher

**Ciphertext**: The transformed, encrypted data (result of encryption)

**Key**: Info needed to correctly decrypt ciphertext into plaintext

**Passphrase**: Similar to a password used to protect a key

**Asymmetric Encryption**: Using two different keys to encrypt and decrypt, one key for each (i.e. RSA)

- Encryption uses a private key, decryption uses a public key or vice versa
- Slower
- Tends to use long keys (RSA -> 2048-4096 bits)
- Based on extremely hard math problems

**Symmetric Encryption**: Using the same key to encrypt and decrypt (i.e. DES and AES)

- Tends to be faster than asymmetric encryption
- Have smaller keys

**Cryptanalysis**: Attacking cryptography to find a weakness in the math used

[**Alice and Bob**](https://en.wikipedia.org/wiki/Alice_and_Bob): Term used to describe two people that want to communicate (named the way they are so that it can be A and B)

## Importance

A lot of data that's meant to be protected uses encryption to keep them safe.

Companies need to comply with laws and other policy in order to keep data safe (i.e. GDPR and [PCI-DSS](https://www.pcisecuritystandards.org/documents/PCI_DSS_for_Large_Organizations_v1.pdf), which says data should be encrypted in both transit and in storage)

## Math

Cryptography makes heavy usage out of the modulo operation, which gives back the remainder of two divided numbers (i.e. 25 % 5 = 0 -> 25 / 5 = 5R0).

## [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

RSA is one of the defacto standards in cryptography.

RSA's math is based on finding factors of really large numbers. For example, it's easy to multiply two prime numbers to get a result, but it's much harder to find the two prime greatest common multiples of said result.

Room suggested I either work the math out myself or use [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool), I aliased it to `rsatool` on my `.zshrc`

RSA has some key variables:

`p` and `q` are variables which represent large numbers. `n` is `p * q`

`e` and `d` are used alongside `n` for the public key and private key, respectfully (pubkey = `n` and `e`; privkey = `n` and `d`)

`m` represents the plaintext and `c` represents the ciphertext

[Blog with more math explanation](https://muirlandoracle.co.uk/2020/01/29/rsa-encryption/)

[Computerphile video on RSA math](https://www.youtube.com/watch?v=JD72Ry60eP4)

## Asymmetric and Symmetric Cryptography

Sometimes used in tandem (i.e. HTTPS sends an asymmetrically encrypted key using a symmetric key to keep it secure and to speed up the request process). Digital certificates can help ensure identity in the case they both are used.

[HTTPS Info](https://robertheaton.com/2014/03/27/how-does-https-actually-work/)

## Digital Signature / Certificates

Digital signatures are used to verify the authenticity of files. The signature is made using asymmetric crypto. The private key produces the signature and the public key verifies it.

One example of this is certificates for a website. The website creates a certificate from a trusted source (or self signs using Let's Encrypt) which is then passed on to the brower and verified using a root certificate authority (CA).

## SSH

SSH keygens also use RSA. `ssh-keygen` creates a public/private key pair. You put the public key in the `authorized_keys` file in the server and use `ssh -i privkey user@serverip` to login. Privkey must be chmod to 600.

## Diffie Hellman Key Exchange

Key exchanges allow two people to establish common crypto (usually symmetric) keys without some observer being able to get them.

Diffie Hellman Key Exchange goes usually like this:

Alice and Bob want to establish a common symmetric key. They both generate a secret (A and B), and they both have some kind of data to encrypt in common (C). Since combining secrets and material makes it very difficult to separate (see RSA), they both create a combo AC and BC. They send those to each other, thus then eventually forming a common key ABC.

```
DH Key Exchange is often used alongside RSA public key cryptography, to prove the identity of the person you’re talking to with digital signing. This prevents someone from attacking the connection with a man-in-the-middle attack by pretending to be Bob.
```

[Computerphile video on it](https://www.youtube.com/watch?v=NmM9HA2MQGI)

## PGP, GPG, AES

PGP - Pretty Good Privacy. Software the implements encryption for encrypting files, digital signing, etc.

GPG - GNU-PG, open source implementation of PGP. Hides passwords for keys much like SSH keys sometimes, can use `gpg2john` to crack them

Example:

```bash
gpg --import private.key
gpg --decrypt message.gpg
```

AES/Rijndael - Advanced Encryption Standard. Made as a replacement to DES, both operate on blocks of data

## Quantum

Quantum, which is gonna probably more relevant in the next decade or so, is gonna be able to crack a lot of encryptions, and work is being done to create more secure algorithms. The current recommendation from the NSA suggests RSA-3072+ or AES-256+.

```
If you’d like to learn more about this, NIST has resources that detail what the issues with current encryption is and the currently proposed solutions for these. https://doi.org/10.6028/NIST.IR.8105

I also recommend the book "Cryptography Apocalypse" By Roger A. Grimes, as this was my introduction to quantum computing and quantum safe cryptography.
```
