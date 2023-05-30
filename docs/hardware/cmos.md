# CMOS

## MOSFET

MOSFET 有两种：NMOS 和 PMOS，电路符号如下：


<figure markdown>
  ![MOSFET](cmos_mosfet.png){ width="400" }
  <figcaption>PMOS 和 NMOS 的电路符号（图源 <a href="https://en.wikipedia.org/wiki/MOSFET">Wikipedia</a>）</figcaption>
</figure>

PMOS 和 NMOS 都有三个电极，分别是源级（Source），栅级（Gate）和漏级（Drain）。MOSFET 的特点是，在 $D$ 到 $S$ 的电流受到 $G$ 也就是栅级的电压的控制：

1. 当 $V_{GS} < V_{th}$ 时，$I_D=0$，此时 MOSFET 处于断开的状态
2. 当 $V_{GS} > V_{th}, V_{GD} > V_{th}$ 时，$I_D=\frac{1}{2}\mu_nC_{ox}\frac{W}{L}(2(V_{GS}-V_{th})V_{DS}-V_{DS}^2)$，此时 MOSFET 处于线性区
3. 当 $V_{GS} > V_{th}, V_{GD} < V_{th}$ 时，$I_D=\frac{1}{2}\mu_nC_{ox}\frac{W}{L}(V_{GS}-V_{th})^2[1+\lambda(V_{DS}-V_{DSsat})]$，此时 MOSFET 处于饱和区

这里的线性区和饱和区是在 $I_D - V_{DS}$ 特性曲线上说的（见下图），意思是当 $V_{GS} > V_{th}$ 的时候，随着 $V_{DS}$ 的增大，$I_D$ 首先会增大，直到 $V_{GD} > V_{th}$ 的时候，$I_D$ 饱和，几乎不再增加。严格来讲，所谓的线性区，实际上也不是直线，而是抛物线。

<figure markdown>
  ![I_D - V_{DS} Curve](cmos_id_vds.png){ width="400" }
  <figcaption> I<sub>D</sub> - V<sub>DS</sub> 特征曲线（图源清华大学张雷老师电子学基础课程的课件）</figcaption>
</figure>

PMOS 和 NMOS 的区别是电流的方向不同。PMOS 电流从 S 流向 D，NMOS 电流从 D 和 S。如果注意到上面 MOSFET 的符号的画法，会发现电流都是从上面往下流。此外还有一个规律，箭头连接的那一侧就是 S。

## 数字电路中的 CMOS

CMOS 全称是 Complementary metal–oxide–semiconductor，意思就是拿 PMOS 和 NMOS 的组合来实现电路。当 CMOS 被用来实现数字电路的时候，PMOS 和 NMOS 经常成对出现，PMOS 接到 $V_{DD}$，NMOS 接到 $GND$ 上。例如用 PMOS 和 NMOS 实现一个非门（NOT gate）：

<figure markdown>
  ![CMOS Not Gate](cmos_not_gate.png){ width="400" }
  <figcaption> CMOS 实现非门（图源 <a href="https://www.geeksforgeeks.org/cmos-logic-gate/">CMOS Logic Gate - Geeks for Geeks</a>）</figcaption>
</figure>

当输入为高电平的时候，NMOS 导通，PMOS 断开，此时输出通过 NMOS 接到了地上，所以输出低电平。当输入为低电平的时候，PMOS 导通，NMOS 断开，此时输出通过 PMOS 接到了电源上，所以输出高电平。用类似的方法，还可以设计出与非门（NAND gate）和或非门（NOR gate）：

<figure markdown>
  ![CMOD NAND and NOR Gate](cmos_nand_nor_gate.png){ width="400" }
  <figcaption> CMOS 实现与非门和或非门（图源 <a href="https://www.geeksforgeeks.org/cmos-logic-gate/">CMOS Logic Gate - Geeks for Geeks</a>）</figcaption>
</figure>

以及在工艺库里常见的 AOI（And Or Invert）和 OAI（Or And Invert）门：

<figure markdown>
  ![CMOD AOI and OAI Gate](cmos_aoi_oai_gate.png){ width="400" }
  <figcaption> CMOS 实现 AOI 和 OAI 门（图源 <a href="https://www.geeksforgeeks.org/cmos-logic-gate/">CMOS Logic Gate - Geeks for Geeks</a>）</figcaption>
</figure>

CMOS 在实现数字电路的时候，并没有用到它的线性区和饱和区的特性，只用到了 $V_{GS}$ 和 $V_{th}$ 的大小以及是否有电流的关系，可以认为 PMOS 和 NMOS 就是一个用电压控制的开关。

