# CVT 时序计算

VESA CVT（Coordinated Video Timings）的时序计算器：输入分辨率和刷新率，选择标准 CVT（CRT 式消隐）、CVT-RB v1、CVT-RB v2 或 CVT-RB v3，得到完整的行/场时序并画出波形。其中 CVT 和 RB v1 按 CVT 1.2（2.0 起这两条公式已从规范里移除，只留引用），RB v2 / RB v3 按 CVT 2.1。

## 计算器

<div class="cvt-calc" id="cvt-calc">
  <div class="cvt-inputs">
    <label>H 像素 <input id="cvt-h" type="number" value="1920" min="8" step="1"></label>
    <label>V 行数 <input id="cvt-v" type="number" value="1080" min="1" step="1"></label>
    <label>刷新率 <input id="cvt-rate" type="number" value="60" min="1" step="0.001"></label>
    <label>类型
      <select id="cvt-mode">
        <option value="crt">CVT</option>
        <option value="rb">CVT-RB v1</option>
        <option value="rb2">CVT-RB v2</option>
        <option value="rb3" selected>CVT-RB v3</option>
      </select>
    </label>
    <label>Hblank（RBv3）<input id="cvt-hblank" type="number" value="80" min="80" max="200" step="8"></label>
    <label><input id="cvt-early" type="checkbox"> EARLY_VSYNC（RBv3）</label>
    <label><input id="cvt-altvblank" type="checkbox"> 交替 VBlank 300 µs（RBv2/v3，DP）</label>
    <label>色深
      <select id="cvt-bpc">
        <option value="8" selected>8 bpc</option>
        <option value="10">10 bpc</option>
        <option value="12">12 bpc</option>
        <option value="16">16 bpc</option>
      </select>
    </label>
    <label>色度
      <select id="cvt-chroma">
        <option value="444" selected>4:4:4</option>
        <option value="422">4:2:2</option>
        <option value="420">4:2:0</option>
      </select>
    </label>
    <label>宽高比
      <select id="cvt-ar">
        <option value="16:9" selected>16:9</option>
        <option value="16:10">16:10</option>
        <option value="4:3">4:3</option>
        <option value="5:4">5:4</option>
        <option value="15:9">15:9</option>
      </select>
    </label>
  </div>
  <div class="cvt-info" id="cvt-info"></div>
  <div class="cvt-values" id="cvt-values"></div>
  <div id="cvt-svg"></div>
  <details class="cvt-steps" open>
    <summary>计算过程</summary>
    <div id="cvt-steps"></div>
  </details>
</div>

## 四种时序的区别

**CVT（标准，CRT 式，CVT 1.2）** 按 CRT 的需求给出较大的水平消隐，消隐宽度由 GTF 占空比公式算出（$C' - M' \times H_{period}$，$C'=30$、$M'=300$），并且不低于行周期的 20%；行同步占行周期 8%，后肩取消隐的一半，前肩为余量。垂直方向要求「同步 + 后肩」至少 550 µs、后肩至少 6 行，前肩固定 3 行。像素时钟向下取整到 0.25 MHz。

**CVT-RB v1（CVT 1.2）** 面向不需要大消隐的固定像素显示器：水平消隐固定 160 像素（同步 32、后肩 80、前肩 48），垂直消隐至少 460 µs，前肩 3 行、后肩至少 6 行。相比标准 CVT 能显著降低像素时钟（1080p60 从 173.0 MHz 降到 138.5 MHz）。

**CVT-RB v2（CVT 2.1）** 把水平消隐压到 80 像素（同步 32、前肩 8、后肩 40），水平有效像素可以是任意 1 像素精度；垂直同步固定 8 行、后肩固定 6 行、前肩为余量，VBlank 至少 460 µs（DisplayPort 允许时可用 300 µs 的交替下限）。像素时钟精度 0.001 MHz，并把 1000/1001 用于视频优化帧率（59.94 Hz 等）——用标称帧率算消隐、再乘系数算时钟，最后向下取整。1080p60 的时钟是 133.32 MHz。

**CVT-RB v3（CVT 2.1）** 面向 Adaptive-Sync（VRR）：先把目标刷新率加 350 ppm，用调整后的值算消隐和时钟，像素时钟改成**向上**取整（0.001 MHz），所以实际刷新率总比目标略高，差值交给 VRR 用额外的垂直消隐行吸收。它不用 1000/1001 系数（只支持逐行），**HActive 必须是 8 的倍数**；水平消隐默认 80，可再加 0–120（8 的倍数，最大 200），同步固定 32、前肩固定 8，其余给后肩。垂直同步固定 8 行、后肩 6 行、前肩为余量，VBlank 至少 460 µs（DP 允许时可用 300 µs 的交替下限）。1080p60 的时钟是 133.367 MHz，比 RBv2 的 133.320 MHz 略高。计算器还提供了 RBv3 的 EARLY_VSYNC 选项：后肩改为 $\lfloor VBI/2 \rfloor$，在 VSYNC 和有效图像之间留更多时间。

垂直同步的宽度用来表示宽高比（标准 CVT 与 RB v1）：

| 宽高比 | Vsync 行数 |
| --- | --- |
| 4:3 | 4 |
| 16:9 | 5 |
| 16:10 | 6 |
| 5:4 / 15:9 | 7 |
| RB v2 / RB v3 | 8（宽高比由 H/V active 推出） |

同步极性也用来区分时序类型：标准 CVT 是 H−/V+，RB 系列是 H+/V−。

计算器没有实现 CVT 的 margin（边距）和隔行模式；RBv3 本身也只支持逐行。

## 数据速率

数据速率 = 像素时钟 × 每像素比特数。8 bpc 的 RGB / Y′CBCR 4:4:4 每像素 24 bit，所以 1080p60 的 CVT 是 $173.000 \times 24 = 4.15$ Gbit/s；10/12/16 bpc 分别再乘 1.25/1.5/2，4:2:2 除以 1.5，4:2:0 除以 2。计算器上方可以直接切换色深和色度。

RBv3 的最小 VBlank 取 460 µs 还是 300 µs 会直接影响数据速率：1080p60 从 133.367 MHz（3.20 Gbit/s）降到 132.047 MHz（3.17 Gbit/s）。

## 参考

- VESA Coordinated Video Timings (CVT) Standard, Version 1.2
- VESA CVT v1.2 Errata E2（2021，Reduced Blanking v3）
- VESA Coordinated Video Timings (CVT) Standard, Version 2.1（2023）
