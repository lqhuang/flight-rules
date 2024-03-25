---
title: CLI on Windows
created: 2018-11-03
updated: 2024-02-16
---

## Create a proxy to redirect network trafic origined to target host

Redirect all traffic

```powershell
netsh interface portproxy add v4tov4 listenport=4000 listenaddress=127.0.0.1 connectport=4000 connectaddress=172.31.217.98
```

Remove

```powershell
netsh interface portproxy del v4tov4 listenport=4000 listenaddress=127.0.0.1
```

List existing mappings

```powershell
netsh interface portproxy show v4tov4
netstat -ano | find 4000
```

- [Can I redirect/route IP adress to another IP address (windows)](https://serverfault.com/questions/712970/can-i-redirect-route-ip-adress-to-another-ip-address-windows)

## UTC Timestamp issue when dual booting Windows and Linux

While Debian prefer to keep the hardware clock in UTC (this prevents the need to
change it on daylight savings and timezone changes) other systems (like Windows)
by default keeps the hardware clock synchronized to local time.

To fix this issue, you can either update `timedatectl` to use local time (not
recommended already) or update Windows to use UTC time instead of local time.

Save the following content to a file with `.reg` extension

```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation]
"RealTimeIsUniversal"=dword:00000001
```

and double click it to import the registry settings. Reboot Windows to take the
change effect.

Refs:

1. [Debian Wiki: Hardware clock and system time when dual booting](https://wiki.debian.org/DateTime#Hardware_clock_and_system_time_when_dual_booting)
2. [Does Windows 7 support UTC as BIOS time?](https://superuser.com/questions/185773/does-windows-7-support-utc-as-bios-time)

## Print ip route table

```powershell
route print
```

## Windows 10 / Windows 11: Outdated audio driver make the system unstable and cause BSOD

> If you’re having issues with BSODs and other errors/maybe even really bad
> frame rate. It’s probably your Realtek audio driver I’ve had this issue on
> multiple PCs and it’s always been the Realtek audio. To fix it you could try
> reinstalling the driver but I’ve had no luck with that. What’s worked for me
> is using one of five drivers.
>
> 1. Old driver from Realtek site probably not recommended as it’s the old
>    control panel also and not even made for windows 11 but still works.
> 2. Generic high definition audio driver may not have all the features though
> 3. Realtek-UAD-generic driver on GitHub it should equivalent to your default
>    driver just much newer.
> 4. AAF Optimus driver has a lot more features then the stock driver and could
>    enhance your audio quality
> 5. Just disable Realtek audio if you have no use for it

I had the very similar issue and I simply disable my onboard audio device in
BIOS, then things work fine now.

Refs:

- [PSA: If you’re having issues after the 23H2 update please read](https://www.reddit.com/r/windows/comments/17p9toh/psa_if_youre_having_issues_after_the_23h2_update/)

## Check version of Windows, PowerShell, .NET, etc.

```powershell
# Windows version
winver.exe  # warning: this is a GUI application
Get-ComputerInfo | Select-Object OsName, OSDisplayVersion, WindowsVersion, WindowsBuildLabEx

# PowerShell version
$PSVersionTable
$PSVersionTable.PSVersion

# output shows `True` when you're a member of the built-in Administrators group.
(New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# .NET version
Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -Recurse | Get-ItemProperty -Name Version -EA 0 | Where-Object { $_.PSChildName -match '^(?!S)\p{L}'} | Select-Object PSChildName, Version
```

- [Get started with OpenSSH for Windows - Prerequisites check](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse#prerequisites-check)

## Install latest version of PowerShell (currently 7)

```powershell
winget search Microsoft.PowerShell
winget install --id Microsoft.PowerShell --source winget
```

Install locations by version:

- Windows PowerShell 5.1: `$env:WINDIR\System32\WindowsPowerShell\v1.0`
- PowerShell 6.x: `$env:ProgramFiles\PowerShell\6`
- PowerShell 7: `$env:ProgramFiles\PowerShell\7`

- [Installing PowerShell on Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?)
- [Migrating from Windows PowerShell 5.1 to PowerShell 7](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7)

## Install and enable OpenSSH server

Make sure to run the following commands in an elevated PowerShell prompt.

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
Add-WindowsCapability -Online -Name OpenSSH.Client  # optional
Add-WindowsCapability -Online -Name OpenSSH.Server
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
# By default the ssh-agent service is disabled. Configure it to start automatically.
# Make sure you're running as an Administrator.
Get-Service ssh-agent | Set-Service -StartupType Automatic

# Confirm the Firewall rule is configured. It should be created automatically by setup. Run the following to verify
if (!(Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue | Select-Object Name, Enabled)) {
    Write-Output "Firewall Rule 'OpenSSH-Server-In-TCP' does not exist, creating it..."
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
} else {
    Write-Output "Firewall rule 'OpenSSH-Server-In-TCP' has been created and exists."
}
```

Refs:

- [Get started with OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)
- [OpenSSH Server configuration for Windows Server and Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_server_configuration)
- [Install the SSH service on a Windows computer](https://learn.microsoft.com/en-us/powershell/scripting/learn/remoting/ssh-remoting-in-powershell?view=powershell-7.4#install-the-ssh-service-on-a-windows-computer)

## Windows change default shell to powershell

On the server side, configure the default ssh shell in the windows registry.

- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShell` - full path of the
  shell executable.
- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShellCommandOption`
  (optional) - switch that the configured default shell requires to execute a
  command, immediately exit and return to the calling process. By default this
  is `-c`. Powershell cmdlets to set powershell bash as default shell
- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShellEscapeArguments`
  (optional) - flag that allow you to skip escaping the arguments of default
  shell. By default this is `0`. This option is only applicable to shells other
  than `powershell`, `bash`, `cygwin`, `cmd`, and `ssh-shellhost.exe`.

```powershell
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShellCommandOption -Value "/c" -PropertyType String -Force

Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "$Env:ProgramFiles\PowerShell\7\pwsh.exe" -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShellCommandOption -Value "/c" -Force
```

Refs:

1. [Win32-OpenSSH Wiki: DefaultShell](https://github.com/PowerShell/Win32-OpenSSH/wiki/DefaultShell)

## SSH key-based authentication for Windows

Set up the `.ssh` directory and `authorized_keys` file

```powershell
$ssh_dir="$env:USERPROFILE\.ssh"
mkdir $ssh_dir
cd $ssh_dir
New-Item authorized_keys
```

```powershell
$sshd_config="$Env:ProgramData\ssh\sshd_config"
Restart-Service sshd
Restart-Service ssh-agent
```

- [Key-based authentication in OpenSSH for Windows - Administrative user](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement#administrative-user)
- [Installing SFTP/SSH Server on Windows using OpenSSH](https://winscp.net/eng/docs/guide_windows_openssh_server#key_authentication)

## OpenSSH utility scripts to fix file permissions

OpenSSH is already available in Windows 10 1803 and later. However, it may cause
some issues when using pubkey to connect from other hosts. The following scripts
can be used to fix the file permissions.

Check access permissions on `authorized_keys` (only System, Administrators and
owner can have access).

```powershell
icacls $Env:USERPROFILE\.ssh\authorized_keys
(Get-Acl $Env:USERPROFILE\.ssh\authorized_keys).Owner
(Get-Acl $Env:USERPROFILE\.ssh\authorized_keys).Access
```

Remove all permissions on file except for the `SYSTEM` and yourself. There must
be exactly two permission entries on the file.

```powershell
icacls $Env:USERPROFILE\.ssh /reset /T
icacls $Env:USERPROFILE\.ssh\authorized_keys /inheritance:r

$administratorsRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Administrators", "FullControl", "Allow")
$systemRule = New-Object System.Security.AccessControl.FileSystemAccessRule("SYSTEM", "FullControl", "Allow")
$userRule = New-Object System.Security.AccessControl.FileSystemAccessRule("$env:USERDOMAIN\$env:USERNAME", "FullControl", "Allow")

$acl_ssh_dir = Get-Acl $Env:USERPROFILE\.ssh
$acl_ssh_auth_keys = Get-Acl $Env:USERPROFILE\.ssh\authorized_keys
# $Env:ProgramData\ssh\administrators_authorized_keys
$acl_ssh_dir.SetAccessRule($userRule)
$acl_ssh_dir.SetAccessRule($systemRule)

$acl_ssh_dir | Set-Acl
# You could do the following to replicate these permissions onto other files
```

After Windows build 1809 or later, it is required to comment out the special
administartors' `AuthorizedKeysFile` in `sshd_config` file, while usually you're
also in administartors group.

```powershell
$sshd_config="$Env:ProgramData\ssh\sshd_config"
Get-Content $sshd_config | Foreach-Object {
  $_ -replace 'Match Group administrators', '# Match Group administrators' `
     -replace 'AuthorizedKeysFile __PROGRAMDATA__/ssh', '# AuthorizedKeysFile __PROGRAMDATA__/ssh'
} | Set-Content $sshd_config
# Out-File -encoding ASCII $sshd_config

Restart-Service sshd
Restart-Service ssh-agent
```

> The `\`` at the end of each line escapes the newline, causing PowerShell to
> continue parsing the expression on the next line

Check the references for more details.

Refs:

1. [Setting up OpenSSH for Windows using public key authentication](https://stackoverflow.com/questions/16212816/setting-up-openssh-for-windows-using-public-key-authentication/)
2. [Security protection of various files in Win32 OpenSSH](https://github.com/PowerShell/Win32-OpenSSH/wiki/Security-protection-of-various-files-in-Win32-OpenSSH)
   - (Outdated)
     [OpenSSH utility scripts to fix file permissions](https://github.com/PowerShell/Win32-OpenSSH/wiki/OpenSSH-utility-scripts-to-fix-file-permissions)
3. [ssh.exe examples: Setup server-side (`sshd`)](https://github.com/PowerShell/Win32-OpenSSH/wiki/ssh.exe-examples#setup-server-side-sshd)
4. [OpenSSHUtils 1.0.0.1](https://www.powershellgallery.com/packages/OpenSSHUtils/1.0.0.1)
5. [How to replace multiple strings in a file using PowerShell](https://stackoverflow.com/questions/3403217/how-to-replace-multiple-strings-in-a-file-using-powershell)
6. [Replace String in PowerShell: A Comprehensive Guide](https://www.sharepointdiary.com/2021/04/string-replacement-in-powershell.html)

## Elevate SSH session to Administrator

Before you can use `sudo` in Windows, you cannot elevate your session to admin
permission. You only have the permission of the user you logged in as. However,

> @bagajjal:
>
> For admin users, ssh connection is an elevated session. Given you are an admin
> and has elevated session, you can write to c:\windows.
>
> This is by design.

Refs:

1.  [Window's ssh service defaults to admin permission](https://stackoverflow.com/questions/70902288/windows-ssh-service-defaults-to-admin-permission)
2.  [ SSH login has full admin rights and there's no way to not grand them #1652 ](https://github.com/PowerShell/Win32-OpenSSH/issues/1652)

## WSL2 over SSH failed to start on Windows 11

Happens only when executing `wsl` command over SSH. The error message is:

```plaintext
c:\....> wsl --version
The file cannot be accessed by the system.
```

> Release Notes for Windows Subsystem for Linux in the Microsoft Store Launching
>
> Windows Subsystem for Linux from session zero does not currently work (for
> example from an ssh connection).

Try to update WSL2 to the latest version by running the following command in

```shell
wsl --update --pre-release
```

It probably will be fixed in future.

- [Cannot run WSL2 over SSH on Windows 11](https://superuser.com/questions/1714736/cannot-run-wsl2-over-ssh-on-windows-11)
- [Release Notes for Windows Subsystem for Linux in the Microsoft Store - Known Issues](https://learn.microsoft.com/en-us/windows/wsl/store-release-notes#known-issues)

## Cheatsheet from Unix Shell to PowerShell

| Shell                | PowerShell                                                   | More usages                                         |
| -------------------- | ------------------------------------------------------------ | --------------------------------------------------- |
| `where`              | `(Get-Command cmd.exe).Source`                               | `Get-Command cmd.exe \| Select-Object *`            |
| `less`               | `Get-Content file-with-long-content.txt \| Out-Host -Paging` | with alias `gc file-with-long-content.txt \| oh -P` |
| `echo "..." >> file` | `Add-Content -Path file -Value "..."`                        |                                                     |

## Snippets for PowerShell

List `PATH` line by line

```powershell
$Env:Path -split ';'
```

List all environment variables

```powershell
Get-ChildItem Env:
Get-ChildItem env:
```

## Sysinternals Live

- [Tool: TCPView](https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview)
