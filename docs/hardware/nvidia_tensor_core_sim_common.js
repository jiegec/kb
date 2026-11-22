/* Tensor Core 模拟器共用的界面框架与格式化工具。
 *
 * 每个模拟器页面只提供：
 *   - <script id="model">：数值模型（voltaDot4 / ampDot），自带 module.exports 以便对拍
 *   - 配置对象：modes、data、compute、trace、note ...
 * 其余的建格子、选中、D 的渲染、下拉框、按钮都由这里负责。
 */
(function (global) {
  "use strict";

  function exponentOf(a) {
    let e = Math.floor(Math.log2(a));
    while (Math.pow(2, e) > a) e--;
    while (Math.pow(2, e + 1) <= a) e++;
    return e;
  }

  function fmtNum(x) {
    if (x === 0) return "0";
    if (!isFinite(x)) return x > 0 ? "∞" : "-∞";
    if (Number.isInteger(x) && Math.abs(x) < 1e15) return String(x);
    const a = Math.abs(x);
    if (a >= 1e6 || a < 1e-4) return x.toExponential(6).replace(/\.?0+e/, "e");
    return String(Number(x.toPrecision(10)));
  }

  // 格子放不下时用更短的写法，完整值挂在 title 上
  function cellText(v) {
    const full = fmtNum(v);
    if (full.length <= 8) return full;
    if (!isFinite(v) || v === 0) return full;
    for (let p = 6; p >= 1; p--) {
      const short = String(Number(v.toPrecision(p))).replace("e+", "e");
      if (short.length <= 8) return short;
    }
    for (let p = 3; p >= 0; p--) {
      const short = v.toExponential(p).replace("e+", "e");
      if (short.length <= 8) return short;
    }
    return String(v).replace("e+", "e");
  }

  function fitCell(node, text) {
    if (text.length >= 8) node.classList.add("small");
    else node.classList.remove("small");
  }

  function dimsText(m, n, fmtName) {
    return m + "×" + n + " " + fmtName;
  }

  function makeSim(cfg) {
    const modes = cfg.modes;
    const data = cfg.data;
    const state = { mode: cfg.defaultMode, si: 0, sj: 0 };

    const el = {
      mode: document.getElementById("mode"),
      note: document.getElementById("note"),
      trace: document.getElementById("trace"),
      traceTitle: document.getElementById("traceTitle"),
      aType: document.getElementById("aType"),
      bType: document.getElementById("bType"),
      cType: document.getElementById("cType"),
      dType: document.getElementById("dType"),
      gridA: document.getElementById("gridA"),
      gridB: document.getElementById("gridB"),
      gridC: document.getElementById("gridC"),
      gridD: document.getElementById("gridD"),
      btnReset: document.getElementById("btnReset"),
      btnRandom: document.getElementById("btnRandom")
    };

    Object.keys(modes).forEach(function (key) {
      const opt = document.createElement("option");
      opt.value = key;
      opt.textContent = modes[key].label;
      el.mode.appendChild(opt);
    });
    el.mode.value = state.mode;

    function shape() {
      return modes[state.mode];
    }

    function get(name, i, j) {
      if (name === "A") return data.A[i][j];
      if (name === "B") return data.B[i][j];
      return data.C[i][j];
    }

    function set(name, i, j, v) {
      if (!isFinite(v)) v = 0;
      if (name === "A") data.A[i][j] = v;
      else if (name === "B") data.B[i][j] = v;
      else data.C[i][j] = v;
    }

    function buildGrid(host, name, rows, cols, interactive) {
      host.innerHTML = "";
      host.style.gridTemplateColumns = "16px repeat(" + cols + ", var(--cw))";
      const corner = document.createElement("div");
      corner.className = "h";
      host.appendChild(corner);
      for (let j = 0; j < cols; j++) {
        const h = document.createElement("div");
        h.className = "h";
        h.textContent = j;
        host.appendChild(h);
      }
      for (let i = 0; i < rows; i++) {
        const h = document.createElement("div");
        h.className = "h";
        h.textContent = i;
        host.appendChild(h);
        for (let j = 0; j < cols; j++) {
          let node;
          if (interactive) {
            node = document.createElement("input");
            node.type = "text";
            node.inputMode = "decimal";
            node.className = "cell";
            node.dataset.name = name;
            node.dataset.i = String(i);
            node.dataset.j = String(j);
            node.value = fmtNum(get(name, i, j));
            node.addEventListener("input", function () { render(); });
            node.addEventListener("change", function () {
              set(name, i, j, parseFloat(node.value));
              render();
            });
          } else {
            node = document.createElement("button");
            node.type = "button";
            node.className = "cell";
            node.dataset.name = name;
            node.dataset.i = String(i);
            node.dataset.j = String(j);
            node.addEventListener("click", function () {
              state.si = i;
              state.sj = j;
              render();
            });
          }
          host.appendChild(node);
        }
      }
    }

    function rebuild() {
      const s = shape();
      if (state.si >= s.m) state.si = s.m - 1;
      if (state.sj >= s.n) state.sj = s.n - 1;
      buildGrid(el.gridA, "A", s.m, s.k, true);
      buildGrid(el.gridB, "B", s.k, s.n, true);
      buildGrid(el.gridC, "C", s.m, s.n, true);
      buildGrid(el.gridD, "D", s.m, s.n, false);
      el.aType.textContent = dimsText(s.m, s.k, cfg.fmtName(s.in));
      el.bType.textContent = dimsText(s.k, s.n, cfg.fmtName(s.in));
      el.cType.textContent = dimsText(s.m, s.n, cfg.fmtName(s.cFmt));
      el.dType.textContent = dimsText(s.m, s.n, cfg.fmtName(s.out));
      el.note.textContent = cfg.note(s);
      el.traceTitle.textContent = "D[" + state.si + "][" + state.sj + "] 的计算过程";
    }

    function drawValues(D) {
      document.querySelectorAll('[data-name="D"]').forEach(function (node) {
        const i = +node.dataset.i, j = +node.dataset.j;
        const txt = cellText(D[i][j]);
        node.textContent = txt;
        node.title = fmtNum(D[i][j]);
        fitCell(node, txt);
        if (i === state.si && j === state.sj) node.classList.add("sel");
        else node.classList.remove("sel");
      });
      document.querySelectorAll("input.cell").forEach(function (node) {
        if (document.activeElement === node) return;
        const txt = fmtNum(get(node.dataset.name, +node.dataset.i, +node.dataset.j));
        node.value = txt;
        node.title = txt;
        fitCell(node, txt);
      });
    }

    function render() {
      const s = shape();
      const D = [];
      for (let i = 0; i < s.m; i++) {
        D[i] = [];
        for (let j = 0; j < s.n; j++) D[i][j] = cfg.compute(data.A, data.B, data.C, i, j, state.mode).d;
      }
      drawValues(D);
      if (cfg.highlight) cfg.highlight(state);
      const res = cfg.compute(data.A, data.B, data.C, state.si, state.sj, state.mode);
      el.trace.textContent = cfg.trace(res, state.mode, state.si, state.sj);
    }

    el.mode.addEventListener("change", function () {
      state.mode = el.mode.value;
      rebuild();
      render();
    });
    el.btnReset.addEventListener("click", function () {
      cfg.reset();
      rebuild();
      render();
    });
    el.btnRandom.addEventListener("click", function () {
      cfg.random();
      rebuild();
      render();
    });

    cfg.reset();
    rebuild();
    render();
    return { state: state, rebuild: rebuild, render: render };
  }

  global.TC = {
    exponentOf: exponentOf,
    fmtNum: fmtNum,
    cellText: cellText,
    fitCell: fitCell,
    sim: makeSim
  };
})(window);
