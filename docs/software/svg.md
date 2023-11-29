# SVG

## 坐标轴

SVG 左上角是坐标 (0, 0)，x 轴正方向向右，y 轴正方向向下：

```
(0, 0) ---------> x
  |
  |
  |
  |
  V
  y
```

宽度是 x 方向上的长度，高度是 y 方向上的长度。

## line

Line：从 (x1, y1) 到 (x2,y2) 连一条直线：

```svg
<line x1="0" y1="100" x2="100" y2="0" stroke="black" />
<line x1="0" y1="0" x2="100" y2="100" stroke="blue" stroke-width="10" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" stroke-width="10" />
</svg>

用多条 line 绘制一个正方形：

```svg
<line x1="0" y1="0" x2="100" y2="0" stroke="black" />
<line x1="100" y1="0" x2="100" y2="100" stroke="black" />
<line x1="100" y1="100" x2="0" y2="100" stroke="black" />
<line x1="0" y1="100" x2="0" y2="0" stroke="black" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="0" x2="100" y2="0" stroke="black" />
    <line x1="100" y1="0" x2="100" y2="100" stroke="black" />
    <line x1="100" y1="100" x2="0" y2="100" stroke="black" />
    <line x1="0" y1="100" x2="0" y2="0" stroke="black" />
</svg>

## rect

Rect：以 (x,y) 为左上角，绘制一个 width x height 的矩形：

```svg
<line x1="0" y1="0" x2="100" y2="0" stroke="black" />
<line x1="0" y1="0" x2="0" y2="100" stroke="black" />
<rect x="10" y="10" width="80" height="80" fill="red" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="0" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="0" y2="100" stroke="black" />
    <rect x="10" y="10" width="80" height="80" fill="red" />
</svg>

## text

Text：默认以 (x,y) 为左下角，绘制一段文字

```svg
<rect x="10" y="10" width="100" height="30" fill="red" />
<text x="20" y="30">Hello, World!</text>
<circle cx="20" cy="30" r="2" fill="blue" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="110" height="30" fill="red" />
    <text x="20" y="30">Hello, World!</text>
    <circle cx="20" cy="30" r="2" fill="blue" />
</svg>

出现在后面的 text 会叠加在出现在前面的 rect 上。

### text-anchor

如果希望实现在 x 方向上居中绘制文字，可以用 `text-anchor="middle"`，此时定位的是正下方的坐标：

```svg
<rect x="10" y="10" width="110" height="30" fill="red" />
<text x="65" y="30" text-anchor="middle">Hello, World!</text>
<circle cx="65" cy="30" r="2" fill="blue" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="110" height="30" fill="red" />
    <text x="65" y="30" text-anchor="middle">Hello, World!</text>
    <circle cx="65" cy="30" r="2" fill="blue" />
</svg>

下面给出不同 `text-anchor` 设置的对比：

```svg
<rect x="10" y="10" width="180" height="90" fill="red" />
<text x="100" y="30" text-anchor="start">start</text>
<circle cx="100" cy="30" r="2" fill="blue" />
<text x="100" y="60" text-anchor="middle">middle</text>
<circle cx="100" cy="60" r="2" fill="blue" />
<text x="100" y="90" text-anchor="end">end</text>
<circle cx="100" cy="90" r="2" fill="blue" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="180" height="90" fill="red" />
    <text x="100" y="30" text-anchor="start">start</text>
    <circle cx="100" cy="30" r="2" fill="blue" />
    <text x="100" y="60" text-anchor="middle">middle</text>
    <circle cx="100" cy="60" r="2" fill="blue" />
    <text x="100" y="90" text-anchor="end">end</text>
    <circle cx="100" cy="90" r="2" fill="blue" />
</svg>

### dominant-baseline

如果要在 x 方向和 y 方向上都居中绘制文字，要在 `text-anchor="middle"` 的基础上，设置 `dominant-baseline="middle"`，此时定位点就是文本的中央：

