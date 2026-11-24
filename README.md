# news-image-20261124
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/mooohgaming/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/mooohgaming/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

`main.py` draws one newspaper page — "The World in One Page" — summing up
Tuesday 24 November 2026 in a single 1024x1024 PNG. Six stories, each with
a headline, two lines of text, a drawn illustration and a source line:

1. **Russia strikes Zaporizhzhia** — two killed and 22 wounded in an
   overnight attack; a Russian drone also strayed into Poland. (Reuters)
2. **Korea scrambles jets** — Russian military planes near Ulleung Island
   trigger a five-minute air-raid warning; jets are scrambled. (Reuters)
3. **Airstrike kills 3 in Gaza** — an Israeli strike near a police post in
   Khan Younis kills three and wounds five more. (Reuters)
4. **US hits Iran's shadow banks** — the Treasury sanctions two dozen
   Iranian exchange houses and front firms. (US Treasury)
5. **Huang is back at Nvidia** — the board reinstates the AI chip boss
   eleven days after he resigned; shares jump by a third. (Reuters)
6. **Kiwis bat out draw with India** — Mitchell and Phillips hold on at
   Wellington; India stay fourth in the Test title race. (ICC)

The program uses only the Python standard library: it draws the page with its
own canvas code and a built-in 5x7 bitmap font, and encodes the PNG by hand
(zlib + struct). No network, no clock, no randomness — two runs produce
byte-identical output.

## Run it

```sh
python3 main.py
```

That writes `/output/entry.png`. To write elsewhere, set
`MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
