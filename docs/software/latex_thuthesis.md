# thuthesis 学位论文排版

- float（algorithm/figure/table）用 htb 不要 p：`图宜紧置于首次引用该图的文字之后。图应尽可能显示在同一页（屏）。`
- 算法用 algorithm 而不用 lstlisting
- 图片用 PPTX 或 matplotlib 转 PDF 用 includegraphics 插入，英文要翻译成中文
- 正文用 SimSun + Times New Roman 字体，包括图片
- matplotlib 配置：`matplotlib.rcParams.update({"font.size": 14, "font.family": ["Times New Roman", "SimSun"], "pdf.fonttype": 42})`
- 表格用居中 `c`：`表单元格中的文字一般应居中书写（上下居中，左右居中），不宜左右居中书写的，可采取两端对齐的方式书写。`
- 公式用 `equation` 环境加 `label`，用 `式（\ref{label}）` 引用：`表达式在文字叙述中采用“式（3-1）”或“式（3.1）”形式，在编号中用“（3-1）”或“（3.1）”形式。`
- 公式内部用 `&=` 对齐：`较长的表达式必须转行时，应在“=”或者“+”“-”“×”“/”等运算符或者“]”“}”等括号之后回行。上下行尽可能在“=”处对齐。`

参考：[研究生学位论文写作指南（Guide to Thesis Writing for Graduate Students）](https://info.tsinghua.edu.cn/f/info/xxfb_fg/xnzx/template/detail?xxid=fa880bdf60102a29fbe3c31f36b76c7e)
