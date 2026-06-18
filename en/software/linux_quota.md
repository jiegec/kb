# Linux Quota

## CPU

限制用户的 CPU 用量：

```shell
# allow user with id 1001 to use 18 cores
sudo systemctl set-property user-1001.slice CPUQuota=1800%
# drop limit
sudo systemctl set-property user-1001.slice CPUQuota=
# the configuration is saved under
# /etc/systemd/system.control/user-1001.slice.d/50-CPUQuota.conf
```

## 内存

限制用户的内存用量：

```shell
# allow user with id 1001 to use 18 cores
sudo systemctl set-property user-1001.slice MemoryMax=20G
# drop limit
sudo systemctl set-property user-1001.slice MemoryMax=
# the configuration is saved under
# /etc/systemd/system.control/user-1001.slice.d/50-MemoryMax.conf
```
