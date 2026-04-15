# Vivado 相关信息

- [下载地址](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools.html)

## 命令行安装

静默命令行安装命令：

```shell
# Vivado HL, 2020.3 or below
./xsetup --agree 3rdPartyEULA,WebTalkTerms,XilinxEULA --batch Install --edition "Vivado HL Design Edition" --location "/opt/Xilinx"
# Vivado ML, 2021.1 or above
./xsetup --agree 3rdPartyEULA,XilinxEULA --batch Install --edition "Vivado ML Standard" --product Vivado --location "/opt/Xilinx"
```

或者：`./xsetup --batch ConfigGen`，修改 install_config.txt 后再 `./xsetup --agree 3rdPartyEULA,XilinxEULA --batch Install --config install_config.txt`。这样可以删掉一些不用的模块。

可以参考 [thu-cs-lab/vivado-docker](https://github.com/thu-cs-lab/vivado-docker) 项目。

## 补丁

打补丁方法：下载官网上的 zip 文件，解压到 `/opt/Vivado/2023.2/patches/ARxxxxx` 路径。以 `AR000035293_vivado_2023_2_preliminary_rev1` 为例，最终应该得到：`/opt/Xilinx/Vivado/2023.2/patches/AR000035293_vivado_2023_2_preliminary_rev1/vivado/patch_readme/AR000035293_vivado_2023_2_preliminary_rev1.txt` 这个文件。打好了以后，启动 Vivado 可以看到版本号变成了 `2023.2_AR000035293`。

常用补丁列表：

- [000036317 - Vivado 2023.2 - Tactical Patch - Vivado Crashing on Save](https://adaptivesupport.amd.com/s/article/000036317?language=en_US)
- [Vivado 2023.1/2023.2 read_checkpoint - incremental Crash on Ubuntu 20.04 and Ubuntu 22.04](https://adaptivesupport.amd.com/s/article/Vivado-2023-1-and-2023-2-incremental-crash-ubuntu-20-04-and-22-04?language=en_US)
- [000035739 - 2022.2/2023.1- Tactical patch - schematic viewer is not displaying cell names or port names with Ubuntu 22.04](https://adaptivesupport.amd.com/s/article/000035739?language=en_US)
- [Export IP Invalid Argument / Revision Number Overflow Issue (Y2K22)](https://adaptivesupport.amd.com/s/article/76960?language=en_US)
- [2022.1 Vivado Design Suite Tactical Patch - Changes made to current project modify files in original project the current project was copied from](https://adaptivesupport.amd.com/s/article/000034002?language=en_US)
- [76616 - Vivado/Vitis installation - Install hangs on Ubuntu 20.04](https://adaptivesupport.amd.com/s/article/76616?language=en_US)

如何打补丁：[53821 - Vivado - How do I use the MYVIVADO environment variable to apply tactical patches?](https://adaptivesupport.amd.com/s/article/53821?language=en_US)
