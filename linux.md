---
title: Linux Notes
created: 2017-02-13
updated: 2025-01-07
---

## Resources

- [Linux Cheat Sheet](https://sites.google.com/site/mrxpalmeiras/linux/linux-cheat-sheet)

## Change permissions of all files and subfolders

To change all the directories to 755 (`drwxr-xr-x`):

    find /opt/lampp/htdocs -type d -exec chmod 755 {} \;

To change all the files to 644 (`-rw-r--r--`):

    find /opt/lampp/htdocs -type f -exec chmod 644 {} \;

Two command in one line:

    # specify a location
    find destination_project '(' -type f -exec chmod 644 {} ';' ')' -o '(' -type d -exec chmod 755 {} ';' ')' # current directory
    find ./ '(' -type f -exec chmod 644 {} ';' ')' -o '(' -type d -exec chmod 755 {} ';' ')'

Refs:

1. [How do I change permissions for a folder and its subfolders/files?](https://stackoverflow.com/questions/3740152/how-do-i-change-permissions-for-a-folder-and-its-subfolders-files)
2. [Change all folder permissions with 1 command](https://unix.stackexchange.com/questions/349053/change-all-folder-permissions-with-1-command)

## 创建用户 adduser 和 useradd 的区别

- `adduser`: 会自动为创建的用户指定主目录，系统 shell，并在创建时提示用户输入密
  码和其他信息，同时会建立一个同名的用户组。
- `useradd`: 需要使用利用各种参数指定，如果不使用参数，则创建的用户无密码、无主
  目录、没有指定 shell 版本。

`useradd`常用选项:

    -d: 指定用户的主目录
    -m: 如果存在不再创建，但是此目录并不属于新创建用户；如果主目录不存在，则强制创建，配合-d使用
    -M: 不创建主目录
    -s: 指定用户登录时的shell版本

## 添加 sudo 权限

### 通过添加到`sudo`组来实现提权

sudo 组为专门有 sudo 权限的组别

    usermod -aG sudo username
    -a, --append:       追加用户
    -G, --groups:       追加用户到特定的组中
    -d, --home:         修改用户的家目录，通常和 -m 一起使用
    -m, --move-home:    修改用户的家目录，通常和 -d 一起使用
    -s, --shell:        修改用户的shell

另外也可以使用 `gpasswd` 对 sudo 组中添加用户或移除用户

    gpasswd -d/-a username GROUP(sudo)
    -a, --add USER:       add USER to GROUP
    -d, --delete USER:    remove USER from GROUP

### 修改 /etc/sudoers 文件实现

在 `/etc/sudoers` 文件中添加

    username ALL=(ALL:ALL) ALL
    %group ALL=(ALL:ALL) ALL

如果觉得每次`sudo`后输入密码太麻烦可以加上`NOPASSWD`

    username ALL=(ALL:ALL) NOPASSWD:ALL
    %group ALL=(ALL:ALL) NOPASSWD:ALL

## Ubuntu 18.04 禁用 DHCP，手动设置 IP 地址

Ubuntu 17.10 以后引入了 `netplan` 来替代原来的 `ifupdown`，如果再通过原来的
`ifupdown` 工具包继续在 /etc/network/interfaces 文件里配置管理网络接口是无效的。
`netplan` 允许利用 `yaml` 文件来配置网络。

手动设置 IP 需要在 `/etc/netplan` 添加 `99-static-ip.yaml`:

```yaml
network:
  version: 2
  ethernets:
    enp3s0:
      dhcp: false
      addresses:
        - 10.10.10.2/24 # using CIDR code instead of netmask
        - 2001:1::1/64
      gateway4: 10.10.10.1
      nameservers:
        search: [mydomain, otherdomain]
        addresses: [10.10.10.1, 1.1.1.1]
```

然后执行 `sudo netplan apply`

ref: https://netplan.io/examples

## linux login with ssh key

Generating an SSH key pair

    ssh-keygen -t ecdsa -b 4096 -C "$(whoami)@$(hostname)-$(date -I)"

Copying the public key to the remote server

    ssh-copy-id remote_username@server_ip_address [-i id_ecdsa]

manually:

    cat ~/.ssh/id_ecdsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"

`chmod -R go= ~/.ssh` this recursively removes all "group" and "other"
permissions for the `~/.ssh/` directory.

Permisson of `~/.ssh/authorized_keys` must be `rw-------`/`600`

Ref:

1. https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1604
2. https://wiki.archlinux.org/index.php/SSH_keys
3. https://security.stackexchange.com/questions/23383/ssh-key-type-rsa-dsa-ecdsa-are-there-easy-answers-for-which-to-choose-when

## pi-hole set custom dns record

### config pi-hole

With a little configuration, you can use your pi-hole as the DNS server for your
LAN, if, for example, your router isn’t doing a very good job serving local
names. Here’s how:

Create a second dnsmasq configuration file:

    echo "addn-hosts=/etc/pihole/lan.list" | sudo tee /etc/dnsmasq.d/02-lan.conf

create a "hosts file" for your network `/etc/pihole/lan.list` with the format
`ipaddress fqdn hostname`, eg

    192.168.1.40  marvin.your.lan  marvin
    192.168.1.41  eddie.your.lan   eddie
    192.168.1.42  hactar.your.lan  hactar

Finally, restart your name server:

    sudo pihole restartdns

PS: Adding `local=/home.lan/` or `local=/local/` or both to
`/etc/dnsmasq.d/02-pihole.conf` will prevent upstream lookups for domains ending
with those.

ref:

1. https://discourse.pi-hole.net/t/howto-using-pi-hole-as-lan-dns-server/533/8
2. https://wiki.archlinux.org/index.php/Dnsmasq

### config dnsmasq

from cli:

    pihole -a hostrecord home.mydomain.de 192.168.1.10
    # IPv6-aware
    pihole -a hostrecord home.mydomain.de 192.168.1.10,2003:89:xxxx:xxxx::xxx

create `/etc/dnsmasq.d/03-pihole-wildcard.conf`/`/etc/dnsmasq.d/03-custom.conf`

    address=/printer.lan/192.168.2.9
    address=/babycam.lan/192.168.2.10
    address=/www.yahoo.com/192.168.2.10
    address=/.subdomain.pc01.domain.com/192.168.1.2
    # or use host-record
    host-record=www.google.com,192.168.1.107
    host-record=www.yahoo.com,192.168.2.10
    # --host-record=<name>[,<name>....][<IPv4-address>],[<IPv6-address>]

Ref:

1. https://unix.stackexchange.com/questions/454039/pi-hole-redirecting-domain-to-ip
2. https://github.com/pi-hole/pi-hole/pull/1266

## make systemd-resolve and dnsmasq compatiable

edit `/etc/systemd/resolved.conf`

    [Resolve]
    DNS=127.0.0.1
    DNSStubListener=no

ref:

1. https://unix.stackexchange.com/questions/304050/how-to-avoid-conflicts-between-dnsmasq-and-systemd-resolved
2. https://github.com/hashicorp/consul/issues/4155

## Use customized dns server for specific domains

If you are using `NetworkManager` for network and `dnsmasq` for dns resolver.
Here is the solution:

1. Create or edit `/etc/NetworkManager/dnsmasq.d/custom-dns`

2. Add these lines so that `domain.intra` will be resolved by `192.168.30.1` and
   home.intra will be resolved by `192.168.0.1`. Add all of them as you wished.

   ```conf
   server=/domain.intra/192.168.30.1
   server=/home.intra/192.168.0.1
   ```

3. Check whether `dnsmasq` is eabled as dns resolver by `NetworkManager`. Set
   `main.dns=dnsmasq` with a configuration file in
   `/etc/NetworkManager/conf.d/dns.conf`

   ```conf
   [main]
   dns=dnsmasq
   ```

4. Restart `NetworkManager.service`. NetworkManager will automatically start
   dnsmasq and add `127.0.0.1` to `/etc/resolv.conf`. The original DNS servers
   can be found in /`run/NetworkManager/no-stub-resolv.conf`.

   IPv6: Enabling `dnsmasq` in NetworkManager may break IPv6-only DNS lookups
   (i.e. `drill -6 [hostname]`) which would otherwise work. In order to resolve
   this, creating the file `/etc/NetworkManager/dnsmasq.d/ipv6_listen.conf` and
   add option `listen-address=::1` will configure `dnsmasq` to also listen to
   the IPv6 loopback:

   In addition, `dnsmasq` also does not prioritize upstream IPv6 DNS.

Of course, `systemd-resolved` is also configurable.

References:

1. [use-a-different-dns-server-for-some-specific-domains](https://askubuntu.com/questions/7515/use-a-different-dns-server-for-some-specific-domains)
2. [NetworkManager#dnsmasq](https://wiki.archlinux.org/index.php/NetworkManager#dnsmasq)
3. [is-there-a-way-to-use-a-specific-dns-for-a-specific-domain](https://serverfault.com/questions/391914/is-there-a-way-to-use-a-specific-dns-for-a-specific-domain)

## The general list of blocked ports from chromium based browser

Some ports generate an error (`ERR_UNSAFE_PORT`) when browsing to them via
`Chrome`. Hence, if you're developing something, you could try to avoid using
these ports. The following ports are considered as unsafe by default.

    1,       // tcpmux
    7,       // echo
    9,       // discard
    11,      // systat
    13,      // daytime
    15,      // netstat
    17,      // qotd
    19,      // chargen
    20,      // ftp data
    21,      // ftp access
    22,      // ssh
    23,      // telnet
    25,      // smtp
    37,      // time
    42,      // name
    43,      // nicname
    53,      // domain
    77,      // priv-rjs
    79,      // finger
    87,      // ttylink
    95,      // supdup
    101,     // hostriame
    102,     // iso-tsap
    103,     // gppitnp
    104,     // acr-nema
    109,     // pop2
    110,     // pop3
    111,     // sunrpc
    113,     // auth
    115,     // sftp
    117,     // uucp-path
    119,     // nntp
    123,     // NTP
    135,     // loc-srv /epmap
    139,     // netbios
    143,     // imap2
    179,     // BGP
    389,     // ldap
    427,     // SLP (Also used by Apple Filing Protocol)
    465,     // smtp+ssl
    512,     // print / exec
    513,     // login
    514,     // shell
    515,     // printer
    526,     // tempo
    530,     // courier
    531,     // chat
    532,     // netnews
    540,     // uucp
    548,     // AFP (Apple Filing Protocol)
    556,     // remotefs
    563,     // nntp+ssl
    587,     // smtp (rfc6409)
    601,     // syslog-conn (rfc3195)
    636,     // ldap+ssl
    993,     // ldap+ssl
    995,     // pop3+ssl
    2049,    // nfs
    3659,    // apple-sasl / PasswordServer
    4045,    // lockd
    6000,    // X11
    6665,    // Alternate IRC [Apple addition]
    6666,    // Alternate IRC [Apple addition]
    6667,    // Standard IRC [Apple addition]
    6668,    // Alternate IRC [Apple addition]
    6669,    // Alternate IRC [Apple addition]
    6697,    // IRC + TLS

See similar blocking list from
[Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Mozilla_Port_Blocking).

ref:

1. [chromium src codes](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/master/net/base/port_util.cc)

## Avoid perl Warning "Setting locale failed" when run shell locally or using SSH to remote server or

If you're experiencing annoyed warning like this:

```
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
    LANGUAGE = (unset),
    LC_ALL = "en_US.UTF-8",
    ...
    LANG = "en_US.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to a fallback locale ("en_US.UTF-8").
locale: Cannot set LC_ALL to default locale: No such file or directory
Selecting previously unselected package iperf.
```

> [!NOTE]
>
> Setting `LC_*` env variables to `en_US.UTF-8` sometimes is not enough.

Three ways:

1. Generate Locales on the Server (server side)
2. Disable Locale Environment Variable Forwarding (client side)
3. Refuse Client Locale Environment Variable (server side)

### 1. Generate Locales on the Server (server side)

Try to comment out the following line in `/etc/locale.gen`:

```
C.UTF-8 UTF-8
en_US.UTF-8 UTF-8
```

Then run `locale-gen` (requires root permission) to generate the locales. Or you
can just run `locale-gen en_US.UTF-8` to generate the locale you need.

```sh
sed -i 's/# C.UTF-8/C.UTF-8/g' /etc/locale.gen
sed -i 's/# en_US.UTF-8/en_US.UTF-8/g' /etc/locale.gen
locale-gen
```

If you want set `locale` from cli, there is serveral command to do this:

```sh
# generate locales. `locale-gen` reads `/etc/locale.gen` file to know what locales to generate. Multiple locales are available.
sudo locale-gen en_US en_US.UTF-8
# debian-like: `dpkg-reconfigure` reconfigures packages after they have already been installed
sudo dpkg-reconfigure locales

 # It updates /etc/default/locale with provided values.
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
# set each locale evironment variables (systemd-based)
sudo localectl set-locale LANG=en_US.UTF-8
```

most changes may need re-login or reboot to take effect.

Ref:

1. [Perl: warning: Setting locale failed in Debian and Ubuntu](https://www.cyberciti.biz/faq/perl-warning-setting-locale-failed-in-debian-ubuntu/)
2. [How do I fix my locale issue?](https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue)

### 2. Disable Locale Environment Variable Forwarding (client side)

We can also disable SSH locale environment variable forwarding to fix this
error. Open the SSH client configuration file on your local computer.

```sh
sudo nano /etc/ssh/ssh_config
```

Find this line:

    SendEnv LANG LC_*

Add a `#` sign at the beginning to comment it out. Save and close the file.

ref:

1. [3 Ways to Fix SSH Locale Environment Variable Error](https://www.linuxbabe.com/linux-server/fix-ssh-locale-environment-variable-error)

### 3. Refuse Client Locale Environment Variable (server side)

The last one, you can just refuse client locale environment variable on server
side.

```sh
sudo nano /etc/ssh/sshd_config
```

Add the following line at the end of the file:

    AcceptEnv LANG LC_*

Save and close the file. Then restart SSH service.

```sh
sudo systemctl restart ssh
```

## Release info changed from test to stable

    N: Repository 'http://mirrors.linode.com/debian buster InRelease' changed its 'Version' value from '' to '10.0'
    E: Repository 'http://mirrors.linode.com/debian buster InRelease' changed its 'Suite' value from 'testing' to 'stable'
    N: This must be accepted explicitly before updates for this repository can be applied. See apt-secure(8) manpage for details.
    N: Repository 'http://mirrors.linode.com/debian-security buster/updates InRelease' changed its 'Version' value from '' to '10'
    E: Repository 'http://mirrors.linode.com/debian-security buster/updates InRelease' changed its 'Suite' value from 'testing' to 'stable'
    N: This must be accepted explicitly before updates for this repository can be applied. See apt-secure(8) manpage for details.

If you're upgrading from `testing` to `buster`, also be sure to run

    apt-get update --allow-releaseinfo-change

If not, `apt-get update` won't let you update with Buster and will spit out
messages like these:

    N: Repository 'http://deb.debian.org/debian buster InRelease' changed its 'Version' value from '' to '10.0'
    E: Repository 'http://deb.debian.org/debian buster InRelease' changed its 'Suite' value from 'testing' to 'stable'
    N: This must be accepted explicitly before updates for this repository can be applied. See apt-secure(8) manpage for details.
    N: Repository 'http://security.debian.org/debian-security buster/updates InRelease' changed its 'Version' value from '' to '10'
    E: Repository 'http://security.debian.org/debian-security buster/updates InRelease' changed its 'Suite' value from 'testing' to 'stable'
    N: This must be accepted explicitly before updates for this repository can be applied. See apt-secure(8) manpage for details.

ref:
https://unix.stackexchange.com/questions/528751/cannot-update-apt-list-repository-no-longer-has-a-release-file

## Debian upgrades between release channels

Like from `Debian 9 strench` to `Debian 10 buster`

```shell
sed s/jessie/stretch/g /etc/apt/sources.list | sudo tee /etc/apt/sources.list
```

很多 package 是有配置文件的。不管你是使用 apt 还是 aptitude，只要是用默认的
remove 删除，都只是删除程序文件，保留配置文件的；而使用 purge 则是一个不留的全部
删除。

### 查看 （以下 3 个等价）

```bash
aptitude search "~o"
aptitude search ~o
aptitude search ?obsolete
```

### 清除

```
sudo aptitude purge "~o"
```

configuration clean up

clean packages in `rc` state

```shell
# 查看rc状态的包
dpkg --list | grep "^rc"
# 清除
dpkg --list | grep "^rc" | cut -d " " -f 3 | xargs sudo dpkg --purge
```

Refs:

1. https://blog.csdn.net/yanxiangtianji/article/details/88075587
2. https://linuxprograms.wordpress.com/2010/05/11/status-dpkg-list/
3. https://www.debian.org/releases/stable/amd64/release-notes/ch-information.en.html
4. https://www.debian.org/releases/stable/amd64/release-notes/ch-upgrading.html

## Ubuntu UTC 时间设置

当装着 Windows 和 Ubuntu 双系统的时候。由于 Windows 和 Ubuntu 时间设置的方式不一
样，切换系统的时候会出现时间误差。

比较方便的方式是改变 Ubuntu 的 UTC 时间设置。把 UTC=yes 改变为 UTC=no 即可。

在最新的 Ubuntu 16.04 更新的情况下，网络上其他很多的改变方式并不正确，并且传统的
修改 /etc/default/rcS 的方式已经无法成功。

先查看当下的 UTC 时间设置

    timedatectl

默认是 UTC=yes 的配置下，应当会显示

```
      Local time: 四 2016-08-25 19:46:11 CST
  Universal time: 四 2016-08-25 11:46:11 UTC
        RTC time: 四 2016-08-25 11:46:11
       Time zone: Asia/Shanghai (CST, +0800)
 Network time on: yes
NTP synchronized: yes
 RTC in local TZ: no
```

所以需要进行调整

    timedatectl set-local-rtc 1 --adjust-system-clock

设置以后，再查看 timedatectl 可以发现，以及变为 UTC=no 了:

```
      Local time: 四 2016-08-25 19:46:45 CST
  Universal time: 四 2016-08-25 11:46:45 UTC
        RTC time: 四 2016-08-25 11:46:45
       Time zone: Asia/Shanghai (CST, +0800)
 Network time on: yes
NTP synchronized: no
 RTC in local TZ: yes
```

此时再切换会 Windows 下就不会再发生时间错误的情况了。

## Port forwading

There are three types of port forwarding with SSH:

- Local port forwarding: connections from the SSH client are forwarded via the
  SSH server, then to a destination server
- Remote port forwarding: connections from the SSH server are forwarded via the
  SSH client, then to a destination server
- Dynamic port forwarding: connections from various programs are forwarded via
  the SSH client, then via the SSH server, and finally to several destination
  servers

Refs:

1. https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding
2. https://www.tunnelsup.com/how-to-create-ssh-tunnels/
3. https://rufflewind.com/2014-03-02/ssh-port-forwarding

## SSH port forwarding without session

Just but not maintain a terminal session

    exit

The `-f` option is the one that actually backgrounds things, but `-N` and `-T`
will save resources which you don't need to allocate for an SSH session whose
sole purpose is to carry your tunnel.

    -f    Requests ssh to go to background just before command execution.
    -N    Do not execute a remote command.
    -T    Disable pseudo-tty allocation.

Addtional option `-o ControlPersist=yes` would be useful to prevent the
connection from being closed when combines with `ControlMaster=auto` or in some
specific system setups.

Refs:

1. https://superuser.com/questions/827934/ssh-port-forwarding-without-session/827972
2. https://unix.stackexchange.com/questions/46235/how-does-reverse-ssh-tunneling-work/46271

## How to fix VIM freezes

I noticed that I have a subconscious habit of pressing `Ctrl+S` when editing a
file. But hey `Ctrl+S` has special meaning for Linux terminal, it’s a terminal
scroll lock - basically it freezes program that wants to write to standard
output/error.

You need use `Ctrl+Q` to unfreeze terminal

This feature is called Software Flow Control (XON/XOFF flow control)

To disable this feature you need the following in either `~/.bash_profile` or
`~/.bashrc`:

    stty -ixon

To disable this altogether, stick `stty -ixon` in a startup script. To allow any
key to get things flowing again, use `stty ixany`.

ref:

1. https://unix.stackexchange.com/questions/12107/how-to-unfreeze-after-accidentally-pressing-ctrl-s-in-a-terminal
2. https://unix.stackexchange.com/questions/72086/ctrl-s-hang-terminal-emulator

References:

1. [how-to-use-defined-function-with-xargs](https://unix.stackexchange.com/questions/158564/how-to-use-defined-function-with-xargs)
2. [bash-c-with-positional-parameters](https://unix.stackexchange.com/questions/152391/bash-c-with-positional-parameters)

## Check for errors

Linux is great but it’s not perfect, that’s why it is good to check for errors
in your Manjaro system from time to time. For example, you can check for any
failed systemd processes.

Open a terminal and run this command:

    sudo systemctl --failed

If you see a screen as above, this is very good. There are no failed processes.
If there’s an erroneous process, you can search in Google for a way to fix it.

In addition, you can also check if there any errors in your log files:

    sudo journalctl -p 3 -xb

By executing this command, you will be able to see if there are other system
errors.

## HiDPI setting for different monitors

1. https://unix.stackexchange.com/questions/253727/is-it-possible-to-configure-a-scaled-desktop-in-xorg-conf-similar-to-using-xra
2. https://ricostacruz.com/til/fractional-scaling-on-xorg-linux
3. https://wiki.archlinux.org/index.php/Xrandr#Configuration
4. https://wiki.archlinux.org/index.php/Multihead_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
5. https://forum.manjaro.org/t/scaling-problems-with-dual-monitor-setup-with-different-resolutions/48515

## dns ia able to resolve a domain but failed to ssh/ping a name service

    drill

    ping: domain.local: Name or service not known

References:

1. [i-can-resolve-a-domain-ping-the-ip-but-i-cant-ping-the-domain](https://unix.stackexchange.com/questions/341093/i-can-resolve-a-domain-ping-the-ip-but-i-cant-ping-the-domain)
2. [why-is-ssh-not-resolving-this-hostname](https://serverfault.com/questions/831747/why-is-ssh-not-resolving-this-hostname/831769)

## rsync

倾斜斜杠结尾的含义是不同的

## tar

解压过深的目录, 通常由于没有好好压缩造成

    # check directory structure
    tar --list -f somefile.tar.gz
    # n is the deepth you want to skip
    tar --strip n -zxf somefile.tar.gz

如何正确打包

    # inapproxiated
    tar -zcf output-path/bundle.tar.gz /long/path/to/dir/you-wanted-to-compressed/bundle

this will make full absolute path structure in your tarball file.

Try to use option `-C, --directory DIR: change to directory DIR` to avoid

    tar -zcf output-path/bundle.tar.gz -C /long/path/to/dir/you-wanted-to-compressed bundle

    tar -zcf output-path/bundle.tar.gz -C /long/path/to/dir/you-wanted-to-compressed/bundle .

References:

1. [tar-extract-discarding-directory-structure](https://superuser.com/questions/71846/tar-extract-discarding-directory-structure)
2. [tar-a-directory-but-dont-store-full-absolute-paths-in-the-archive](https://stackoverflow.com/questions/18681595/tar-a-directory-but-dont-store-full-absolute-paths-in-the-archive)

## Permission denied while using `cat` and `echo` to redirection

Yes, when you tried to `cat` or `echo` string redirect to file directly, it
raise permission denied error.

    sudo echo "something" >   target.file

The problem is that the redirection is being processed by your original shell,
not by `sudo`. Shells are not capable of reading minds and do not know that that
particular `>>` is meant for the `sudo` and not for it.

You need to:

1. quote the redirection ( so it is passed on to sudo)
2. **and** use `sudo -s` (so that sudo uses a shell to process the quoted
   redirection.)

example:

    sudo -s 'echo "something" >> target.file'
    sudo bash -c 'foo > target.file'

Or the more elegant way is

    # add -a for append (>>)
    echo "something" | sudo tee -a target.file > /dev/null

`/dev/null` on the end because `tee` sends its output to both the named file
**and** its own standard output, and I don't need to see it on my terminal. (The
`tee` command acts like a "T" connector in a physical pipeline, which is where
it gets its name.)

Also, a here-document is available for a multiple lines content

```shell
sudo tee -a /etc/target.conf > /dev/null << 'EOF'
[archlinuxfr]
Server = http://repo.archlinux.fr/$arch

EOF
```

Notice that the behavior of `'EOF'` and `EOF` after `<<` is quite differnet.
single quotes (`'`...`'`) instead of doubles (`"`...`"`) so that everything is
literal and you didn't have to put a backslash in front of the `$` in `$arch`.

References:

1. [why-sudo-cat-gives-a-permission-denied-but-sudo-vim-works-fine](https://stackoverflow.com/questions/10134901/why-sudo-cat-gives-a-permission-denied-but-sudo-vim-works-fine)

## Unix: Use custom shell function with `xargs`

Try export function, then calling it in a subshell

    echo_func() {
        echo $1
    }

    export -f echo_func
    (ls) | xargs -L1 -I {} bash -c 'echo_func "$@"' -- {}

Don't forget the last `--` options, due to position parameters of `bash -c` are
quite different.

References:

1. [calling-shell-functions-with-xargs](https://stackoverflow.com/questions/11003418/calling-shell-functions-with-xargs)
2. [how-to-use-defined-function-with-xargs](https://unix.stackexchange.com/questions/158564/how-to-use-defined-function-with-xargs)
3. [bash-c-with-positional-parameters](https://unix.stackexchange.com/questions/152391/bash-c-with-positional-parameters)

## Pass a list / to pipe style shell

when you have a list of values need to pass into shell pipe to execute each
elements individually.

Try `xargs`, here is example:

    (cd ~; ls) | xargs -L1 echo

The `-L1` option tells xargs to use each line as a sole argument to an
invocation of the command.

And Use `-I` to set replace string with combine command.

Extra notes:
[Why you shouldn't parse the output of ls(1)](http://mywiki.wooledge.org/ParsingLs)

References:

1. [how-do-i-pipe-a-newline-separated-list-as-arguments-to-another-command](https://askubuntu.com/questions/987336/how-do-i-pipe-a-newline-separated-list-as-arguments-to-another-command)
2. [how-to-pass-command-output-as-multiple-arguments-to-another-command](https://stackoverflow.com/questions/33431842/how-to-pass-command-output-as-multiple-arguments-to-another-command)

## Swappiness

Swappiness can have a value between 0 and 100, the default value is 60. A low
value causes the kernel to avoid swapping, a higher value causes the kernel to
try to use swap space. Using a low value on sufficient memory is known to
improve responsiveness on many systems.

To temporarily set the swappiness value:

    sudo sysctl -w vm.swappiness=10

To set the swappiness value permanently, create a sysctl.d(5) configuration
file. For example:

    echo vm.swappiness=10 | sudo tee /etc/sysctl.d/99-swappiness.conf > /dev/null

Also, filesystem caches are optimiziable:

    echo vm.vfs_cache_pressure=60 | sudo tee -a /etc/sysctl.d/99-swappiness.conf > /dev/null

References:

1. [Swap#Swappiness](https://wiki.archlinux.org/index.php/Swap#Swappiness)
2. [tales-from-responsivenessland-why-linux-feels-slow-and-how-to-fix-that](https://rudd-o.com/linux-and-free-software/tales-from-responsivenessland-why-linux-feels-slow-and-how-to-fix-that)

## Terminate SSH session after lost connection

Try to using escape characters `~.` to terminate current session.

Other more, tune `ClientAliveInterval` and `ClientAliveCountMax` parameters in
`sshd_config`

References:

1. https://unix.stackexchange.com/questions/196701/terminal-hang-when-lost-connection-and-ssh-is-on/196724
2. https://askubuntu.com/questions/29942/how-can-i-break-out-of-ssh-when-it-locks

## Run multiple commands in one line

There are three different ways to combine commands in the terminal:

| symbol | commands                 | info                                             |
| ------ | ------------------------ | ------------------------------------------------ |
| `;`    | command 1 ; command 2    | Run command 1 first and then command 2           |
| `&&`   | command 1 && command 2   | Run command 2 only if command 1 ends sucessfully |
| `\|\|` | command 1 \|\| command 2 | Run command 2 only if command 1 fails            |

References:

1. https://itsfoss.com/basic-terminal-tips-ubuntu/

## Keep SSH client alive after resuming from sleep (for laptop)

```
# For macOS, add this file to /etc/ssh/ssh_config.d/
Host *
    TCPKeepAlive yes
    ServerAliveInterval 60
```

Make sure your `/etc/ssh/ssh_config` contains:

```
Include /etc/ssh/ssh_config.d/*
```

Check TCP configuration

```shell
sysctl -A | grep net.inet.tcp
```

```plain
net.inet.tcp.keepidle: 7200000
net.inet.tcp.keepintvl: 75000
net.inet.tcp.keepcnt: 8
```

## Mount CIFS

```shell
mkdir /mnt/remote-target/
mount -t cifs //192.168.0.155/nas -o username=anonymous,password=,rw,nounix,iocharset=utf8,file_mode=0644,dir_mode=0755 /mnt/freenas
```

NFS

sudo mount 192.168.0.155:/mnt/NAS /mnt/NAS

## Get private or public IP address of machine

### Private IP address

Use `hostname`:

```shell
hostname -i | awk '{ print $1 }'
hostname -i | cut -d ' ' -f 1
# 192.168.100.21
```

Use `ip`:

```shell
ip addr | grep -E '^\s*inet' | grep -m 1 global | awk '{ print $2 }' | sed 's|/.*||'

# more precise
ip addr show scope global up | grep -m 1 -E '\b(inet)\b' | awk '{ print $2 }' | sed 's|/.*||'

# For IPv6
ip addr show scope global up | grep -m 1 -E '\b(inet6)\b' | awk '{ print $2 }' | sed 's|/.*||'

# Get IP from route table
ip route get 1 | head -1 | awk '{print $7}'
```

Comments:

- `ip -4 a`: Only show TCP/IP IPv4
- `ip -6 a`: Only show TCP/IP IPv6
- `grep -m 1`: max count 1

Use `ifconfig`:

```shell
ifconfig | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{ print $2 }'
ifconfig | grep -E '\b(inet)\b' | grep -v '127.0.0.1' | head -1 | awk '{ print $2 }'
ifconfig | grep '\<inet\>' | cut -d ' ' -f 2 | grep -v '127.0.0.1' | head -1
```

### Public IP address

```shell
curl ifconfig.me
curl checkip.amazonaws.com
curl ipecho.net/plain
# IPv6 available
curl ident.me
curl icanhazip.com
```

References:

1. [How to get the primary IP address of the local machine on Linux and OS X?](https://stackoverflow.com/questions/13322485/how-to-get-the-primary-ip-address-of-the-local-machine-on-linux-and-os-x)
2. [Determine Your Private and Public IP Addresses from the Command Line](https://www.linuxtrainingacademy.com/determine-public-ip-address-command-line-curl)
3. [Linux ip Command Examples](https://www.cyberciti.biz/faq/linux-ip-command-examples-usage-syntax/)

## How to check how long a process has been running

Refs:

1. https://unix.stackexchange.com/questions/7870/how-to-check-how-long-a-process-has-been-running

## Smart tree print without `tree`

If you do not have `tree` command installed, you can get a pretty close
approximation with

```
find . | sort | sed 's@[^/]*/@  @g'
```

1. [Tweet of Tim Chase](https://twitter.com/gumnos/status/1545379459771109377)

## Using Brace Expansion in Bash Shell

### Basic syntax

Brace expansion `{..}` is one of the most underutilized but awesome shell
features in Linux.

```console
$ echo {1..10}
1 2 3 4 5 6 7 8 9 10
$ echo {7..1}
7 6 5 4 3 2 1
$ echo {3..-4}
3 2 1 0 -1 -2 -3 -4
```

Add leading zeroes

```console
$ echo {01..10}
01 02 03 04 05 06 07 08 09 10
```

The brace expansion in the form of `{x..y..z}` to generate values from `x` till
`y` while incrementing by `z`.

```console
$ echo {0..15..2}
0 2 4 6 8 10 12 14
$ echo {1..15..2}
1 3 5 7 9 11 13 15
```

Using sequence of letters

```console
$ echo {H..A..2}
H F D B
$ echo {a..f}
a b c d e f
```

### Detail examples

Create files with a particular name pattern:

```console
$ touch file_{1..10}.txt
$ ls
file_10.txt  file_2.txt  file_4.txt  file_6.txt  file_8.txt
file_1.txt   file_3.txt  file_5.txt  file_7.txt  file_9.txt
```

Use multiple braces like matrix

```console
$ touch {a,b,c}.{hpp,cpp}
$ ls
a.cpp  a.hpp  b.cpp  b.hpp  c.cpp  c.hpp
```

Create backup file with out `cp -p long_filename.txt long_filename.txt.bak`

```console
$ cp -p long_filename.txt{,.bak}
$ ls
long_filename.txt  long_filename.txt.bak
```

Using brace expansion in path

```sh
mv project/{new,old}/dir/file
# The above command is equivalent to:
mv project/new/dir/file project/old/dir/file
```

Ref:
[Using Brace Expansion in Bash Shell](https://linuxhandbook.com/brace-expansion/)

## HDD - Check supported sector sizes

Hard disk drives with a translation layer (see above) will usually report a
logical block size of 512 (for backwards compatibility) and a physical block
size of 4096 (indicating they are Advanced Format drives).

Tools which will report the sector of a drive (provided the drive will report it
correctly) includes:

```shell
# fdisk
fdisk -l /dev/sdX | grep 'Sector size'

# smartmontools
smartctl -a /dev/sdX | grep 'Sector Size'

# hdparm
hdparm -I /dev/sdX | grep 'Sector size:'
```

- [Arch Wiki: Advanced Format](https://wiki.archlinux.org/title/Advanced_Format)

## How to test and validate DNSSEC using dig command line

- https://www.cyberciti.biz/faq/unix-linux-test-and-validate-dnssec-using-dig-command-line/

## Check owned files by packages

```
dpkg -L zlib1g-dev | grep libz.a
```

## Check whether AES-NI is enabled

find out AES-NI (Advanced Encryption) Enabled on Linux System

```sh
grep -m1 -o aes /proc/cpuinfo
```

Check if AES-NI is enabled on Linux with cpuid

```
cpuid | grep -i aes | sort | uniq
```

Is Intel AES-NI instructions optimized driver loaded?

```
sort -u /proc/crypto | grep module
```

Is Intel AES-NI enabled for openssl enabled?

```
openssl engine
```

benchmark openssl performance

```sh
openssl speed aes-128-cbc
# or
openssl speed -evp aes-256-cbc
```

- [How to find out AES-NI Enabled on Linux System](https://www.cyberciti.biz/faq/how-to-find-out-aes-ni-advanced-encryption-enabled-on-linux-system/)

## 检查后台进程是否成功启动

```shell
set -e -o pipefail
sleep 1000 &
pid=$!
kill -0 ${pid} # kill -0 检查进程是否存活
```

Ref:
[shell 编程的若干实用技巧 - satanson 的文章 - 知乎](https://zhuanlan.zhihu.com/p/46100771)

## A trick to check current shell

```sh
ps -p $$
```

## (draft) SSH pattern

- https://askubuntu.com/questions/605479/what-does-h-mean-in-sshd-configuration
- https://unix.stackexchange.com/questions/61655/multiple-similar-entries-in-ssh-config
- https://en.wikibooks.org/wiki/OpenSSH/Pattern_Matching_in_OpenSSH_Configuration

## Tar on the fly

TIL, I just found you don't need to write archive file to disk then uncompress
it while you're downloading something. You can do it ON THE FLY! The keys is the
`-f -` option

```sh
curl -L https://url/xxx.tar.bz | tar -C ${TARGET_LOCATION} -xJf -
```

On the opposite, compressing may isn't that easy, but still be available to
compress a single file, The same `-f -` option works as well.

```sh
ls -sR | tar -cf - something
ls -sR | tar -c something
```

or just use `gzip`:

```sh
ls -sR | gzip > documents_tree.txt.gz
```

You can then use `gunzip documents_tree.txt` to uncompress it, or tools like
`gzcat` and `zless` to view it without having to uncompress it first.

You also could use

```sh
ls -sR | tee /dev/tty | gzip > documents_tree.txt.gz
```

Then you'll see the `ls` output in parallel with it being written to the gzip
file.

Refs:

- [How to tar/untar the output on the fly](https://superuser.com/questions/345376/how-to-tar-untar-the-output-on-the-fly)
- [TAR-ing on-the-fly](https://stackoverflow.com/questions/42910343/tar-ing-on-the-fly)

## Find Out DNS Server IP Address

1. Try to do real DNS lookup using command and check the output:

```sh
host -a www.cyberciti.biz | grep from
dig www.cyberciti.biz | grep SERVER
```

2. Check system configuration file:

```sh
cat /etc/resolv.conf
# or
grep nameserver /etc/resolv.conf
```

or using `resolvectl` to query (requires `systemd-resolved` service enabled):

```sh
resolvectl status
```

Some distros may start `systemd-resolved.service`,

- If using `NetworkManager` to manage network, try this:

  ```sh
  nmcli dev show | grep 'IP4.DNS'
  ```

- If using `systemd-networkd` to manage network, try this:

  ```sh
  networkctl status -l --no-pager | grep 'DNS'
  ```

3. Dump and view traffic on a network (recommended for advanced users only)

> You can use the tcpdump command to dump traffic on a network and view dns
> traffic. tcpdump command works on most Unix-like operating systems. tcpdump
> command analyzes network behavior, performance and applications that generate
> or receive network traffic including dns traffic. To view dns traffic only run
> tcpudmp as root user in a separate window:

```sh
tcpdump udp and src port 53
tcpdump udp and dst port 53
tcpdump -n -s 1500 -i eth0 udp port 53
```

Ref:

- [How To Find Out DNS Server IP Address Used By My Router](https://www.cyberciti.biz/faq/how-to-find-out-dns-for-router/)

## What are Exit Codes in Linux?

| Exit code | Meaning of the code                                                               |
| --------- | --------------------------------------------------------------------------------- |
| `0`       | Command executed with no errors                                                   |
| `1`       | Code for generic errors                                                           |
| `2`       | Incorrect command (or argument) usage                                             |
| `126`     | Permission denied (or) unable to execute                                          |
| `127`     | Command not found, or PATH error                                                  |
| `128+n`   | Command terminated externally by passing signals, or it encountered a fatal error |
| `130`     | Termination by Ctrl+C or SIGINT (termination code 2 or keyboard interrupt)        |
| `143`     | Termination by SIGTERM (default termination)                                      |
| `255/*`   | Exit code exceeded the range 0-255, hence wrapped up                              |

> **NOTE**
>
> The termination signals like `130` (SIGINT or `^C`) and `143` (SIGTERM) are
> prominent, which are just `128+n` signals with n standing for the termination
> code.
>
> For examples:
>
> - 130 = 128 + 2 (SIGINT)
> - 137 = 128 + 9 (SIGKILL)
> - 143 = 128 + 15 (SIGTERM)

The exit code of the previously executed command is stored in the special
variable `$?`. You can retrieve the exit status by running:

```sh
echo $?
```

Ref:

- [What are Exit Codes in Linux?](https://itsfoss.com/linux-exit-codes/)

## Pipeline content to cURL as POST data

It's common for command line utilities to use `-` to represent standard input.
cURL is one such utility.

In cURL, `-d @something` will expect to get its data from path something.

```sh
curl -X POST http://localhost:8000/inference -H 'Content-Type: application/json' -d @local.json
```

So `-d @-` tells curl to get its POST data from standard input.

```sh
echo 'your-content' | curl -X POST http://localhost:8000/inference -H 'Content-Type: text/json' -d @-
```

Ref:

1. [How to send a post request with the result of a command or a script using curl?](https://stackoverflow.com/questions/73574682/how-to-send-a-post-request-with-the-result-of-a-command-or-a-script-using-curl)

## Common environment variables while building projects

When you're building a project or executing binaries, you may need to set some
environment variables to let compiler or linker know where to find related or
third dependencies.

```
71.06 ----------------------------------------------------------------------
71.06 Libraries have been installed in:
71.06    /home/username/.local/lib
71.06
71.06 If you ever happen to want to link against installed libraries
71.06 in a given directory, LIBDIR, you must either use libtool, and
71.06 specify the full pathname of the library, or use the `-LLIBDIR'
71.06 flag during linking and do at least one of the following:
71.06    - add LIBDIR to the `LD_LIBRARY_PATH' environment variable
71.06      during execution
71.06    - add LIBDIR to the `LD_RUN_PATH' environment variable
71.06      during linking
71.06    - use the `-Wl,--rpath -Wl,LIBDIR' linker flag
71.06    - have your system administrator add LIBDIR to `/etc/ld.so.conf'
71.06
71.06 See any operating system documentation about shared libraries for
71.06 more information, such as the ld(1) and ld.so(8) manual pages.
71.06 ----------------------------------------------------------------------
```

To search executable files:

- `PATH`

To search libraries (`libxxx.so`, `libxxx.a`):

- `LD_RUN_PATH` (for **runtime** search during linking?)
  - When the `-rpath` option is used during compilation, the path specified in
    `LD_RUN_PATH` is hardcoded directly into the executable.
- `LD_PRELOAD` is an environment variable that allows you to specify libraries
  to be loaded before all others when executing a program.
- `LD_LIBRARY_PATH` (for **runtime** search after **dynamic** linking)
- `LIBRARY_PATH` (for **compile-time** search before linking)
- Specifiy manually:
  - `-L` is used to specify additional directories where the linker should
    search for libraries during the compilation process. (`-L/root/.local/lib`)
  - `-l` links with a library file without the lib prefix and the `.a` or `.so`
    extensions. For example,` -lmath` will search for `libmath.so` or
    `libmath.a` in the directories specified by `-L` and the default system
    library directories.

> [!NOTE]
>
> What is the difference between `LD_LIBRARY_PATH` and `LIBRARY_PATH`
>
> `LD_LIBRARY_PATH` and `LIBRARY_PATH` are environment variables used by the GCC
> (GNU Compiler Collection) to specify the paths to search for shared libraries
> during runtime and compile-time, respectively.
>
> `LD_LIBRARY_PATH` is used at runtime by the dynamic linker to find shared
> libraries, while `LIBRARY_PATH` is used at compile-time by the compiler to
> find libraries and their header files. When compiling code, `LIBRARY_PATH` is
> used by the linker (`ld`) to locate libraries specified with `-l` and include
> directories specified with `-L`.

To search include dir for header files (`xxx.h`, `xxx.hpp`):

- `CPATH` (for both C and C++ header files)
- `C_INCLUDE_PATH` (for C header files)
- `CPLUS_INCLUDE_PATH` (for C++ header files)
- `OBJC_INCLUDE_PATH` (for Objective-C header files)
- Specifiy manually: `
  - `-I dir`, eg: `-I.`, `-I/special/include`
  - `-include file` eg: `-include stdio.h`

Refs:

- [How can I add a default include path for GCC in Linux?](https://stackoverflow.com/questions/558803/how-can-i-add-a-default-include-path-for-gcc-in-linux)
- [GCC online documentation: Environment Variables](https://gcc.gnu.org/onlinedocs/cpp/Environment-Variables.html)
- [GCC online documentation: Invocation](https://gcc.gnu.org/onlinedocs/cpp/Invocation.html)

## Changing the Install Directory with `make install`

When we run `./configure`, we can use parameters to change the directories where
make install will install the files:

- `–prefix=<dir>`: This is usually `/usr` or `/usr/local` by default, and it is
  the prefix used in other parameters
- `–libdir=<dir>`: This is the libraries directory, and it’s usually
  `${prefix}/lib` or `${prefix}/lib64` by default
- `–bindir=<dir>`: This is the executables directory, and it’s usually
  `${prefix}/bin` by default

Sometimes, we just want to install the package in another place without changing
its internal directory structure. To do that properly, we’ll set the
`DESTDIR=<dir>` variable when running make install

```sh
DESTDIR=/tmp make install
```

Ref:

1. [Changing the Install Directory with `make install`](https://www.baeldung.com/linux/change-install-dir-make-install)

## Something broken while upgrading glibc on Arch-based Linux

Yeah. I got this error while upgrading glibc on my manjaro system.

```
...
... # too many lines
...
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_MEASUREMENT exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_MESSAGES/SYS_LC_MESSAGES exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_MONETARY exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_NAME exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_NUMERIC exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_PAPER exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_TELEPHONE exists in filesystem
glibc-locales: /usr/lib/locale/zu_ZA.utf8/LC_TIME exists in filesystem
Errors occurred, no packages were upgraded.
```

> ### 2023-10-09
>
> glibc-locales update requires manual intervention
>
> If you had the old glibc-locales package from the extra repo installed, the
> update to the new core package will need manual intervention:
>
> ```sh
> sudo pacman -Syu glibc-locales --overwrite /usr/lib/locale/\*/\*
> ```

Ref:

1. [[Stable Update] 2023-10-09 - Mesa, Grub, GlibC, Thunderbird, KDE Frameworks Renaming](https://forum.manjaro.org/t/stable-update-2023-10-09-mesa-grub-glibc-thunderbird-kde-frameworks-renaming/149302/2)

## Create a new user with encrypted password

To create a new user with password in automated way, usually useful for script.
First, of course, you need to define your username and password.

```sh
USERNAME=foo
PASSWORD=bar

useradd -m -s /bin/bash $USERNAME
```

After create your user with `bash` shell and home directory, you can use
`chpasswd` or `passwd` to set password for the user in **direct** and
**unencrypted** style.

```bash
echo "$USERNAME:$PASSWORD" | chpasswd
echo "$PASSWORD" | passwd "$USERNAME" --stdin
```

A more succinct approach is to generate a encrypted password with
`openssl passwd`, and pass it to `useradd` command simultaneously.

```bash
ENCRYPTED_PASSWORD=$(openssl passwd -1 $PASSWORD)
# Alternatives: $(echo "P4sSw0rD" | openssl passwd -1 -stdin)
useradd -m -s /bin/bash -p $ENCRYPTED_PASSWORD $USERNAME

# Interative way to read password from stdin
# ENCRYPTED_PASSWORD=$(read -sp 'Input your password:': pw ; echo $pw | openssl passwd -1 -stdin)
```

`mkpasswd` is also a command line tool to generate encrypted password, but it's
probably not pre-installed on distros unlike `openssl`.

```bash
mkpasswd -m sha-512
mkpasswd -m md5
```

And until now, I just know that hashed password has different prefix to indicate
its algorithm and salt (known as "hashed passphrase format"). This signature is
defined in `crypt` function in `glibc2`.

For example,

```
$1$nYoK618n$3uBwQXtuduPHUmSuu35Nr1
$6$H80xfvgwmRH8Eu1B$Ja43MWjRdzfWz7kPr1ltil1M./L67KacWll0a8VrPZE6B/qmY4gEtLWzr5mSz1i7fe3Os2et8NyeBEuGGE6xC0
```

`$1$` means MD5, `$6$` means SHA-512. The format is defined as

```
$<id>[$<param>=<value>(,<param>=<value>)*][$<salt>[$<hash>]]
```

where

- `id`: an identifier representing the hashing algorithm (such as `1` for MD5,
  `5` for SHA-256 etc.)
- `param` name and its `value`: hash complexity parameters, like
  rounds/iterations count
- `salt`: radix-64 encoded salt
- `hash`: radix-64 encoded result of hashing the password and salt

Another manual description from `glibc2` docs:

```
If salt is a  character  string  starting  with  the  characters
"$id$" followed by a string terminated by "$":

    $id$salt$encrypted

then instead of using the DES machine, id identifies the encryp‐
tion method used and this then determines how the  rest  of  the
password  string is interpreted.  The following values of id are
supported:

    ID  | Method
    ─────────────────────────────────────────────────────────
    1   | MD5
    2a  | Blowfish (not in mainline glibc; added in some
        | Linux distributions)
    5   | SHA-256 (since glibc 2.7)
    6   | SHA-512 (since glibc 2.7)

So  $5$salt$encrypted  is  an  SHA-256  encoded   password   and
$6$salt$encrypted is an SHA-512 encoded one.
```

Refs:

1. [How to automatically add user account AND password with a Bash script?](https://stackoverflow.com/questions/2150882/how-to-automatically-add-user-account-and-password-with-a-bash-script)
2. [How to add a user without knowing the encrypted form of the password?](https://serverfault.com/questions/367559/how-to-add-a-user-without-knowing-the-encrypted-form-of-the-password)
3. [How to create an SHA-512 hashed password for shadow?](https://serverfault.com/questions/330069/how-to-create-an-sha-512-hashed-password-for-shadow/)
4. [crypt (C)](<https://en.wikipedia.org/wiki/Crypt_(C)>)

### `set -e, -u, -o, -x pipefail` Explanation

set -euxo pipefail is short for:

```bash
set -e
set -u
set -x
set -o pipefail
```

Ref:

1. [`set -e, -u, -o, -x pipefail` Explanation](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425)
2. [Use Bash Strict Mode (Unless You Love Debugging)](http://redsymbol.net/articles/unofficial-bash-strict-mode/)

## Enable NTP services

Jesus, I just found that my server time has a drift. And what amazed me is NTP
service is not enabled by default on main cloud image even without
`systemd-timesyncd` installed?

Check your current ntp status:

```sh
timedatectl status # `status` probably is not imperative
```

Ouput

```
Local time: Thu 2023-11-16 01:47:31 UTC
           Universal time: Thu 2023-11-16 01:47:31 UTC
                 RTC time: Thu 2023-11-16 01:48:29
                Time zone: UTC (UTC, +0000)
System clock synchronized: no
              NTP service: inactive
          RTC in local TZ: no
```

or using `timedatectl show` to get well-formatted env output

```
Timezone=UTC
LocalRTC=no
CanNTP=yes
NTP=no
NTPSynchronized=no
TimeUSec=Thu 2023-11-16 01:55:10 UTC
RTCTimeUSec=Thu 2023-11-16 01:55:10 UTC
```

Besides, try also `timesync-status` and `show-timesync` to show status and
properties of `systemd-timesyncd`.

```sh
# Make sure you have `systemd-timesyncd` installed
# apt install systemd-timesyncd
timedatectl set-ntp true
```

Ref:

- [Arch Wiki: systemd-timesyncd](https://wiki.archlinux.org/title/systemd-timesyncd)

## Shell: assign output of pipe (`|`) to variable

Using stdin redirection (`<`) or `read` builtin command

```sh
echo 'hello' | message=$(</dev/stdin)
# or
echo 'hello' | read message
```

- [Bash: Assign output of pipe to a variable](https://unix.stackexchange.com/questions/338000/bash-assign-output-of-pipe-to-a-variable)

## Disable Sleep, Hibernate, Suspend on Debian Linux

```sh
# mask out related systemd targets
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
# check status
sudo systemctl status sleep.target suspend.target hibernate.target hybrid-sleep.target
```

```console
○ sleep.target
     Loaded: masked (Reason: Unit sleep.target is masked.)
     Active: inactive (dead)

○ suspend.target
     Loaded: masked (Reason: Unit suspend.target is masked.)
     Active: inactive (dead)

○ hibernate.target
     Loaded: masked (Reason: Unit hibernate.target is masked.)
     Active: inactive (dead)

○ hybrid-sleep.target
     Loaded: masked (Reason: Unit hybrid-sleep.target is masked.)
     Active: inactive (dead)
```

Ref:

- [suspend - How do I disable my system from going to sleep? - Ask Ubuntu](https://askubuntu.com/questions/47311/how-do-i-disable-my-system-from-going-to-sleep)
- [How to Disable Sleep, Hibernate, and Suspend on [Debian] Linux via Terminal · Snippets · GitLab](https://gitlab.com/-/snippets/2515869)

## User specific crontab job not running

From _man page of `crontab(1)`_:

> Scheduling cron jobs with **crontab** can be allowed or disallowed
> for different users. For this purpose, use the `cron.allow` and
> `cron.deny` files. If the `cron.allow` file exists, a user must be
> listed in it to be allowed to use **crontab**. If the `cron.allow`
> file does not exist but the `cron.deny` file does exist, then a
> user must not be listed in the `cron.deny` file in order to use
> **crontab**. If neither of these files exist, then only the super
> user is allowed to use **crontab**.

> Another way to restrict the scheduling of cron jobs beyond
> **crontab** is to use PAM authentication in `/etc/security/access.conf`
> to set up users, which are allowed or disallowed to use **crontab**
> or modify system cron jobs in the `/etc/cron.d/` directory.

> The temporary directory can be set in an environment variable.
> If it is not set by the user, the `/tmp` directory is used.

And please notice

> The files `cron.allow` and `cron.deny` cannot be used to restrict the
> execution of cron jobs; they only restrict the use of crontab.
> In particular, restricting access to crontab has no effect on an
> existing crontab of a user. Its jobs will continue to be executed
> until the crontab is removed.

> The files `cron.allow` and `cron.deny` must be readable by the user
> invoking crontab. If this is not the case, then they are treated
> as non-existent.

From _Linux Bash Shell Scripting Tutorial - /etc/cron.allow_

> ```
> # Enter the user names, one per line, who will be allowed to use crontab commands.
> # Be sure to add `root` to this list. If you do not, superuser access to crontab commands will be denied.
> root
> username1
> username2
> username3
> .
> .
> .
> ```

Refs:

- [Stackoverflow - Crontab won't run for user](https://stackoverflow.com/questions/53172222/crontab-wont-run-for-user)
  - outdated, but still useful and informative which make me understand the concept of `cron.allow` and `cron.deny`
  - [Controlling Access to crontab](https://docs.oracle.com/cd/E19455-01/805-7229/6j6q8svfu/index.html)
  - [Linux Bash Shell Scripting Tutorial - /etc/cron.allow](https://bash.cyberciti.biz/guide//etc/cron.allow)
- [crontab(1) — Linux manual page](https://man7.org/linux/man-pages/man1/crontab.1.html)

## Ignore files while compressing via `zip`

`zip` command has `-x` option to exclude files or directories while compressing.

```man
  -r   recurse into directories
  -x   exclude the following names
  -i   include only the following names

Include and Exclude:
  -i pattern pattern ...   include files that match a pattern
  -x pattern pattern ...   exclude files that match a pattern
  Patterns are paths with optional wildcards and match paths as stored in
  archive.  Exclude and include lists end at next option, @, or end of line.
    zip -x pattern pattern @ zipfile path path ...
```

But the `-x` option is a bit tricky, the following command does not work as expected:

```sh
zip -r archive.zip . -x dir/*
```

You need to use `\` to escape `*` on Unix like system to exclude files or directories you want.

```sh
zip -r archive.zip . -x dir/\*.c
# or
zip -r archive.zip . -x "dir/\*.c"
# or
zip -r archive.zip . -x 'dir/*'
# Bash wildcard expansion will interfere with supplying `*` or `.` in an argument.
```

And note that currently the trailing `/` is needed for directories.

```sh
zip -r archive.zip . -x ./\*\*/dir/
```

- [Unix zip directory but excluded specific subdirectories (and everything within them) - Super User](https://superuser.com/questions/312301/unix-zip-directory-but-excluded-specific-subdirectories-and-everything-within-t)

## Ubuntu: Find all files installed by a package

```sh
# by dpkg
# ...
# -L|--listfiles <package>...      List files 'owned' by package(s).
dpkg -L <package-name>


# or by apt-file
#
#   list|show          <pattern>        List files in packages (pattern is package)
#   search|find        <pattern>        Search files in packages (pattern is file)
apt-file list <package-name>
# do not forget to update the index after installing apt-file
# `apt-file update`
```

Refs:

- [apt-file - Debian Wiki](https://wiki.debian.org/apt-file): no description found
- [ubuntu - Finding path of static system libraries in Linux - Stack Overflow](https://stackoverflow.com/questions/26415485/finding-path-of-static-system-libraries-in-linux)
