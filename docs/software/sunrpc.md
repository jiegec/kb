# SUNRPC 使用样例

下面是一个使用 SUNRPC 实现字符串小写转大写服务的例子。

第一步：编写 RPC 接口：

```shell
$ cat test.x
program TEST_PROG {
    version TEST_VERS {
        string TEST(string) = 1;
    } = 1;
} = 0x12345678;
$ rpcgen test.x
# generates test_clnt.c/test_svc.c/test.h
```

第二步：编写服务端实现，它做的事情是把输入的字符串转大写：

```shell
$ cat server.c
#include "test.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char **test_1_svc(char **input, struct svc_req *req) {
    static char *result;
    char *str = *input;

    result = malloc(strlen(str) + 1);
    if (!result) return NULL;

    for (int i = 0; str[i]; i++)
        result[i] = toupper((unsigned char)str[i]);
    result[strlen(str)] = '\0';

    return &result;
}
$ gcc server.c test_svc.c -o test_svc -I/usr/include/tirpc -ltirpc
```

第三步：编写客户端实现，通过 RPC 调用服务端的实现：

```c
#include "test.h"
#include <stdio.h>

int main(int argc, char *argv[]) {
    CLIENT *clnt;
    char *server = "localhost";
    char *input = "hello rpc";
    char **result;

    clnt = clnt_create(server, TEST_PROG, TEST_VERS, "tcp");
    if (!clnt) {
        clnt_pcreateerror(server);
        return 1;
    }

    result = test_1(&input, clnt);
    if (!result) {
        clnt_perror(clnt, "call failed");
        return 1;
    }

    printf("Original: %s\n", input);
    printf("Result  : %s\n", *result);

    clnt_freeres(clnt, (xdrproc_t)xdr_wrapstring, (char*)result);
    clnt_destroy(clnt);
    return 0;
}
$ gcc client.c test_clnt.c -o test_clnt -I/usr/include/tirpc -ltirpc
```

最后，运行服务端和客户端，得到结果：

```shell
$ ./test_svc &
$ ./test_clnt
Original: hello rpc
Result  : HELLO RPC
$ rpcinfo
   program version netid     address                service    owner
 305419896    1    udp       0.0.0.0.197.117        -          1001
 305419896    1    tcp       0.0.0.0.211.156        -          1001
$ lsof -c test_svc
COMMAND     PID   USER   FD   TYPE    DEVICE SIZE/OFF     NODE NAME
test_svc 825692 jiegec    3u  IPv4 248857870      0t0      UDP *:50549
test_svc 825692 jiegec    4u  IPv4 248857872      0t0      TCP *:54172 (LISTEN)
```

其中 305419896 就是 0x12345678，50549 是 `197*256+117`，54172 是 `211*256+156`。

Credit: 本文由 DeepSeek 辅助编写。
