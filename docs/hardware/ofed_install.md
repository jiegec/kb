# NVIDIA DOCA-OFED 安装

之前的 Mellanox OFED 已经合并到 NVIDIA DOCA-OFED 当中，安装方式参考 <https://developer.nvidia.com/doca-downloads>，以 Debian 13 为例，选择：

- Host-Server
- DOCA-Host
- Linux
- x86_64
- doca-all
- Debian
- 13
- deb (local)

```shell
wget https://www.mellanox.com/downloads/DOCA/DOCA_v3.3.0/host/doca-host_3.3.0-088000-26.01-debian13_amd64.deb
sudo dpkg -i doca-host_3.3.0-088000-26.01-debian13_amd64.deb
sudo apt-get update
sudo apt-get -y install doca-all
```
