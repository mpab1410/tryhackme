# Windows Fundamentals

Part 1 seems to be going over some basic Windows functionality, I'll add any misc. notes here:

- Windows is based off of the NTFS (New Technology File System) system vs FAT16/32 which is what is used in storage mediums and sometimes Linux. [Microsoft docs](https://docs.microsoft.com/en-us/troubleshoot/windows-client/backup-and-storage/fat-hpfs-and-ntfs-file-systems)
- Window's implementation of NTFS includes Alternate Data Streams (ADS) which allows files to have more than one data stream, which has been used for things like malware. Powershell can view ADS data as well as some other 3rd party tools. [Malwarebytes](https://blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/)
- `lusermgr.msc` is the old control panel page that allows for managing users and groups

Part 2 didn't really introduce much, just some of the system utilities.

## Intro to Windows

### Powershell/CMD Utils

`cd: HKLM:\\ && reg` - Move into the registries store and use `reg` to manage and query registry keys. Essentially, what RegEdit uses.

`icacls` - Powershell/cmd tool used to get file/folder permissions. Gives certain letters:

- `I` - permission inherited from the parent container
- `F` - full access (full control)
- `M` - Modify right/access
- `OI` - object inherit
- `IO` - inherit only
- `CI` - container inherit
- `RX` - read and execute
- `AD` - append data (add subdirectories)
- `WD` - write data and add files

![icacls basic run in powershell](https://i.imgur.com/g0b0Pa8.png)

You can also set file/folder ownership using it

![icacls setting owner to Users](https://i.imgur.com/mFlrbGE.png)

### Active Directory - Auth

Local auth in Windows is done with Local Security Authority (LSA), which is a protected subsystem that keeps track of security policies and accounts on a computer system. It also maintains local security info.

Two varieties of Active Directory, each with different authentication types:

On Prem (self-hosted) - has a record of all PCs, users, servers, etc. on a network, logs them into network. AD then checks user's role (authorization)

- NTLM(2) - uses a challenge-response sequence of messages between a client and server system. Does not provide data integrity or protection for the authenitcated network connection

![ntlm chart](https://i.imgur.com/z7VT6PM.png)

- LDAP(S) - uses an API in order to obtain auth information. LDAPS uses encryption, while LDAP does not

![ldap chart](https://i.imgur.com/Vep5s0C.png)

- Kerberos - uses symmetric-key cryptography and requires trusted third-party authorization to verify user identities

![kerebos chart](https://i.imgur.com/nnsV5NM.png)

Azure AD (cloud/online) - AD identities stored on the cloud, used for things like Office 365 and Azure access

- Security Assertion Markup Language (SAML) - type of Single Sign-On (SSO); set of rules/standards which allows apps (Service Providers) to trust user identites (Identity Providers)
- OAuth2 - standard that apps user for client app authenitcation, with roles for an auth server (issues an access token), resource owner (app end user granting permission to access a resource server with an access token), client (app that requests an access token), and a resource server (takes in and validates auth token, essentially the app called)
- OpenID Connect - auth standard built on top of OAuth2, adds an additional token called an ID token (JSON Web Token [JWT]). Used specifically for user authenticaton versus OAuth2 which is supposed to be used for resource sharing and access.

### Types of Windows Servers

Domain Controller: controls users and groups of AD on-prem and cloud. Restricts actions and improves security of other servers in the network

File Server: Used for file sharing

Web Server: Used to hosting static/dynamic web content, usually using IIS

FTP Server: Used to help move files between computers securely using the FTP protocol

Mail Server: Help serve mail for a network, usually through Microsoft Exchange

Database Server: Hosts databases used within a network, can be others but most likely will be SQL Server

Proxy Server: Used to filter requests, improve performance, share connections, etc. 

App Server: Used to host apps of any other variety

