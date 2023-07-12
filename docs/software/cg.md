# 计算机图形学

本文参考了如下网站：

- [OpenGL Projection Matrix - Song Ho Ahn](http://www.songho.ca/opengl/gl_projectionmatrix.html)
- [glOrtho](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glOrtho.xml)
- [gluPerspective](http://www.songho.ca/opengl/gl_projectionmatrix.html)
- [Projection matrices](https://eliemichel.github.io/LearnWebGPU/basic-3d-rendering/3d-meshes/projection-matrices.html)

## 齐次坐标

齐次坐标是在 3 维的坐标 $(x, y, z)$ 的基础上，添加一维，变成 $(x, y, z, w)$，对应 3 维的 $(x/w, y/w, z/w)$，这样做可以方便一些计算。

因此从 3 维坐标转换为齐次坐标的时候，添加一维 $w = 1$，变成 $(x, y, z, 1)$。

## Normalized Device Coordinates

NDC（Normalized Device Coordinates）是经过一系列变换以后，得到的最终的坐标。以 OpenGL 为例，NDC 就是一个在三个坐标轴上都在 $[-1, 1]$ 之间的立方体，只有在这个立方体中的物体才会被显示出来。

NDC 的坐标范围在不同的图形 API 下可能不一样，例如 OpenGL 和 WebGL 是从 $(-1, -1, -1)$ 到 $(1, 1, 1)$，而 DirectX-12、Metal、Vulkan 和 WebGPU 是从 $(-1, -1, 0)$ 到 $(1, 1, 1)$，也就是 Z 轴上的范围只有 $[0, 1]$。

最后显示在屏幕上的时候，显示区域的左下角就对应 $x=-1, y=-1$，右上角对应 $x=1, y=1$（也可能是左上角 $x=-1, y=-1$，右下角 $x=1, y=1$，不同的图形 API 规定不同）。$z$ 轴对应深度，显示在前面的（$z$ 较小的）会遮挡显示在后面的（$z$ 较大的）。

## 正交投影

正交投影要做的是把一个长方体线性映射到 NDC 中，以 OpenGL 为例，也就是要映射到三个维度上都是 $[-1, 1]$ 之间的立方体。

这个长方体的边和坐标轴平行，因此可以用以下几个变量来定义长方体的坐标：

1. left, right, top, bottom：定义了长方体上平行于 X-Y 屏幕的面的位置，其中 left 和 right 就是 X 轴上的最小值和最大值，bottom 和 top 就是 Y 轴上的最小值和最大值
2. near，far：定义了长方体在 Z 轴上的区间，离原点最近的平面的 Z 值是 `-near`，最远的平面的 Z 值是 `-far`

下面用这些坐标的首字母来简称：$l$ 代表 left，依此类推。

目标是把这个长方体映射到 $[-1, 1]$ 的立方体上。

首先考虑 X 轴：要线性地把 $x=l$ 映射到 $x=-1$，把 $x=r$ 映射到 $x=1$，可以得到 $x' = \frac{2}{r-l}x-\frac{r+l}{r-l}$。

同理，Y 坐标的计算公式是 $y' = \frac{2}{t-b}y-\frac{t+b}{t-b}$。

Z 轴上多了一个负号：线性地把 $z=-n$ 映射到 $z=-1$，把 $z=-f$ 映射到 $z=1$，得到 $z' = \frac{-2}{f-n}z-\frac{f+n}{f-n}$。

注：如果 NDC 的 Z 轴范围是 $[0, 1]$，那么 Z 轴的计算公式就是 $z' = \frac{-1}{f-n}z-\frac{n}{f-n}$

总结一下就是：

\begin{align}
x' = \frac{2}{r-l}x-\frac{r+l}{r-l} \\
y' = \frac{2}{t-b}y-\frac{t+b}{t-b} \\
z' = \frac{-2}{f-n}z-\frac{f+n}{f-n}
\end{align}

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
  ![](cg_glortho.png){ width="300" }
  <figcaption>正交投影矩阵（图源 <a href="https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glOrtho.xml">glOrtho</a>）</figcation>
</figure>

## 透视投影

透视投影要做的是把一个四棱台（Square Frustum，四棱锥水平切开，底面和顶面是正方形，其余四个面都是梯形）映射到 NDC 上。其中四棱台的四条棱延长以后，交于原点。也就是说焦点就是坐标轴的原点。

相比正交投影，透视投影最大的不同在于它近大远小的特性，更加贴近实际：正交投影无论深度多少，看到的物体大小不变；而在透视投影中，从原点出发，到 near 平面上的一点连成射线，这条射线上的点都对应同一个屏幕上的点，因此远的物体在屏幕上看的小，近的物体在屏幕上看得大。

因此在实现透视投影的时候，就要利用这条从原点出发到 near 平面的一点的射线：由于这条射线上的点都对应屏幕上同一个点，因此在 NDC 中也对应同一个 $(x', y')$ 坐标。那么，在计算 $x'$ 和 $y'$ 的时候，先利用相似三角形关系，把点映射到 near 平面上（near 平面的 Z 坐标是 $z=-n$）：

\begin{align}
\frac{x'}{x} = \frac{-n}{z} \\
\frac{y'}{y} = \frac{-n}{z}
\end{align}

这样就得到了四棱台到长方体的映射，但是这里涉及到对 $z$ 的除法运算，为了在矩阵中实现针对 $z$ 的除法运算，需要利用齐次坐标自带的除法：$(x, y, z, w) \to (x/w, y/w, z/w)$，也就是说，把 $z$ 的值挪到 $w$ 上，就相当于实现了除法。按照这个思路，可以得到下面的矩阵：

$$
\begin{pmatrix}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & A & B \\
0 & 0 & -1 & 0
\end{pmatrix}
$$

其中 $A$ 和 $B$ 是未知数。验证一下上面的矩阵是否实现了除法：

首先是生成齐次坐标：

$$
(x, y, z) \to (x, y, z, 1)
$$

矩阵变换以后：

\begin{align}
x' &= nx \\
y' &= ny \\
z' &= Az + B \\
w' &= -z
\end{align}

再从齐次坐标变回来，得到 $(-\frac{nx}{z}, -\frac{ny}{z}, -A-\frac{B}{z})$。可以看到，x 和 y 都得到了和前面用相似三角形计算出来一样的结果，但是 z 的值出现了变化。但是没有关系，虽然 z 的值变了，但是它依然是保序的，只需要继续保证它在 $[-f, -n]$ 范围即可：

\begin{align}
-n = -A-\frac{B}{-n} \\
-f = -A-\frac{B}{-f}
\end{align}

求解可得 $A=n+f, B=-nf$，因此前面的矩阵就是：

$$
\begin{pmatrix}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -nf \\
0 & 0 & -1 & 0
\end{pmatrix}
$$

到这一步，就完成了四棱台到长方体的映射，接下来就是正交投影了，把长方体映射到 NDC 上，因此最终整体的投影矩阵就是把两个矩阵乘起来（正交投影矩阵左乘上面的矩阵），得到的结果如下：

$$
\begin{pmatrix}
\frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\
0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\
0 & 0 & \frac{-2}{f-n} & -\frac{f+n}{f-n} \\
0 & 0 & 0 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -nf \\
0 & 0 & -1 & 0
\end{pmatrix}
=
\begin{pmatrix}
\frac{2n}{r-l} & 0 & \frac{r+l}{r-l} & 0 \\
0 & \frac{2n}{t-b} & \frac{t+b}{t-b} & 0 \\
0 & 0 & -\frac{n+f}{f-n} & \frac{-2nf}{f-n} \\
0 & 0 & -1 & 0
\end{pmatrix}
$$

这就是最终的透视投影的矩阵。需要注意的是，它假设了输入的坐标的 $w=1$，如果输入的齐次坐标的 $w \ne 1$，计算结果就会有问题。在 OpenGL 中，可以用 gluPerspective() 函数得到它：

<figure markdown>
  ![](cg_gluperspective.png){ width="300" }
  <figcaption>透视投影矩阵（图源 <a href="https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml">gluPerspective</a>）</figcation>
</figure>

和上面的结果看似不同，但只要设定 $r=-l, t=-b, f=\frac{n}{t}, aspect=\frac{r}{t}$，两个矩阵就是一样的。也就是说 gluPerspective 采用了透视投影的特殊情况：左右和上下对称。

其中 aspect 是长宽比（x 轴除以 y 轴）；$f=cot(\frac{fovy}{2})$ 是这么推导的：y 方向上的视野角度上下对称，角度大小是 $fovy$，那么在水平线上方的角度就是 $\frac{fovy}{2}$，而这个角度在三角形中，它的对边是 $t$，邻边是 $n$，所以 $tan(\frac{fovy}{2})=\frac{t}{n}$，反过来就得到 $f=\frac{n}{t}=cot(\frac{fovy}{2})$。

更加通用的 OpenGL 函数是 [glFrustum](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glFrustum.xml)，它得到的矩阵和上面推导出来的矩阵是一样的，没考虑特殊情况。


