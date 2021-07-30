# Windows Fundamentals

Part 1 seems to be going over some basic Windows functionality, I'll add any misc. notes here:

- Windows is based off of the NTFS (New Technology File System) system vs FAT16/32 which is what is used in storage mediums and sometimes Linux. [Microsoft docs](https://docs.microsoft.com/en-us/troubleshoot/windows-client/backup-and-storage/fat-hpfs-and-ntfs-file-systems)
- Window's implementation of NTFS includes Alternate Data Streams (ADS) which allows files to have more than one data stream, which has been used for things like malware. Powershell can view ADS data as well as some other 3rd party tools. [Malwarebytes](https://blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/)
- `lusermgr.msc` is the old control panel page that allows for managing users and groups

Part 2 didn't really introduce much, just some of the system utilities.

## Intro to Windows

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
