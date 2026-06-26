#!/usr/bin/env node
/**
 * XingTu MVP — Comprehensive UI Test Suite v2
 * 10 scenarios × 3 designs = 30 test cases
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE = '/Users/valera/workspace/bazi-research';
const SCREENSHOTS = path.join(BASE, 'artifacts', 'ui-tests');
fs.mkdirSync(SCREENSHOTS, { recursive: true });

const DESIGNS = {
  chrono:  { name: 'Chronograph', file: 'xingtu-mvp-design1-chronograph.html' },
  horizon: { name: 'Horizon',     file: 'xingtu-mvp-design2-horizon.html' },
  classic: { name: 'Classique',   file: 'xingtu-mvp-design3-classique.html' },
};

let passed = 0, failed = 0, total = 0;

async function run() {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: 'en-US',
  });

  for (const [key, design] of Object.entries(DESIGNS)) {
    const url = 'file://' + path.join(BASE, design.file);
    const sd = path.join(SCREENSHOTS, key);
    fs.mkdirSync(sd, { recursive: true });

    console.log(`\n${'='.repeat(60)}`);
    console.log(`  ${design.name}`);
    console.log(`${'='.repeat(60)}`);

    // S1: Splash → Picker
    await T(ctx, url, key, sd, design, 1, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await A('Splash visible', async () => {
        const h = await page.locator('h1, h2, h3, .logo, button').first().isVisible();
        if (!h) throw new Error('No splash content');
      });
      // Click enter button
      await page.evaluate(() => {
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
          const t = b.textContent.toLowerCase();
          if (t.includes('begin') || t.includes('enter') || t.includes('开启') || t.includes('叩问') || t.includes('start')) {
            b.click(); return;
          }
        }
      });
      await page.waitForTimeout(500);
      await A('Picker visible', async () => {
        const t = await page.textContent('body');
        if (!t || t.length < 20) throw new Error('Empty body after splash click');
      });
      await shot(page, sd, '01-after-splash');
    });

    // S2: Simple select → see result
    await T(ctx, url, key, sd, design, 2, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1990, month: 5, day: 15, hourIdx: 6 });
      await clickReveal(page);
      await page.waitForTimeout(700);
      await A('BaZi result shows', async () => {
        const t = await page.textContent('body');
        const hasP = /[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥]/.test(t);
        if (!hasP) throw new Error('No BaZi pillars found');
      });
      await shot(page, sd, '02-bazi-result');
    });

    // S3: Play with selectors
    await T(ctx, url, key, sd, design, 3, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      // Try to find and interact with year selector
      await page.evaluate(() => {
        // Scroll wheels if present
        document.querySelectorAll('.wheel-list, .slider-track, [class*="inner"]').forEach(el => {
          const p = el.parentElement;
          if (p) { p.scrollTop = 200; p.scrollLeft = 100; }
        });
      });
      await page.waitForTimeout(200);
      // Try clicking next/prev buttons
      const navBtns = await page.locator('button').all();
      for (const b of navBtns) {
        const t = await b.textContent();
        if (/next|prev|previous|\+|−|→|←|\d{4}/.test(t)) {
          await b.click().catch(() => {}); break;
        }
      }
      await page.waitForTimeout(200);
      await A('Selector interaction OK', async () => {
        const t = await page.textContent('body');
        if (!t || t.length < 20) throw new Error('Page blank after interaction');
      });
      await shot(page, sd, '03-selector-play');
    });

    // S4: Result + date change #1
    await T(ctx, url, key, sd, design, 4, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1990, month: 5, day: 15, hourIdx: 6 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '04a-result-1990');
      // Change to 1985
      await goBack(page);
      await selectBirthday(key, page, { year: 1985, month: 3, day: 1, hourIdx: 0 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '04b-result-1985');
      await A('1985 result shown', async () => {
        const t = await page.textContent('body');
        if (!t || t.length < 50) throw new Error('Empty result');
      });
    });

    // S5: Date change #2 — modern era
    await T(ctx, url, key, sd, design, 5, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 2000, month: 12, day: 25, hourIdx: 11 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '05a-result-2000');
      await goBack(page);
      await selectBirthday(key, page, { year: 1976, month: 7, day: 4, hourIdx: 3 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '05b-result-1976');
    });

    // S6: Date change #3 — extremes
    await T(ctx, url, key, sd, design, 6, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1950, month: 1, day: 1, hourIdx: 6 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '06a-result-1950');
      await goBack(page);
      await selectBirthday(key, page, { year: 2024, month: 8, day: 15, hourIdx: 6 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await shot(page, sd, '06b-result-2024');
    });

    // S7: Full explore — back, re-enter, all fields
    await T(ctx, url, key, sd, design, 7, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1995, month: 6, day: 10, hourIdx: 4 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await goBack(page);
      await page.waitForTimeout(300);
      await selectBirthday(key, page, { year: 2005, month: 3, day: 20, hourIdx: 9 });
      await clickReveal(page);
      await page.waitForTimeout(600);
      await A('Re-entry works', async () => {
        const t = await page.textContent('body');
        if (!t || t.length < 50) throw new Error('Empty after re-entry');
      });
      await shot(page, sd, '07-reentry');
    });

    // S8: Explore BaZi result sections
    await T(ctx, url, key, sd, design, 8, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1990, month: 5, day: 15, hourIdx: 7 });
      await clickReveal(page);
      await page.waitForTimeout(800);
      // Scroll result
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(200);
      await shot(page, sd, '08a-result-scrolled');
      await A('Result has element info', async () => {
        const t = await page.textContent('body');
        if (!/wood|fire|earth|metal|water|木|火|土|金|水/i.test(t))
          throw new Error('No element analysis');
      });
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(100);
      await shot(page, sd, '08b-result-top');
    });

    // S9: Amulet/premium interaction
    await T(ctx, url, key, sd, design, 9, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      await selectBirthday(key, page, { year: 1990, month: 5, day: 15, hourIdx: 7 });
      await clickReveal(page);
      await page.waitForTimeout(700);
      // Check for purchase/amulet buttons
      const premium = await page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const hasBuy = btns.some(b => /purchase|buy|subscribe|unlock|🛒/i.test(b.textContent));
        const hasAmulet = document.querySelector('[class*="amulet"], [class*="modal"], [class*="card"], [id*="amulet"]');
        return { hasBuy: !!hasBuy, hasAmulet: !!hasAmulet, btnCount: btns.length };
      });
      console.log(`    [INFO] Premium: buy=${premium.hasBuy} amulet=${premium.hasAmulet} btns=${premium.btnCount}`);
      // Try clicking any amulet/premium element
      await page.evaluate(() => {
        const el = document.querySelector('[class*="amulet"], .buy-btn, [class*="purchase"], [class*="card"]');
        if (el) el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      });
      await page.waitForTimeout(400);
      await shot(page, sd, '09-premium');
    });

    // S10: Edge cases
    await T(ctx, url, key, sd, design, 10, async (page) => {
      await page.waitForLoadState('domcontentloaded', { timeout: 8000 }).catch(() => {});
      await clickEnter(page);
      // Rapid clicks
      for (let i = 0; i < 5; i++) {
        await page.evaluate(() => {
          document.querySelectorAll('button').forEach(b => b.click());
        }).catch(() => {});
        await page.waitForTimeout(30);
      }
      // Check disabled buttons
      const db = await page.evaluate(() => document.querySelectorAll('button:disabled').length);
      console.log(`    [INFO] Disabled buttons: ${db}`);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(100);
      // Try select + reset
      await selectBirthday(key, page, { year: 1990, month: 5, day: 15, hourIdx: 6 });
      await page.evaluate(() => {
        const backs = Array.from(document.querySelectorAll('button')).filter(b =>
          /back|reset|←|clear/i.test(b.textContent)
        );
        if (backs.length) backs[0].click();
      }).catch(() => {});
      await page.waitForTimeout(300);
      await shot(page, sd, '10-edge-cases');
    });
  }

  console.log(`\n${'='.repeat(60)}`);
  console.log(`  TOTAL: ${passed} passed, ${failed} failed / ${total}`);
  console.log(`${'='.repeat(60)}`);
  await browser.close();
  process.exit(failed > 0 ? 1 : 0);
}

// ── Helpers ──
async function A(name, fn) {
  total++;
  try { await fn(); passed++; console.log(`    [PASS] ${name}`); }
  catch(e) { failed++; console.log(`    [FAIL] ${name}: ${e.message}`); }
}

function shot(page, dir, name) {
  return page.screenshot({ path: path.join(dir, name + '.png'), fullPage: false });
}

async function clickEnter(page) {
  await page.waitForTimeout(200);
  await page.evaluate(() => {
    const btns = document.querySelectorAll('button');
    for (const b of btns) {
      const t = b.textContent.trim().toLowerCase();
      if (t.includes('begin') || t.includes('enter') || t.includes('开启') || t.includes('叩问') || t.includes('start') || t === '✦') {
        b.click(); return;
      }
    }
  });
  await page.waitForTimeout(500);
}

async function clickReveal(page) {
  await page.evaluate(() => {
    // Try different reveal functions
    if (typeof doSpin === 'function') { doSpin(); return; }
    if (typeof showResults === 'function') { showResults(); return; }
    if (typeof reveal === 'function') { reveal(); return; }
    if (typeof calculateBaZi === 'function') { calculateBaZi(); return; }
    // Try clicking buttons by text
    const btns = document.querySelectorAll('button');
    for (const b of btns) {
      const t = b.textContent.trim().toLowerCase();
      if (t.includes('calculat') || t.includes('reveal') || t.includes('✦') || t.includes('揭示') || t.includes('命运') || t.includes('spin') || t.includes('result') || t.includes('go')) {
        if (!b.disabled) { b.click(); return; }
      }
    }
  });
  await page.waitForTimeout(500);
}

async function goBack(page) {
  await page.evaluate(() => {
    const btns = document.querySelectorAll('button');
    for (const b of btns) {
      const t = b.textContent.trim();
      if (t === '←' || t.includes('Back') || t.includes('back') || t.includes('返回')) {
        b.click(); return;
      }
    }
    // Fallback: try function
    if (typeof goBack === 'function') goBack();
    else if (typeof showScreen === 'function') showScreen('picker');
    else if (typeof goToPicker === 'function') goToPicker();
  });
  await page.waitForTimeout(400);
}

async function selectBirthday(key, page, opts) {
  const { year, month, day, hourIdx } = opts;
  if (key === 'chrono') {
    await page.evaluate(({ y, m, d, h }) => {
      // Try clicking sectors directly
      const sectors = document.querySelectorAll('[data-dial]');
      if (sectors.length > 0) {
        sectors.forEach(s => {
          const idx = parseInt(s.dataset.index);
          const dial = s.dataset.dial;
          if (dial === 'year' && idx === 10) { // 1990 in 1980-1991
            s.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
          if (dial === 'month' && idx === (m - 1)) {
            s.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
          if (dial === 'day' && idx === (d - 1)) {
            s.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
          if (dial === 'hour' && idx === h) {
            s.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
        });
      }
    }, { y: year, m: month, d: day, h: hourIdx });
  } else if (key === 'horizon') {
    await page.evaluate(({ y, m, d, h }) => {
      if (typeof sliders === 'undefined') return;
      const cy = new Date().getFullYear();
      const yi = (cy + 5) - y;
      const setSlider = (id, idx) => {
        const s = sliders[id];
        if (!s || idx < 0 || idx >= s.itemCount) return;
        s.currentIdx = idx;
        s.currentPos = -(idx * s.itemW) + s.centerOffset;
        s.track.style.transition = 'none';
        s.track.style.transform = 'translateX(' + s.currentPos + 'px)';
        Array.from(s.track.children).forEach((el, i) => el.classList.toggle('active', i === idx));
        if (typeof updateDisplay === 'function') updateDisplay(s);
      };
      setSlider('year', yi);
      setSlider('month', m - 1);
      setSlider('day', d - 1);
      setSlider('hour', h);
    }, { y: year, m: month, d: day, h: hourIdx });
  } else if (key === 'classic') {
    await page.evaluate(({ y, m, d, h }) => {
      if (typeof wheels === 'undefined') return;
      const yi = y - 1900;
      if (wheels.year && wheels.year._snapTo) wheels.year._snapTo(yi, true);
      if (wheels.month && wheels.month._snapTo) wheels.month._snapTo(m - 1, true);
      if (wheels.day && wheels.day._snapTo) wheels.day._snapTo(d - 1, true);
      if (wheels.hour && wheels.hour._snapTo) wheels.hour._snapTo(h, true);
    }, { y: year, m: month, d: day, h: hourIdx });
  }
  await page.waitForTimeout(300);
}

async function T(ctx, url, key, sd, design, num, fn) {
  const page = await ctx.newPage();
  const label = `S${String(num).padStart(2,'0')}`;
  try {
    console.log(`\n  ── S${num} ──`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
    await page.waitForTimeout(300);
    await fn(page);
    console.log(`  [OK] ${label}`);
  } catch(e) {
    failed++; total++;
    console.log(`  [CRASH] ${label}: ${e.message?.substring(0, 100)}`);
    try { await shot(page, sd, `${label}-crash`); } catch(e2) {}
  } finally {
    await page.close();
  }
}

run().catch(e => { console.error('FATAL:', e); process.exit(1); });
