# Windows Fundamentals

Part 1 seems to be going over some basic Windows functionality, I'll add any misc. notes here:

- Windows is based off of the NTFS (New Technology File System) system vs FAT16/32 which is what is used in storage mediums and sometimes Linux. [Microsoft docs](https://docs.microsoft.com/en-us/troubleshoot/windows-client/backup-and-storage/fat-hpfs-and-ntfs-file-systems)
- Window's implementation of NTFS includes Alternate Data Streams (ADS) which allows files to have more than one data stream, which has been used for things like malware. Powershell can view ADS data as well as some other 3rd party tools. [Malwarebytes](https://blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/)
- `lusermgr.msc` is the old control panel page that allows for managing users and groups