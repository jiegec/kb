// CVT / CVT-RB / CVT-RB v2 timing calculator (VESA CVT 1.2)
(function (global) {
	"use strict";

	var CELL_GRAN = 8;

	var VSYNC_BY_AR = { "4:3": 4, "16:9": 5, "16:10": 6, "5:4": 7, "15:9": 7 };

	function compute(o) {
		var h = Math.max(1, Math.floor(o.h));
		var v = Math.max(1, Math.floor(o.v));
		var rate = o.rate;
		var mode = o.mode;
		var steps = [];

		function f(x, d) {
			return x.toFixed(d === undefined ? 3 : d);
		}

		if (mode === "crt" || mode === "rb") return computeLegacy(o, f, steps);

		/* CVT 2.1: RB Timing v2 / v3 */
		var is2 = mode === "rb2";
		var PPM = is2 ? 0 : 350;
		var gran = is2 ? 1 : 8;                 // C_CELL_GRAN_RND: v2 1, v3 8
		var minVBlank = o.altVblank ? 300 : 460; // C_RB_MIN_V_BLANK / C_RB_ALT_MIN_V_BLANK

		var hActive = Math.floor(h / gran) * gran;
		var vLines = v;

		// v2: blanking uses the nominal rate, pixel clock uses the target rate (× 1000/1001 if video-optimized)
		var nominal = rate, mult = 1;
		if (is2) {
			var cand = rate * 1000 / 1001;
			if (Math.abs(cand - Math.round(cand)) < 0.01) {
				nominal = Math.round(cand);
				mult = 1000 / 1001;
			}
		}
		var rateBlank = is2 ? nominal : rate * (1 + PPM / 1e6);
		var rateClock = is2 ? nominal * mult : rate * (1 + PPM / 1e6);

		if (!is2) steps.push("V_FIELD_RATE = " + f(rate) + " × (1 + 350 ppm) = " + f(rateClock) + " Hz");
		if (o.altVblank) steps.push("使用交替最小 VBlank：300 µs（DP 允许时）");
		if (is2 && gran === 1) steps.push("HActive 精度 1 像素（RB v2）");
		if (!is2) steps.push("HActive 精度 8 像素（RB v3）：" + h + " → " + hActive);

		var hper = ((1e6 / rateBlank) - minVBlank) / vLines;
		steps.push("H_PERIOD_EST = (10⁶ / " + f(rateBlank) + " − " + minVBlank + ") / " + vLines + " = " + f(hper) + " µs");

		var vbi = Math.ceil(minVBlank / hper);
		steps.push("VBI_LINES = ceil(" + minVBlank + " / " + f(hper) + ") = " + vbi);

		var vblank = Math.max(vbi, 1 + 8 + 6);
		if (vblank > vbi) steps.push("  小于最小 VBI（1 + 8 + 6 = 15 行），取 " + vblank);

		var vback;
		if (!is2 && o.earlyV) {
			var est = Math.floor(vbi / 2);
			if (vblank - est - 8 < 1) {
				vback = vblank - 8 - 1;
				steps.push("EARLY_VSYNC：V_BACK = " + vblank + " − 8 − 1 = " + vback + "（保证前肩 ≥ 1）");
			} else {
				vback = est;
				steps.push("EARLY_VSYNC：V_BACK = floor(" + vbi + " / 2) = " + vback);
			}
		} else {
			vback = 6;
		}
		var vsync = 8;
		var vfront = vblank - vback - vsync;
		var vtotal = v + vblank;

		steps.push("TOTAL_V_LINES = " + v + " + " + vblank + " = " + vtotal +
			"（Vfront " + vfront + " / Vsync 8 / Vback " + vback + "）");

		var addH = 0;
		if (!is2) {
			addH = (o.hblank >= 88 && o.hblank <= 200 && o.hblank % 8 === 0) ? o.hblank - 80 : 0;
		}
		var hblank = 80 + addH;
		var htotal = hActive + hblank;
		var hsync = 32;
		var hfront = 8;
		var hback = hblank - 40;

		steps.push("TOTAL_PIXELS = " + hActive + " + " + hblank + " = " + htotal);
		if (addH) steps.push("  HBlank = 80 + 附加 " + addH + "（须为 8 的倍数，最大 120）");

		var step = 0.001;
		var raw = rateClock * vtotal * htotal / 1e6;
		var pclk = is2
			? step * Math.floor(raw / step)
			: step * Math.ceil(raw / step);
		steps.push("PIXEL_FREQ = " + (is2 ? "floor" : "ceil") + "((" + f(rateClock) + " × " + vtotal + " × " +
			htotal + " / 10⁶) / 0.001) × 0.001 = " + f(pclk) + " MHz");
		steps.push("H_FRONT = 8，H_SYNC = 32，H_BACK = " + hback + "（Hblank − 40）");

		var hfreq = pclk * 1000 / htotal;
		var vfreq = hfreq * 1000 / vtotal;

		return {
			mode: mode,
			hActive: hActive, hfront: hfront, hsync: hsync, hback: hback, hblank: hblank, htotal: htotal,
			vActive: v, vfront: vfront, vsync: vsync, vback: vback, vblank: vblank, vtotal: vtotal,
			pclk: pclk, hfreq: hfreq, vfreq: vfreq,
			hpol: "P", vpol: "N", vsyncWidth: vsync, nominal: rateBlank, mult: mult, rate: rate,
			steps: steps
		};
	}

	/* CVT 1.2: standard CRT-based and RB v1 */
	function computeLegacy(o, f, steps) {
		var h = Math.max(1, Math.floor(o.h));
		var v = Math.max(1, Math.floor(o.v));
		var rate = o.rate;
		var mode = o.mode;
		var vsyncWidth = VSYNC_BY_AR[o.ar] || 5;
		var CELL = CELL_GRAN;
		var hActive = Math.floor(h / CELL) * CELL;
		var htotal, hblank, hfront, hsync, hback;
		var vtotal, vblank, vfront, vsync, vback;
		var pclk, hfreq, vfreq, hpol, vpol;

		if (mode === "crt") {
			var MIN_VSYNC_BP = 550, MIN_V_PORCH = 3, MIN_VBPORCH = 6;
			var C_PRIME = 30, M_PRIME = 300;

			var hperiod = ((1 / rate) - MIN_VSYNC_BP / 1e6) / (v + MIN_V_PORCH) * 1e6;
			steps.push("H_PERIOD_EST = ((1 / " + f(rate) + ") − 550 µs) / (" + v + " + 3) = " + f(hperiod) + " µs");

			var vsbp = Math.floor(MIN_VSYNC_BP / hperiod) + 1;
			steps.push("V_SYNC_BP = floor(550 / " + f(hperiod) + ") + 1 = " + vsbp);
			if (vsbp < vsyncWidth + MIN_VBPORCH) {
				vsbp = vsyncWidth + MIN_VBPORCH;
				steps.push("  小于 Vsync(" + vsyncWidth + ") + 最小后肩(6)，取 " + vsbp);
			}
			vsync = vsyncWidth;
			vback = vsbp - vsync;
			vfront = MIN_V_PORCH;
			vblank = vfront + vsync + vback;
			vtotal = v + vblank;
			steps.push("V_BACK = " + vsbp + " − " + vsync + " = " + vback + "，V_FRONT = 3，TOTAL_V_LINES = " + v + " + " + vblank + " = " + vtotal);

			var duty = C_PRIME - (M_PRIME * hperiod / 1000);
			steps.push("IDEAL_DUTY_CYCLE = 30 − 300 × " + f(hperiod) + " / 1000 = " + f(duty, 2) + " %");
			if (duty < 20) {
				duty = 20;
				steps.push("  低于 20%，按 20% 计");
			}
			hblank = Math.floor(hActive * duty / (100 - duty) / (2 * CELL)) * 2 * CELL;
			steps.push("H_BLANK = floor(" + hActive + " × " + f(duty, 2) + " / (100 − " + f(duty, 2) + ") / 16) × 16 = " + hblank);
			htotal = hActive + hblank;
			steps.push("TOTAL_PIXELS = " + hActive + " + " + hblank + " = " + htotal);

			hsync = Math.floor((htotal * 0.08) / CELL) * CELL;
			hback = hblank / 2;
			hfront = hblank - hback - hsync;
			pclk = 0.25 * Math.floor((htotal / hperiod) / 0.25);
			steps.push("PIXEL_FREQ = floor((" + htotal + " / " + f(hperiod) + ") / 0.25) × 0.25 = " + f(pclk) + " MHz");
			steps.push("H_SYNC = floor(" + htotal + " × 8% / 8) × 8 = " + hsync + "，H_BACK = " + hback + "，H_FRONT = " + hfront);
			hpol = "N";
			vpol = "P";
		} else {
			var MIN_V_BLANK = 460, step = 0.25, v_sync = vsyncWidth;
			var hper = ((1e6 / rate) - MIN_V_BLANK) / v;
			steps.push("H_PERIOD_EST = (10⁶ / " + f(rate) + " − 460) / " + v + " = " + f(hper) + " µs");
			var vbi = Math.floor(MIN_V_BLANK / hper) + 1;
			steps.push("VBI_LINES = floor(460 / " + f(hper) + ") + 1 = " + vbi);
			var minVbi = 3 + v_sync + 6;
			if (vbi < minVbi) {
				vbi = minVbi;
				steps.push("  小于最小 VBI（" + minVbi + " 行），取 " + vbi);
			}
			vblank = vbi;
			vtotal = v + vblank;
			vsync = v_sync;
			vfront = 3;
			vback = vblank - vsync - vfront;
			steps.push("TOTAL_V_LINES = " + v + " + " + vblank + " = " + vtotal + "（Vfront 3 / Vsync " + vsync + " / Vback " + vback + "）");

			hblank = 160;
			htotal = hActive + hblank;
			hsync = 32;
			hback = 80;
			hfront = 48;
			steps.push("TOTAL_PIXELS = " + hActive + " + 160 = " + htotal);
			pclk = step * Math.floor((rate * vtotal * htotal / 1e6) / step);
			steps.push("PIXEL_FREQ = floor((" + f(rate) + " × " + vtotal + " × " + htotal + " / 10⁶) / 0.25) × 0.25 = " + f(pclk) + " MHz");
			steps.push("H_SYNC = 32，H_BACK = 80，H_FRONT = 48");
			hpol = "P";
			vpol = "N";
		}

		hfreq = pclk * 1000 / htotal;
		vfreq = hfreq * 1000 / vtotal;

		return {
			mode: mode,
			hActive: hActive, hfront: hfront, hsync: hsync, hback: hback, hblank: hblank, htotal: htotal,
			vActive: v, vfront: vfront, vsync: vsync, vback: vback, vblank: vblank, vtotal: vtotal,
			pclk: pclk, hfreq: hfreq, vfreq: vfreq,
			hpol: hpol, vpol: vpol, vsyncWidth: vsync, nominal: rate, mult: 1, rate: rate,
			steps: steps
		};
	}
	global.CVTCompute = compute;

	if (typeof document === "undefined") return;

	/* ---------- rendering ---------- */

	var COLORS = {
		active: "rgba(76, 175, 80, 0.35)",
		sync: "rgba(239, 83, 80, 0.35)",
		blank: "rgba(33, 150, 243, 0.22)"
	};
	var X0 = 120, X1 = 930, W = X1 - X0;

	function esc(s) {
		return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
	}

	function r2(n) {
		return Math.round(n * 100) / 100;
	}

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

	function ticks(segs, total, y0, y1) {
		var out = [], acc = 0, i, x;
		for (i = 0; i < segs.length - 1; i++) {
			acc += segs[i].w;
			x = X0 + (acc / total) * W;
			out.push('<line x1="' + r2(x) + '" y1="' + y0 + '" x2="' + r2(x) + '" y2="' + y1 +
				'" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="3 3"></line>');
		}
		return out.join("\n");
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

	function legend(items, y) {
		var out = [], x = X0, i, it, label;
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

	function panel(cfg) {
		var out = [];
		out.push('<text x="' + X0 + '" y="' + cfg.titleY + '" font-size="12" fill="currentColor" opacity="0.85">' +
			esc(cfg.title) + "</text>");
		out.push(ticks(cfg.segs, cfg.total, cfg.syncHigh - 4, cfg.bandY1 + 2));
		out.push('<text x="106" y="' + (cfg.syncHigh + 11) + '" font-size="11" text-anchor="end" fill="currentColor">' +
			esc(cfg.syncName) + "</text>");
		out.push('<path d="' + stepPath(cfg.segs, cfg.total, cfg.syncHigh, cfg.syncLow, "sync", cfg.pol) +
			'" fill="none" stroke="currentColor" stroke-width="1.6"></path>');
		out.push('<text x="106" y="' + (cfg.dataHigh + 11) + '" font-size="11" text-anchor="end" fill="currentColor">DE</text>');
		out.push('<path d="' + stepPath(cfg.segs, cfg.total, cfg.dataHigh, cfg.dataLow, "data", cfg.pol) +
			'" fill="none" stroke="currentColor" stroke-width="1.6"></path>');
		out.push(band(cfg.segs, cfg.total, cfg.bandY0, cfg.bandY1));
		out.push('<text x="' + X1 + '" y="' + (cfg.bandY1 + 16) + '" font-size="11" text-anchor="end" fill="currentColor" opacity="0.8">' +
			esc(cfg.totalLabel) + "</text>");
		out.push(legend(cfg.legendItems, cfg.legendY));
		return out.join("\n");
	}

	function fmt(n, d) {
		return n.toFixed(d === undefined ? 3 : d);
	}

	function render(t) {
		var hSegs = [
			{ kind: "blank", w: t.hfront },
			{ kind: "sync", w: t.hsync },
			{ kind: "blank", w: t.hback },
			{ kind: "active", w: t.hActive }
		];
		var vSegs = [
			{ kind: "blank", w: t.vfront },
			{ kind: "sync", w: t.vsync },
			{ kind: "blank", w: t.vback },
			{ kind: "active", w: t.vActive }
		];

		var modeName = t.mode === "crt" ? "CVT" : t.mode === "rb" ? "CVT-RB v1" : t.mode === "rb2" ? "CVT-RB v2" : "CVT-RB v3";
		var info = document.getElementById("cvt-info");
		if (info) {
			info.textContent = modeName + " · " + t.hActive + "×" + t.vActive + "@" + fmt(t.rate, 3) + " Hz" +
				" · 极性 " + t.hpol + "/" + t.vpol + " · 像素时钟 " + fmt(t.pclk, 3) + " MHz" +
				" · 实际 " + fmt(t.vfreq, 3) + " Hz";
		}

		var vals = document.getElementById("cvt-values");
		if (vals) {
			vals.innerHTML =
				"<div>H：Hactive " + t.hActive + " · Hfront " + t.hfront + " · Hsync " + t.hsync +
				" · Hback " + t.hback + " · Hblank " + t.hblank + " · Htotal " + t.htotal + "</div>" +
				"<div>V：Vactive " + t.vActive + " · Vfront " + t.vfront + " · Vsync " + t.vsync +
				" · Vback " + t.vback + " · Vblank " + t.vblank + " · Vtotal " + t.vtotal + "</div>" +
				"<div>像素时钟 " + fmt(t.pclk, 3) + " MHz · 行频 " + fmt(t.hfreq, 3) + " kHz · 场频 " + fmt(t.vfreq, 3) + " Hz</div>" +
				"<div>数据速率 " + fmt(t.gbps, 2) + " Gbit/s（" + t.bpc + " bpc " +
				(t.chroma === "444" ? "4:4:4" : t.chroma === "422" ? "4:2:2" : "4:2:0") + "）</div>";
		}

		var stepsEl = document.getElementById("cvt-steps");
		if (stepsEl && t.steps) {
			stepsEl.innerHTML = "<ol>" + t.steps.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol>";
		}

		var parts = [];
		parts.push('<svg viewBox="0 0 960 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">');
		parts.push(panel({
			title: "行时序（一个行周期）",
			titleY: 18,
			syncName: "HSYNC (" + t.hpol + ")",
			pol: t.hpol,
			segs: hSegs, total: t.htotal,
			syncHigh: 38, syncLow: 62, dataHigh: 82, dataLow: 106,
			bandY0: 118, bandY1: 138,
			totalLabel: "Htotal " + t.htotal,
			legendItems: [
				{ kind: "blank", label: "Hfront", value: t.hfront },
				{ kind: "sync", label: "Hsync", value: t.hsync },
				{ kind: "blank", label: "Hback", value: t.hback },
				{ kind: "active", label: "Hactive", value: t.hActive }
			],
			legendY: 162
		}));
		parts.push(panel({
			title: "场时序（一个帧周期）",
			titleY: 218,
			syncName: "VSYNC (" + t.vpol + ")",
			pol: t.vpol,
			segs: vSegs, total: t.vtotal,
			syncHigh: 238, syncLow: 262, dataHigh: 282, dataLow: 306,
			bandY0: 318, bandY1: 338,
			totalLabel: "Vtotal " + t.vtotal,
			legendItems: [
				{ kind: "blank", label: "Vfront", value: t.vfront },
				{ kind: "sync", label: "Vsync", value: t.vsync },
				{ kind: "blank", label: "Vback", value: t.vback },
				{ kind: "active", label: "Vactive", value: t.vActive }
			],
			legendY: 362
		}));
		parts.push("</svg>");

		var target = document.getElementById("cvt-svg");
		if (target) target.innerHTML = parts.join("\n");
	}

	function init() {
		var root = document.getElementById("cvt-calc");
		if (!root) return;
		if (root.getAttribute("data-ready") === "1") return;
		root.setAttribute("data-ready", "1");

		var hi = document.getElementById("cvt-h");
		var vi = document.getElementById("cvt-v");
		var ri = document.getElementById("cvt-rate");
		var mi = document.getElementById("cvt-mode");
		var ai = document.getElementById("cvt-ar");
		var bi = document.getElementById("cvt-hblank");
		var ei = document.getElementById("cvt-early");
		var dpi = document.getElementById("cvt-bpc");
		var ci = document.getElementById("cvt-chroma");
		var ti = document.getElementById("cvt-altvblank");
		if (!hi || !vi || !ri || !mi || !ai || !bi || !ei || !dpi || !ci || !ti) return;

		// allow ?h=2560&v=1440&rate=60&mode=rb2&ar=16:9
		if (typeof URLSearchParams !== "undefined") {
			var q = new URLSearchParams(window.location.search);
			if (q.get("h")) hi.value = q.get("h");
			if (q.get("v")) vi.value = q.get("v");
			if (q.get("rate")) ri.value = q.get("rate");
			if (q.get("mode")) mi.value = q.get("mode");
			if (q.get("ar")) ai.value = q.get("ar");
			if (q.get("hblank")) bi.value = q.get("hblank");
			if (q.get("early")) ei.checked = q.get("early") === "1";
			if (q.get("alt")) ti.checked = q.get("alt") === "1";
		}

		function update() {
			var h = parseInt(hi.value, 10);
			var v = parseInt(vi.value, 10);
			var r = parseFloat(ri.value);
			if (!isFinite(h) || h < 8 || !isFinite(v) || v < 1 || !isFinite(r) || r <= 0) {
				var bad = document.getElementById("cvt-info");
				if (bad) bad.textContent = "输入无效";
				return;
			}
			var rb3 = mi.value === "rb3";
			var rb = mi.value === "rb2" || rb3;
			ai.disabled = rb;
			bi.disabled = !rb3;
			ei.disabled = !rb3;
			ti.disabled = !rb;
			var bpc = parseInt(dpi.value, 10) || 8;
			var chroma = ci.value;
			var chromaFactor = chroma === "422" ? 2 : chroma === "420" ? 1.5 : 3;
			var t = compute({
				h: h, v: v, rate: r, mode: mi.value, ar: ai.value,
				hblank: parseInt(bi.value, 10) || 80,
				earlyV: ei.checked,
				altVblank: ti.checked
			});
			if (!t || !isFinite(t.pclk) || t.pclk <= 0 || !isFinite(t.vtotal) || t.vtotal <= 0) {
				var err = document.getElementById("cvt-info");
				if (err) err.textContent = "输入无效";
				return;
			}
			if (t) {
				t.bpc = bpc;
				t.chroma = chroma;
				t.gbps = t.pclk * bpc * chromaFactor / 1000;
			}
			render(t);
		}

		[hi, vi, ri, mi, ai, bi, ei, dpi, ci, ti].forEach(function (el) {
			el.addEventListener("input", update);
			el.addEventListener("change", update);
		});
		update();
	}

	if (window.document$ && typeof window.document$.subscribe === "function") {
		window.document$.subscribe(init);
	} else if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", init);
	} else {
		init();
	}
})(typeof window !== "undefined" ? window : globalThis);
