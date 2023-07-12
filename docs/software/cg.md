# 计算机图形学

本文参考了如下网站：

- [OpenGL Projection Matrix](http://www.songho.ca/opengl/gl_projectionmatrix.html)
- [glOrtho](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glOrtho.xml)

## 齐次坐标

齐次坐标是在 3 维的坐标 $(x, y, z)$ 的基础上，添加一维，变成 $(x, y, z, w)$，对应 3 维的 $(x/w, y/w, z/w)$，这样做可以方便一些计算。

因此从 3 维坐标转换为齐次坐标的时候，添加一维 $w = 1$，变成 $(x, y, z, 1)$。

## 正交投影

正交投影要做的是把一个长方体线性映射到三个维度上都是 $[-1, 1]$ 之间的立方体。

这个长方体的边和坐标轴平行，因此可以用以下几个变量来定义长方体的坐标：

1. left, right, top, bottom：定义了长方体上平行于 X-Y 屏幕的面的位置，其中 left 和 right 就是 X 轴上的最小值和最大值，bottom 和 top 就是 Y 轴上的最小值和最大值
2. near，far：定义了长方体在 Z 轴上的区间，离原点最近的平面的 Z 值是 `-near`，最远的平面的 Z 值是 `-far`

下面用这些坐标的首字母来简称：$l$ 代表 left，依此类推。

目标是把这个长方体映射到 $[-1, 1]$ 的立方体上。

首先考虑 X 轴：要线性地把 $x=l$ 映射到 $x=-1$，把 $x=r$ 映射到 $x=1$，可以得到 $x' = \frac{2}{r-l}x-\frac{r+l}{r-l}$。

同理，Y 坐标的计算公式是 $y' = \frac{2}{t-b}y-\frac{t+b}{t-b}$。

Z 轴上多了一个负号：线性地把 $z=-n$ 映射到 $z=-1$，把 $z=-f$ 映射到 $z=1$，得到 $z' = \frac{-2}{f-n}z-\frac{f+n}{f-n}$。

总结一下就是：

$$
x' = \frac{2}{r-l}x-\frac{r+l}{r-l}
$$

$$
y' = \frac{2}{t-b}y-\frac{t+b}{t-b}
$$

$$
z' = \frac{-2}{f-n}z-\frac{f+n}{f-n}
$$

考虑到实际采用的是齐次坐标系，$w$ 不变，所以 $w' = w$。把上面的等式写成矩阵的形式，就是：

$$
\begin{pmatrix}
\frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\
0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\
0 & 0 & \frac{-2}{f-n} & -\frac{f+n}{f-n} \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

这正是 OpenGL 正交投影函数 glOrtho() 所计算的矩阵：

<figure markdown>
  ![](cg_glortho.png){ width="500" }
  <figcaption>正交投影矩阵（图源 <a href="https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glOrtho.xml">glOrtho</a>）</figcation>
</figure>


