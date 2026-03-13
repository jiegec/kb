# 尖塔

## 杀戮尖塔 2

### 铁甲战士

#### 易伤流

打法：给敌人挂易伤，通过熔融之拳让层数翻倍，再用主宰把易伤转化为力量。

普通：

- 痛击（Bash）：造成 8 点伤害。给予 2 层易伤。
- 闪电霹雳（Thunderclap）：对所有敌人造成4点伤害，给予1层易伤。
- 熔融之拳（Molten Fist）：造成 10 点伤害。将该敌人身上的易伤层数翻倍。消耗。
- 耸肩无视（Shrug It Off）：获得 8 点格挡。抽 1 张牌。

罕见：

- 拆卸（Dismantle）：造成 8 点伤害。如果该敌人有易伤效果，则攻击两次。
- 无情猛攻（Unrelenting）：造成 12 点伤害。你打出的下一张攻击牌耗能变成零能量。
- 主宰（Dominate）：敌人身上每有一层易伤，就获得 1 点能量。消耗。

稀有：

- 狂宴（Feed）：造成 10 点伤害。斩杀时，永久获得 3 点最大生命值。消耗。
- 残酷（Cruelty）：有易伤状态的敌人额外受到 25% 的伤害。
- 绯红披风（Crimson Mantle）：在你的回合开始时，失去 1 点生命并获得 8 点格挡。
- 巨像（Colossus）：获得 5 点格挡。在本回合中，有易伤状态的敌人对你造成的伤害降低 50%。

### 亡灵契约师

#### 灵魂流

打法：获取大量灵魂用于过牌，用捕捉灵魂和吊杀进行输出，用守墓人和挽歌保证生存，用唤起获得大量能量

普通：

- 守墓人（Grave Warden）：获得 8 点格挡。将一张灵魂放入你的抽牌堆中。
- 违逆（Defy）：虚无。获得 6 点格挡。给予 1 层虚弱。
- 唤起（Invoke）：在下个回合召唤 2 并获得 2 能量。

罕见：

- 纠缠（Haunt）：每当你打出一张灵魂时，随机一名敌人失去 6 生命。
- 捕捉灵魂（Capture Spirit）：敌人失去 3 生命。将 3 张灵魂加入你的抽牌堆。
- 挽歌（Dirge）：召唤 3X 次。将 X 张灵魂添加到你的抽牌堆中。

稀有：

- 吊杀（Hang）：造成 10 点伤害。让所有“吊杀”牌对这名敌人造成的伤害翻倍。

无限：

- 捕捉灵魂+疯狂科学：
    - 前置条件：卡组有一张捕捉灵魂，此外在打造时间事件中，获得疯狂科学，进行充能改造，且卡组足够小。
    - 卡牌说明：
        - 捕捉灵魂（Capture Spirit，耗费 1 能量）：敌人失去 3 生命。将 3 张灵魂加入你的抽牌堆。
        - 疯狂科学（Mad Science，耗费 1 能量）：获得 8 点格挡。获得 2 能量。
    - 无限流程：把其他无关牌都留在手上，先打捕捉灵魂消耗 1 能量，一直抽灵魂，直到把疯狂科学和捕捉灵魂抽上来，再打疯狂科学消耗 1 能量再恢复 2 能量，循环。
    - 其中捕捉灵魂可以换成其他打伤害同时可以获得灵魂的牌，如剥夺（耗费 1 能量，造成 9 点伤害。将一张灵魂加入你的抽牌堆）；如果有纠缠（每当你打出一张灵魂时，随机一名敌人失去 6 生命），其他耗费 1 能量生成灵魂的牌也都可以。

### 创建 Mod

针对 v0.98.3 版本，参考 [STS2 Early Access Mod Guide](https://www.reddit.com/r/slaythespire/comments/1rm5gvg/sts2_early_access_mod_guide/):

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
11. 复制 `./.godot/mono/temp/bin/Debug/FirstMod.dll` 和 `FirstMod.pck` 到游戏的 `mods` 目录下的 `FirstMod` 目录，如 `/Library/Application\ Support/Steam/steamapps/common/Slay\ the\ Spire\ 2/SlayTheSpire2.app/Contents/MacOS/mods/FirstMod`（macOS）或 `~/.steam/steam/steamapps/common/Slay\ the\ Spire\ 2/mods/FirstMod`（Linux），不存在需要创建
12. 启动游戏

最终项目见 [jiegec/STS2FirstMod](https://github.com/jiegec/STS2FirstMod)。

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

针对 Beta v0.99 版本（修复了 macOS 上加载 Mod 的 bug），改动如下：

1. 修改 `mod_manifest.json` 格式：

    ```json
    {
        "id": "FirstMod",
        "name": "FirstMod",
        "author": "doctornoodlearms",
        "description": "",
        "version": "1.0.0",
        "has_pck": true,
        "has_dll": true,
        "dependencies": [],
        "affects_gameplay": true
    }
    ```

2. `mod_manifest.json` 也要安装到 `mods` 目录下，不再放到 pck 内部

### 存档路径

1. 不打 mod 时：`~/Library/Application\ Support/SlayTheSpire2/steam/*`（macOS）或 `~/.local/share/SlayTheSpire2/steam/76561198118473939/*`（Linux）
2. 打 mod 时：`~/Library/Application\ Support/SlayTheSpire2/steam/*/modded`（macOS）或 `~/.local/share/SlayTheSpire2/steam/76561198118473939/*/modded`（Linux）

### 反编译

```shell
git clone https://github.com/icsharpcode/ILSpy.git
nix-shell -p dotnet-sdk_10 -p dotnet-runtime_10 -p powershell --run "cd ILSpy && dotnet build ILSpy.XPlat.slnf && dotnet ./ICSharpCode.ILSpyCmd/bin/Debug/net10.0/ilspycmd.dll -o $PWD ~/.steam/steam/steamapps/common/Slay\ the\ Spire\ 2/data_sts2_linuxbsd_x86_64/sts2.dll --nested-directories -p"
```
