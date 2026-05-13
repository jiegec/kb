# Dirty Frag

官网：[V4bel/dirtyfrag](https://github.com/V4bel/dirtyfrag)

复现：`git clone https://github.com/V4bel/dirtyfrag.git && cd dirtyfrag && gcc -O0 -Wall -o exp exp.c -lutil && ./exp`

CVE: CVE-2026-43284 (xfrm) 和 CVE-2026-43500 (RxRPC)

相关：[copy fail 2: electric boogaloo](https://afflicted.sh/blog/posts/copy-fail-2.html)

发行版修复方式：

- Debian：通过内核更新修复，<https://security-tracker.debian.org/tracker/CVE-2026-43284> 和 <https://security-tracker.debian.org/tracker/CVE-2026-43500>
- Ubuntu：尚未修复，见 <https://ubuntu.com/security/CVE-2026-43284>, <https://ubuntu.com/blog/dirty-frag-linux-vulnerability-fixes-available>
