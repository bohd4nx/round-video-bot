<div align="center">
  <img src="" alt="round-video-bot" width="96" height="96" style="border-radius: 20px;"><br><br>

# round-video-bot

[![Stars](https://img.shields.io/github/stars/bohd4nx/Telegram-Video-Bot?style=flat&color=blue&label=Stars)](https://github.com/bohd4nx/Telegram-Video-Bot/stargazers)
[![Forks](https://img.shields.io/github/forks/bohd4nx/Telegram-Video-Bot?style=flat&color=blue&label=Forks)](https://github.com/bohd4nx/Telegram-Video-Bot/forks)
[![Telegram](https://img.shields.io/badge/demo-@RoundMsgBot-blue?style=flat&logo=telegram)](https://t.me/RoundMsgBot)

Telegram bot that converts videos into **round video notes**.

**[Try Demo](https://t.me/RoundMsgBot)** · **[Report Bug](https://github.com/bohd4nx/Telegram-Video-Bot/issues)**

</div>

---

## Features

- Converts any video into a round note
- iOS and Android overlay styles — user picks per video
- Videos longer than 60 s are auto-split into sequential notes
- Russian and English, auto-detected from Telegram locale
- PostgreSQL-backed user and download history

---

## Quick Start

**Requires:** Python 3.10+, ffmpeg, PostgreSQL

```bash
git clone https://github.com/bohd4nx/Telegram-Video-Bot.git
cd Telegram-Video-Bot
cp .env.example .env   # fill in BOT_TOKEN, POSTGRES_*
```

```bash
# Docker (recommended)
docker compose up -d

# or local
pip install .
python main.py
```
