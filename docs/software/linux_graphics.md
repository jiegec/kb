# Linux 图形软件栈

本文讨论 Linux 是如何驱动显卡显示内容的，以及这个过程中涉及到的各个软件的功能。

## 从 INT 10h 到 VBE

早期还没有图形界面的时候，需要显示的内容就是文本和光标，所以早期的显卡的功能也是围绕这个来实现的：BIOS 提供一段代码，当内核通过 [INT 10h](https://en.wikipedia.org/wiki/INT_10H) 进入 BIOS 的时候，它会执行 BIOS 的代码，去完成绘制文本和光标的任务。这个接口提供了如下功能：

1. 设置 video mode：文字有多少行多少列，多少种颜色，字体大小等等
2. 设置光标 cursor：移动到哪个位置，什么样式
3. 输出文字：在光标位置输出文字
4. 设置颜色：前景/后景颜色

例如 INT 10h AH=0Eh 的功能是输出一个字节到显示输出，其中 AL 寄存器保存要输出的字符。Linux 中用这个方法来实现 putchar：

```c
// in arch/x86/boot/tty.c
static void __section(".inittext") bios_putchar(int ch)
{
	struct biosregs ireg;

	initregs(&ireg);
	ireg.bx = 0x0007;
	ireg.cx = 0x0001;
	ireg.ah = 0x0e;
	ireg.al = ch;
	intcall(0x10, &ireg, NULL);
}
```

之后的版本引入了图形模式，可以控制分辨率，设置像素的颜色等等。这个过程十分原始，每次操作都需要在内核里用 INT 10h 调用 BIOS 的代码，效率很低。

随着时代的发展，INT 10h 更新为 [VESA BIOS Extensions（VBE）](http://www.petesqbsite.com/sections/tutorials/tuts/vbe3.pdf)。从 [VBE](https://wiki.osdev.org/VBE) 2.0 版本开始，引入了 frame buffer 的支持：在内存中设置一片连续区域来保存要显示的像素，内核把要显示的像素按照一定的格式写到 frame buffer 里面，一次 call 就可以把 frame buffer 里面的内容更新到显示输出上。

随着 UEFI 的出现，API 进化为 EFI 1.0 的 [Universal Graphic Adapter (UGA)](https://en.wikipedia.org/wiki/UEFI#Graphics_features) 和 UEFI
 的 [Graphics Output Protocol (GOP)](https://en.wikipedia.org/wiki/UEFI#GOP)。

## framebuffer

上文提到，从 VBE 2.0 开始，提供了 framebuffer 功能，使得内核可以比较自由地控制要绘制的内容，只需要把绘制的内容放到内存里，交给 VBE 就可以把内容显示出来。framebuffer 可以由内核来负责绘制，把用户态程序往 stdout 输出的文字绘制到 framebuffer 里面；也可以把 framebuffer 交给用户态，启动 X11 server 等等。

于是内核是怎么处理 framebuffer 的呢？framebuffer 可能由不同的硬件提供，所以需要一套设备类型来统一处理 framebuffer，那就是 fbdev。那么，VBE 2.0 提供的 framebuffer 功能，在 Linux 下的驱动就由  [vesafb](https://docs.kernel.org/fb/vesafb.html) 驱动（`drivers/video/fbdev/vesafb.c`）提供。

在启动的时候，Linux 内核会通过 VBE 的 Function 01h - Return VBE Mode Information 配置 framebuffer，如果配置成功，就会拿到一个物理地址 `lfb_base`（linear frame buffer base），以及对应的 frame buffer 格式。

UEFI 也是类似的：Linux 的 [efifb](https://docs.kernel.org/fb/efifb.html) 驱动会从 UEFI 中获取到 framebuffer 的地址等信息：

```log
efifb: probing for efifb
efifb: framebuffer at 0xc0000000, using 4032k, total 4032k
efifb: mode is 1280x800x32, linelength=5120, pages=1
efifb: scrolling: redraw
efifb: Truecolor: size=8:8:8:8, shift=24:16:8:0
```

检测到 framebuffer 以后，怎么去使用它呢？有两种办法：

1. 内核接管 framebuffer，生成一个 console（驱动是 [fbcon](https://docs.kernel.org/fb/fbcon.html)），内核负责 console 到 framebuffer 的绘制；相比之前的 `console -> VGA driver (INT 10h) -> hardware`，有统一的 framebuffer 驱动以后，变成了 `console -> fbcon -> fbdev driver -> hardware`
2. 同时创建设备 [`/dev/fb*`](https://docs.kernel.org/fb/framebuffer.html)，用户可以通过读写这些设备文件来修改 framebuffer 的内容；此外，还可以用 ioctl 命令去操控 framebuffer（定义在 `linux/fb.h`）

现在如果安装了 Linux 发行版，又没有启动图形界面，那么大概率看到的就是一个 fbcon 驱动提供的 console，底层是 efifb 或者平台相关的 fb 驱动，例如 i915drmfb（Intel 显卡），nouveaudrmfb（NVIDIA 显卡），astdrmfb（ASPEED 显卡）等等。也可能是用户态的 [kmscon](https://wiki.archlinux.org/title/KMSCON) 程序提供的 console，代替 fbcon 的功能，用 drm 或者 fbdev 在用户态实现 console 绘制。

图形界面，例如 X11，也可以用 fbdev 的 framebuffer 来绘制内容：[xf86-video-fbdev](https://gitlab.freedesktop.org/xorg/driver/xf86-video-fbdev)。

framebuffer 提供了一个比较简单的接口，使得内核和用户都可以通过它去控制要显示的内容，而不单单是普通的 80 列 25 行的文字。但现在的显卡要复杂的多，要支持各种图形 API，各种硬件加速功能，所以简单的 framebuffer 功能不能满足高性能图形的需求。因此现在用的比较多的是 DRM（Direct Rendering Manager），后面会介绍它。

## X11

X11 是常用的图形界面系统，它的架构是比较传统的 Client/Server：系统中运行一个 X Server，然后用户程序是 X Client。X Client 通过 Socket 和 X Server 通讯，告诉 X Server 需要绘制哪些图形；X Server 负责显示以及键盘鼠标的交互，如果用户操作了键盘鼠标，则会把相应的事件通过 Socket 通知 X Client。

这种 Client/Server 的设计使得 X11 可以远程使用：经典的 SSH X Forwarding，就是在远程系统上运行 X Client，用本地的 X Server 显示。

Client 和 Server 之间的通信协议是 [X Window System Protocol](https://www.x.org/releases/X11R7.7/doc/xproto/x11protocol.html)，用户可以用 libX11（Xlib）或者 XCB（X C Binding）直接在 X Protocol 层次上进行开发。下面是一个例子，用 libX11（Xlib）库来和 X Server 建立连接，创建窗口并绘制的例子（来自 [Rosetta Code](https://rosettacode.org/wiki/Window_creation/X11#C)）：

```c
#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
   Display *d;
   Window w;
   XEvent e;
   const char *msg = "Hello, World!";
   int s;

   d = XOpenDisplay(NULL);
   if (d == NULL) {
      fprintf(stderr, "Cannot open display\n");
      exit(1);
   }

   s = DefaultScreen(d);
   w = XCreateSimpleWindow(d, RootWindow(d, s), 10, 10, 100, 100, 1,
                           BlackPixel(d, s), WhitePixel(d, s));
   XSelectInput(d, w, ExposureMask | KeyPressMask);
   XMapWindow(d, w);

   while (1) {
      XNextEvent(d, &e);
      if (e.type == Expose) {
         XFillRectangle(d, w, DefaultGC(d, s), 20, 20, 10, 10);
         XDrawString(d, w, DefaultGC(d, s), 10, 50, msg, strlen(msg));
      }
      if (e.type == KeyPress)
         break;
   }

   XCloseDisplay(d);
   return 0;
}
```

编译：`gcc test.c -lX11 -o test` 并运行，就可以看到一个窗口，窗口上有一个正方形和一段 `Hello, World!`。查看 strace，可以看到它打开了 `/tmp/.X11-unix/` 下面的 unix socket，每个 DISPLAY 对应一个 unix socket，然后通过它和 X Server 进行了通信。

可见在 X11 的架构下，实际负责绘制的是 Server，Client 会把命令发送给 Server。但是这样做效率会比较低，因为要在 Client 和 Server 之间来回通信。因此后来 X11 引入了 Direct Rendering Infrastructure（DRI）：Client 和 GPU 通信，进行硬件加速的绘制，而不是 Client 发送给 Server，让 Server 去和 GPU 通信。

Wayland 在这个思路上走得更远：把绘制的大部分工作交给 Client，此时 Server 要负责的就是把来自不同 Client 绘制的内容组合成最后显示的结果，因此 Wayland 的 Server 叫做 Compositor。Server 和 Client 之间通过 CPU 上的内存（通过 shared memory，shm）或者 GPU 上的内存（通过 DMABUF）来传输要绘制的像素。其实就是每个 Client 都有自己的 framebuffer，然后 Server 把来自不同 Client 的 framebuffer 组装成最终显示出来的 framebuffer。

## DRM & KMS

Direct Rendering Manager（DRM）是内核里负责和硬件打交道，同时又给用户态提供硬件加速能力的驱动。在用户态一侧，则是 Mesa 提供 OpenGL/Vulkan 等图形 API。可以用 [drm_info](https://gitlab.freedesktop.org/emersion/drm_info) 查看系统中 DRM 设备的状态。

[Kernel Mode Setting（KMS）](https://www.kernel.org/doc/html/v4.15/gpu/drm-kms.html) 是让内核负责配置显示输出的分辨率等等模式（Mode Set），因为只有确定了分辨率等参数，才能确定 framebuffer 的大小和格式。
