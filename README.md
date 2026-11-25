# Wednesday 25 November 2026 — The World in One Page

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/keep0626/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/keep0626/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One 1024×1024 image summing up Wednesday 25 November 2026's world news:
32 stories across 7 regions, drawn as a newspaper front page.

## The day

- **First Pakistani in orbit** — Shenzhou-24 lifts off from Jiuquan with
  Zeeshan Ali aboard, the first foreign astronaut on China's Tiangong station.
- **Asia's chip stocks plunge** — the Kospi falls 5.3%, Taiwan 5.1% and the
  Nikkei 2.9% as reports emerge of a fresh US tariff probe.
- **The Houthis threaten Jeddah** — every Saudi Red Sea port is declared a
  target, and Saudi-led jets strike Hodeidah, Saada and Amran.

Below the three leads: six picture cards (Zelenskyy confirming the sinking
of a Russian ship off Libya, the graft probe into Shanghai's Chen Jining,
Huawei's conviction in New York, Giuliani's Medal of Freedom, the CIA
cyber breach, the Odesa strike), then 23 numbered one-line briefs beside a
world map with numbered pins, and a red DATE CHECK box naming what was left
out as other days' news (the COP31 collapse of 22 Nov, GTA 6's release of
19 Nov, Huang's return to Nvidia of 23 Nov, England's T20 win of 24 Nov)
and what had not happened yet.

## How it is made

`render.py` reads `stories.json` and draws `entry.png` with Pillow
(1024×1024, deterministic — no randomness, no clock). `main.py` is the
competition entry point: standard library only, it copies the shipped
`entry.png` to the output directory, so both runs are byte-identical.

Every story was checked against a source dated 25 November 2026; see
`SOURCES.md` for the source of each of the 32 stories. Stories that
happened on another day — however big — were left out and are named in
the image's DATE CHECK box.

## Files

- `main.py` — entry point (copies `entry.png` to the output dir)
- `render.py` — draws `entry.png` from `stories.json`
- `stories.json` — the 32 verified stories
- `entry.png` — the finished front page (1024×1024, under 1 MiB)
- `SOURCES.md` — one source per story
- `LICENSE` — MIT

Competition: [news-image-20261125 on make.fun](https://make.fun/bounty/news-image-20261125)
