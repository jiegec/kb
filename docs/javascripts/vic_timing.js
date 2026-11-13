// Interactive VIC timing visualization for docs/hardware/cta_vic.md
(function () {
	"use strict";

	var COLORS = {
		active: "rgba(76, 175, 80, 0.35)",
		sync: "rgba(239, 83, 80, 0.35)",
		blank: "rgba(33, 150, 243, 0.22)"
	};
	var X0 = 120; // plot left
	var X1 = 930; // plot right
	var W = X1 - X0;

	function esc(s) {
		return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
	}

	function r2(n) {
		return Math.round(n * 100) / 100;
	}

	// level of the signal inside one segment; yHigh/yLow picked by caller
	function levelFor(seg, mode, pol) {
		if (mode === "sync") {
			if (seg.kind === "sync") return pol === "P" ? 1 : 0;
			return pol === "P" ? 0 : 1;
		}
		return seg.kind === "active" ? 1 : 0;
	}

	function stepPath(segs, total, yHigh, yLow, mode, pol) {
		var d = [], x = X0, prev = null, i, s, w, y;
		for (i = 0; i < segs.length; i++) {
			s = segs[i];
			w = (s.w / total) * W;
			y = levelFor(s, mode, pol) ? yHigh : yLow;
			if (prev === null) d.push("M" + r2(x) + " " + y);
			else if (prev !== y) d.push("L" + r2(x) + " " + prev + " L" + r2(x) + " " + y);
			d.push("L" + r2(x + w) + " " + y);
			prev = y;
			x += w;
		}
		return d.join(" ");
	}

	function boundaries(segs, total) {
		var xs = [X0], acc = 0, i;
		for (i = 0; i < segs.length - 1; i++) {
			acc += segs[i].w;
			xs.push(X0 + (acc / total) * W);
		}
		return xs;
	}

	function band(segs, total, y0, y1) {
		var out = [], x = X0, i, s, w;
		for (i = 0; i < segs.length; i++) {
			s = segs[i];
			w = (s.w / total) * W;
			out.push('<rect x="' + r2(x) + '" y="' + y0 + '" width="' + r2(w) + '" height="' + (y1 - y0) +
				'" fill="' + COLORS[s.kind === "active" ? "active" : s.kind === "sync" ? "sync" : "blank"] +
				'" stroke="currentColor" stroke-opacity="0.35" stroke-width="0.5"></rect>');
			x += w;
		}
		return out.join("\n");
	}

	function ticks(xs, y0, y1) {
		var out = [], i;
		for (i = 1; i < xs.length; i++) {
			out.push('<line x1="' + r2(xs[i]) + '" y1="' + y0 + '" x2="' + r2(xs[i]) + '" y2="' + y1 +
				'" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="3 3"></line>');
		}
		return out.join("\n");
	}

	function legend(items, y) {
		var out = [], x = X0, i, it, tx, label;
		for (i = 0; i < items.length; i++) {
			it = items[i];
			out.push('<rect x="' + r2(x) + '" y="' + (y - 8) + '" width="9" height="9" rx="1.5" fill="' +
				COLORS[it.kind === "active" ? "active" : it.kind === "sync" ? "sync" : "blank"] +
				'" stroke="currentColor" stroke-opacity="0.35" stroke-width="0.5"></rect>');
			label = it.label + " " + it.value;
			out.push('<text x="' + r2(x + 13) + '" y="' + y + '" font-size="11" fill="currentColor">' + esc(label) + "</text>");
			x += 13 + label.length * 6.2 + 16;
		}
		return out.join("\n");
	}

	function waveformPanel(cfg) {
		var segs = cfg.segs, total = cfg.total, out = [];
		var xs = boundaries(segs, total);
		out.push('<text x="' + X0 + '" y="' + cfg.titleY + '" font-size="12" fill="currentColor" opacity="0.85">' +
			esc(cfg.title) + "</text>");
		out.push(ticks(xs, cfg.syncHigh - 4, cfg.bandY1 + 2));
		out.push('<text x="106" y="' + (cfg.syncHigh + 11) + '" font-size="11" text-anchor="end" fill="currentColor">' +
			esc(cfg.syncName) + "</text>");
		out.push('<path d="' + stepPath(segs, total, cfg.syncHigh, cfg.syncLow, "sync", cfg.pol) +
			'" fill="none" stroke="currentColor" stroke-width="1.6"></path>');
		out.push('<text x="106" y="' + (cfg.dataHigh + 11) + '" font-size="11" text-anchor="end" fill="currentColor">DE</text>');
		out.push('<path d="' + stepPath(segs, total, cfg.dataHigh, cfg.dataLow, "data", cfg.pol) +
			'" fill="none" stroke="currentColor" stroke-width="1.6"></path>');
		out.push(band(segs, total, cfg.bandY0, cfg.bandY1));
		out.push('<text x="' + X1 + '" y="' + (cfg.bandY1 + 16) + '" font-size="11" text-anchor="end" fill="currentColor" opacity="0.8">' +
			esc(cfg.totalLabel) + "</text>");
		out.push(legend(cfg.legendItems, cfg.legendY));
		return out.join("\n");
	}

	function render(data, index) {
		var v = data[index];
		var info = document.getElementById("vic-info");
		if (info) {
			info.textContent = "VIC " + v.vic + " · " + v.ha + "×" + v.va + (v.ip === "i" ? "i" : "p") +
				" · " + v.ar + " · " + v.vf.toFixed(3) + " Hz · 像素时钟 " + v.pf.toFixed(3) + " MHz" +
				" · H 极性 " + v.hpol + " / V 极性 " + v.vpol + " · Ln " + v.ln;
		}

		var hSegs = [
			{ kind: "blank", w: v.hfront },
			{ kind: "sync", w: v.hsync },
			{ kind: "blank", w: v.hback },
			{ kind: "active", w: v.ha }
		];
		var hLegend = [
			{ kind: "blank", label: "Hfront", value: v.hfront },
			{ kind: "sync", label: "Hsync", value: v.hsync },
			{ kind: "blank", label: "Hback", value: v.hback },
			{ kind: "active", label: "Hactive", value: v.ha }
		];

		var vSegs, vLegend, vTitle;
		if (v.ip === "i") {
			var half = v.va / 2;
			vSegs = [
				{ kind: "blank", w: v.vfront }, { kind: "sync", w: v.vsync }, { kind: "blank", w: v.vback },
				{ kind: "active", w: half, field: 1 },
				{ kind: "blank", w: v.vfront }, { kind: "sync", w: v.vsync }, { kind: "blank", w: v.vback },
				{ kind: "active", w: half, field: 2 }
			];
			vTitle = "场时序（共 " + v.vt + " 行，每场 " + v.va / 2 + " 行有效）";
			vLegend = [
				{ kind: "blank", label: "Vfront", value: v.vfront },
				{ kind: "sync", label: "Vsync", value: v.vsync },
				{ kind: "blank", label: "Vback", value: v.vback },
				{ kind: "active", label: "Vactive/场", value: half }
			];
		} else {
			vSegs = [
				{ kind: "blank", w: v.vfront },
				{ kind: "sync", w: v.vsync },
				{ kind: "blank", w: v.vback },
				{ kind: "active", w: v.va }
			];
			vTitle = "场时序（一个帧周期）";
			vLegend = [
				{ kind: "blank", label: "Vfront", value: v.vfront },
				{ kind: "sync", label: "Vsync", value: v.vsync },
				{ kind: "blank", label: "Vback", value: v.vback },
				{ kind: "active", label: "Vactive", value: v.va }
			];
		}

		var parts = [];
		parts.push('<svg viewBox="0 0 960 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">');
		parts.push(waveformPanel({
			title: "行时序（一个行周期，共 " + v.ht + " 个像素）",
			titleY: 18,
			syncName: "HSYNC (" + v.hpol + ")",
			pol: v.hpol,
			segs: hSegs, total: v.ht,
			syncHigh: 38, syncLow: 62, dataHigh: 82, dataLow: 106,
			bandY0: 118, bandY1: 138,
			totalLabel: "Htotal " + v.ht,
			legendItems: hLegend, legendY: 162
		}));
		parts.push(waveformPanel({
			title: vTitle,
			titleY: 218,
			syncName: "VSYNC (" + v.vpol + ")",
			pol: v.vpol,
			segs: vSegs, total: v.vt,
			syncHigh: 238, syncLow: 262, dataHigh: 282, dataLow: 306,
			bandY0: 318, bandY1: 338,
			totalLabel: "Vtotal " + v.vt,
			legendItems: vLegend, legendY: 362
		}));
		parts.push("</svg>");

		var target = document.getElementById("vic-svg");
		if (target) target.innerHTML = parts.join("\n");
	}

	function init() {
		var root = document.getElementById("vic-widget");
		if (!root || !window.VIC_DATA || !window.VIC_DATA.length) return;
		if (root.getAttribute("data-ready") === "1") return;
		root.setAttribute("data-ready", "1");

		var data = window.VIC_DATA;
		var sel = document.getElementById("vic-select");
		if (!sel) return;

		var counts = {}, i, opt, label;
		for (i = 0; i < data.length; i++) counts[data[i].vic] = (counts[data[i].vic] || 0) + 1;
		for (i = 0; i < data.length; i++) {
			opt = document.createElement("option");
			opt.value = String(i);
			label = "VIC " + data[i].vic + " · " + data[i].ha + "×" + data[i].va +
				(data[i].ip === "i" ? "i" : "p") + " · " + data[i].vf.toFixed(3) + " Hz · " + data[i].ar;
			if (counts[data[i].vic] > 1) label += " · Vtotal " + data[i].vt;
			opt.textContent = label;
			sel.appendChild(opt);
		}

		sel.addEventListener("change", function () {
			render(data, parseInt(sel.value, 10) || 0);
		});

		// preselect: ?vic=16 or the first entry
		var want = null;
		var m = /[?&]vic=(\d+)/.exec(window.location.search);
		if (m) {
			var target = parseInt(m[1], 10);
			for (i = 0; i < data.length; i++) {
				if (data[i].vic === target) { want = i; break; }
			}
		}
		if (want === null) want = 0;
		sel.value = String(want);
		render(data, want);
	}

	function boot() {
		if (window.document$ && typeof window.document$.subscribe === "function") {
			window.document$.subscribe(init);
		} else if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", init);
		} else {
			init();
		}
	}

	boot();
})();