```svg
<rect x="10" y="10" width="110" height="30" fill="red" />
<text x="65" y="25" text-anchor="middle" dominant-baseline="middle">Hello, World!</text>
<circle cx="65" cy="25" r="2" fill="blue" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="110" height="30" fill="red" />
    <text x="65" y="25" text-anchor="middle" dominant-baseline="middle">Hello, World!</text>
    <circle cx="65" cy="25" r="2" fill="blue" />
</svg>

因此，结合 `text-anchor` 和 `dominant-baseline`，可以定位文本的不同位置，实现各种对齐。

下面给出不同 `dominant-baseline` 设置的对比：

```svg
<rect x="10" y="10" width="180" height="280" fill="red" />
<text x="20" y="30" dominant-baseline="text-bottom">text-bottom abc123</text>
<line x1="20" y1="30" x2="160" y2="30" stroke="blue" stroke-width="1" />
<text x="20" y="60" dominant-baseline="alphabetic">alphabetic abc123</text>
<line x1="20" y1="60" x2="160" y2="60" stroke="blue" stroke-width="1" />
<text x="20" y="90" dominant-baseline="ideographic">ideographic abc123</text>
<line x1="20" y1="90" x2="160" y2="90" stroke="blue" stroke-width="1" />
<text x="20" y="120" dominant-baseline="middle">middle abc123</text>
<line x1="20" y1="120" x2="160" y2="120" stroke="blue" stroke-width="1" />
<text x="20" y="150" dominant-baseline="central">central abc123</text>
<line x1="20" y1="150" x2="160" y2="150" stroke="blue" stroke-width="1" />
<text x="20" y="180" dominant-baseline="mathematical">mathematical abc123</text>
<line x1="20" y1="180" x2="160" y2="180" stroke="blue" stroke-width="1" />
<text x="20" y="210" dominant-baseline="hanging">hanging abc123</text>
<line x1="20" y1="210" x2="160" y2="210" stroke="blue" stroke-width="1" />
<text x="20" y="240" dominant-baseline="text-top">text-top abc123</text>
<line x1="20" y1="240" x2="160" y2="240" stroke="blue" stroke-width="1" />
```

<svg height="250px" xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="180" height="280" fill="red" />
    <text x="20" y="30" dominant-baseline="text-bottom">text-bottom abc123</text>
    <line x1="20" y1="30" x2="160" y2="30" stroke="blue" stroke-width="1" />
    <text x="20" y="60" dominant-baseline="alphabetic">alphabetic abc123</text>
    <line x1="20" y1="60" x2="160" y2="60" stroke="blue" stroke-width="1" />
    <text x="20" y="90" dominant-baseline="ideographic">ideographic abc123</text>
    <line x1="20" y1="90" x2="160" y2="90" stroke="blue" stroke-width="1" />
    <text x="20" y="120" dominant-baseline="middle">middle abc123</text>
    <line x1="20" y1="120" x2="160" y2="120" stroke="blue" stroke-width="1" />
    <text x="20" y="150" dominant-baseline="central">central abc123</text>
    <line x1="20" y1="150" x2="160" y2="150" stroke="blue" stroke-width="1" />
    <text x="20" y="180" dominant-baseline="mathematical">mathematical abc123</text>
    <line x1="20" y1="180" x2="160" y2="180" stroke="blue" stroke-width="1" />
    <text x="20" y="210" dominant-baseline="hanging">hanging abc123</text>
    <line x1="20" y1="210" x2="160" y2="210" stroke="blue" stroke-width="1" />
    <text x="20" y="240" dominant-baseline="text-top">text-top abc123</text>
    <line x1="20" y1="240" x2="160" y2="240" stroke="blue" stroke-width="1" />
</svg>

这些值来自于字体的 [baseline 设置](https://en.wikipedia.org/wiki/Baseline_(typography))，见 [The 'bsln' table](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6bsln.html)。

## ellipse

Ellipse：椭圆或者圆，以 (cx, cy) 为中心，(rx, ry) 为 X 和 Y 方向上的半径：

```svg
<line x1="0" y1="0" x2="100" y2="0" stroke="black" />
<line x1="0" y1="0" x2="0" y2="100" stroke="black" />
<ellipse cx="50" cy="50" rx="40" ry="40" fill="red" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="0" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="0" y2="100" stroke="black" />
    <ellipse cx="50" cy="50" rx="40" ry="40" fill="red" />
</svg>

也可以直接用 circle 来画圆，此时只有一个半径：

```svg
<line x1="0" y1="0" x2="100" y2="0" stroke="black" />
<line x1="0" y1="0" x2="0" y2="100" stroke="black" />
<circle cx="50" cy="50" r="40" fill="blue" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="0" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="0" y2="100" stroke="black" />
    <circle cx="50" cy="50" r="40" fill="blue" />
</svg>

## path

path 允许用比较灵活的语法来绘制一段图形，语法类似于：移动到哪里，绘制一个到哪里的直线/曲线等等：

```svg
<path d="M 0 0 L 100 0, 100 100, 0 100" stroke="black" fill="none" />
```

<svg xmlns="http://www.w3.org/2000/svg">
    <path d="M 0 0 L 100 0, 100 100, 0 100" stroke="black" fill="none" />
</svg>

1. `M 0 0`（Move To），移动到 (0, 0)
2. `L 100 0`（Line To），从当前位置画一条线到 (100, 0)

此处给 `L` 命令传输了多个参数：(100, 0)、(100 100)、(0, 100)，相当于先划线到 (100, 0)，再划线到 (100, 100)，最后画到 (0, 100)。因为没有绘制回到原点的线，所以没有画成一个正方形。

完整的命令列表见 [Path commands](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#path_commands)，分为以下几类：

1. MoveTo（移动）: M, m
2. LineTo（画线）: L, l（画任意方向的线）, H, h（画横向线）, V, v（画纵向线）
3. Cubic Bézier Curve（三次贝塞尔曲线）: C, c, S, s
4. Quadratic Bézier Curve（二次贝塞尔曲线）: Q, q, T, t
5. Elliptical Arc Curve（椭圆上的弧线）: A, a
6. ClosePath（回到起始点）: Z, z

命令的大写版本通常表示参数采用的是绝对坐标；小写版本通常表示参数采用的是相对坐标，要从最后一次绘制的坐标加上相对坐标计算出新的绝对坐标。

## viewBox

viewBox 表示要显示坐标轴上哪个范围的内容，四个数字 `min-x min-y width height`：

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>
```

<svg viewBox="0 0 100 100" height="100px" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>

缩小 viewBox 以后，只能看到左上角的一段蓝线：

```svg
<svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>
```

<svg viewBox="0 0 50 50" height="100px" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>

缩小 viewBox 的同时，在页面中占用的空间不变，因此图像内容会显得更大：

```svg
<svg viewBox="40 40 20 20" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>
```

<svg viewBox="40 40 20 20" height="100px" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="100" x2="100" y2="0" stroke="black" />
    <line x1="0" y1="0" x2="100" y2="100" stroke="blue" />
</svg>

## 参考

- <https://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html>