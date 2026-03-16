# 尖塔

## 杀戮尖塔 2

### 铁甲战士

#### 易伤流

思路：先给敌人上易伤，熔融之拳把层数翻倍，最后用主宰把易伤转成力量。

普通：

- 痛击（Bash）：造成 8 点伤害。给予 2 层易伤。
- 闪电霹雳（Thunderclap）：对所有敌人造成 4 点伤害，给予 1 层易伤。
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

思路：捕捉灵魂攒灵魂过牌，吊杀和死亡行军打伤害，守墓人和挽歌保命，唤起和预借时间给能量。

普通：

- 守墓人（Grave Warden）：获得 8 点格挡。将一张灵魂放入你的抽牌堆中。
- 违逆（Defy）：虚无。获得 6 点格挡。给予 1 层虚弱。
- 唤起（Invoke）：在下个回合召唤 2 并获得 2 能量。
- 鬼火（Wisp）：获得 1 能量。消耗。

罕见：

- 纠缠（Haunt）：每当你打出一张灵魂时，随机一名敌人失去 6 生命。
- 挽歌（Dirge）：召唤 3X 次。将 X 张灵魂添加到你的抽牌堆中。
- 捕捉灵魂（Capture Spirit）：敌人失去 3 生命。将 3 张灵魂加入你的抽牌堆。
- 预借时间（Borrowed Soul）：给予自身 3 层灾厄。获得 1 能量。
- 死亡行军（Death March）：造成 8 点伤害。在你回合进行中每抽到一张牌，都会使其额外造成 3 点伤害。
- 灵魂风暴（Soul Storm）：造成 9 点伤害。你的消耗牌堆中每有一张灵魂，伤害增加 2。

稀有：

- 吊杀（Hang）：造成 10 点伤害。让所有“吊杀”牌对这名敌人造成的伤害翻倍。

与灾厄流配合，通过不断打出灵魂来触发湮灭，配合预借时间，触发厄运之衣，再用死亡之门防守：

- 湮灭（Oblivion）：你在本回合内每打出一张牌，就给予该敌人 3 层灾厄。
- 厄运之衣（Shroud）：每当你给予灾厄时，获得 2 点格挡。
- 死亡之门（Death's Door）：获得 6 点格挡。如果你在本回合中曾给予过灾厄，则额外获得 2 次格挡。

无限：

- 捕捉灵魂加回复费用牌（预借时间或疯狂科学）：
    - 前置条件：卡组够小，有捕捉灵魂和一张回费牌（预借时间，或在打造时间事件中获得疯狂科学并充能改造）。
    - 卡牌说明：
        - 捕捉灵魂（Capture Spirit，耗费 1 能量）：敌人失去 3 生命。将 3 张灵魂加入你的抽牌堆。
        - 预借时间（Borrowed Time，耗费 0 能量）：给予自身 3 层灾厄。获得 1 能量。
        - 疯狂科学（Mad Science，耗费 1 能量）：获得 8 点格挡。获得 2 能量。
    - 无限流程：把无关牌留在手上，先打捕捉灵魂抽灵魂，抽到回费牌（预借时间或疯狂科学）和捕捉灵魂后，打回费牌，循环。
    - 捕捉灵魂可换成其他打伤害同时产灵魂的牌，如剥夺（耗费 1 能量，造成 9 点伤害。将一张灵魂加入你的抽牌堆）；如有纠缠（每当你打出一张灵魂时，随机一名敌人失去 6 生命），其他产灵魂的牌也可用。

### 创建 Mod

以下步骤适用于 v0.98.3 版本，参考了 [STS2 Early Access Mod Guide](https://www.reddit.com/r/slaythespire/comments/1rm5gvg/sts2_early_access_mod_guide/)：

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

8. 在项目根目录创建 `FirstMod` 子目录，放入一张名为 `mod_image.png` 的图片作为 Mod 封面
9. 点击 Project -> Export...，Add... -> Windows Desktop
10. 在 Resources 选项卡选择 Export selected resources，勾选 `mod_image.png` 和 `mod_manifest.json`，点击 Export PCK/ZIP，保存为 `FirstMod.pck`。也可以用命令行导出：`/Applications/Godot_mono.app/Contents/MacOS/Godot --export-pack "Windows Desktop" FirstMod.pck --headless`
11. 将 `./.godot/mono/temp/bin/Debug/FirstMod.dll` 和 `FirstMod.pck` 复制到游戏 `mods/FirstMod` 目录（路径：macOS 为 `/Library/Application\ Support/Steam/steamapps/common/Slay\ the\ Spire\ 2/SlayTheSpire2.app/Contents/MacOS/mods/FirstMod`，Linux 为 `~/.steam/steam/steamapps/common/Slay\ the\ Spire\ 2/mods/FirstMod`），目录不存在则手动创建
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

v0.98.3 已知问题：macOS ARM 能构建 dll 和 pck，但游戏无法加载；Linux 版游戏可以加载 macOS 构建的文件。

Beta v0.99 已修复 macOS 加载 Mod 的问题，改动如下：

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
