# BIND9 Cookbook

## 配置文件路径

配置文件入口是 `/etc/bind/named.conf`，根据 include 可以把内容分布到多个文件当中。

## 配置 Zone

添加 Zone 配置：

```text
zone "example.com" {
    type master;
    file "db.example.com";
};
```

`/var/cache/bind/db.example.com` 保存了 Zone 的 DNS 记录。

## 配置 DDNS

运行：`tsig-keygen -a HMAC-SHA256 key-name` 生成 secret，配置：

```text
key "key-name" {
    algorithm hmac-sha256;
    secret "REDACTED";
};
zone "example.com" {
    allow-update {
        key "key-name";
    };
};
```

## 配置 Master(Primary)/Slave(Secondary)

Master(Primary) 侧配置：

```text
zone "example.com" {
    type master;
    file "db.example.com";
    also-notify {
        1.2.3.4;
    };
    allow-transfer {
        5.6.7.8;
    };
};
```

默认情况下，修改 Zone 内容时，如果有其他 NS，它会自动 NOTIFY；也可以通过 `also-notify` 手动指定被通知的 DNS Slave 地址。通过 `allow-transfer` 允许 Slave 同步完整的 Zone 内容。

Slave(Secondary) 侧：

```text
zone "example.com" {
    type slave;
    file "db.example.com";
    masters {
        1.2.3.4;
    };
    allow-notify {
        5.6.7.8;
    };
};
```

通过 `masters` 指定 Master DNS 服务器地址，表示从哪里同步；`allow-notify` 可以指定额外的 DNS 地址，允许它们 NOTIFY 本 Slave。
