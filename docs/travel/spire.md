# 尖塔

## 杀戮尖塔 2

### 亡灵契约师

#### 灵魂流

普通

- 守墓人（Grave Warden）：获得 8 点格挡。将一张灵魂放入你的抽牌堆中。
- 违逆（Defy）：虚无。获得 6 点格挡。给予 1 层虚弱。
- 唤起（Invoke）：在下个回合召唤 2 并获得 2 能量。

罕见：

- 纠缠（Haunt）：每当你打出一张灵魂时，随机一名敌人失去 6 生命。
- 捕捉灵魂（Capture Spirit）：敌人失去 3 生命。将 3 张灵魂加入你的抽牌堆。
- 挽歌（Dirge）：召唤 3X 次。将 X 张灵魂添加到你的抽牌堆中。

稀有：

- 吊杀（Hang）：造成 10 点伤害。让所有“吊杀”牌对这名敌人造成的伤害翻倍。

### 创建 Mod

参考 [STS2 Early Access Mod Guide](https://www.reddit.com/r/slaythespire/comments/1rm5gvg/sts2_early_access_mod_guide/):

1. 安装 [Godot 4.5.1 .NET 版](https://godotengine.org/download/archive/4.5.1-stable/)，如 `Godot_v4.5.1-stable_mono_macos.unitervsal.zip`
2. 安装 [.NET SDK](https://dotnet.microsoft.com/zh-cn/download)，如 `dotnet-sdk-10.0.200-osx-arm64.pkg`
3. 打开 Godot，创建项目，项目名如 `FirstMod`
4. 在 Script 选项卡，创建 Script，文件名如 `NewScript.cs`，语言选择 .NET，填写以下内容：

    ```csharp
    using Godot;
    using MegaCrit.Sts2.Core.Modding;
    using MegaCrit.Sts2.Core.Logging;

    namespace FirstMod;

    [ModInitializer("ModLoaded")]
    public static class FirstMod {
        public static void ModLoaded() {
            Log.Warn("MOD FINISHED LOADING");
        }
    }
    ```

5. 复制游戏的 sts2.dll（如 `~/Library/Application\ Support/steam/steamapps/common/Slay\ the\ Spire\ 2/SlayTheSpire2.app/Contents/Resources/data_sts2_macos_arm64/sts2.dll`）到项目根目录下
6. 修改 `FirstMod.csproj` 为以下内容，修改 .NET 版本为 9.0，引入 sts2.dll，然后点击 Build Project：

    ```xml
    <Project Sdk="Godot.NET.Sdk/4.5.1">
    <PropertyGroup>
        <TargetFramework>net9.0</TargetFramework>
        <EnableDynamicLoading>true</EnableDynamicLoading>
    </PropertyGroup>
    <ItemGroup>
        <Reference Include="sts2">
            <HintPath>sts2.dll</HintPath>
        </Reference>
    </ItemGroup>
    </Project>
    ```

7. 在项目根目录创建 `mod_manifest.json`：

    ```json
    {
        "pck_name": "FirstMod",
        "name": "FirstMod",
        "author": "doctornoodlearms",
        "description": "",
        "version": "1.0.0"
    } 
    ```

8. 在项目根目录下 `FirstMod` 目录下准备一张图片，名为 `mod_image.png`，用于 Mod 的图片
9. 点击 Project -> Export...，点击 Add...，选择 Windows Desktop
10. 在 Export Path 下面的 Resources，选择 Export selected resources (and dependencies)，下面勾选 `mod_image.png` 和 `mod_manifest.json`，点击下面的 Export PCK/ZIP，保存为 `FirstMod.pck`，之后也可以用命令行来导出，如 `/Applications/Godot_mono.app/Contents/MacOS/Godot --export-pack "Windows Desktop" FirstMod.pck --headless`
11. 复制 `./.godot/mono/temp/bin/Debug/FirstMod.dll` 和 `FirstMod.pck` 到游戏的 `mods` 目录下的 `FirstMod` 目录，如 `~/Library/Application\ Support/SlayTheSpire2/mods/FirstMod`（macOS）或 `~/.steam/steam/steamapps/common/Slay\ the\ Spire\ 2/mods/FirstMod`（Linux），不存在需要创建
12. 启动游戏

命令行构建脚本，生成 dll 和 pck 到 FirstMod 目录下：

```shell
#!/bin/sh
set -x
cp ~/Library/Application\ Support/steam/steamapps/common/Slay\ the\ Spire\ 2/SlayTheSpire2.app/Contents/Resources/data_sts2_macos_arm64/sts2.dll .
/Applications/Godot_mono.app/Contents/MacOS/Godot --build-solutions --quit --headless
mkdir -p FirstMod
cp ./.godot/mono/temp/bin/Debug/FirstMod.dll FirstMod/
/Applications/Godot_mono.app/Contents/MacOS/Godot --export-pack "Windows Desktop" FirstMod/FirstMod.pck --headless
```

启动 Godot 的 Debug Server：

1. 在 Godot 中，选择 Debug -> Keep Debug Server Open
2. 在 Steam 中，设置启动选项 `--remote-debug tcp://127.0.0.1:6007`
3. 启动游戏

目前的情况：

1. 在 macOS ARM 上可以正常构建 dll 和 pck，但是无法在 macOS 上的游戏中加载
2. Linux 上的游戏可以加载在 macOS 上构建的 dll 和 pck

存档路径：

1. 不打 mod 时：`~/Library/Application\ Support/SlayTheSpire2/steam/*`（macOS）或 `~/.local/share/SlayTheSpire2/steam/76561198118473939/*`（Linux）
2. 打 mod 时：`~/Library/Application\ Support/SlayTheSpire2/steam/*/modded`（macOS）或 `~/.local/share/SlayTheSpire2/steam/76561198118473939/*/modded`（Linux）
