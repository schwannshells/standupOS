# standupOS

Agent skills for standup comedy operations. Drop in a recording of your set and let AI agents transcribe, analyze laughs, find dead zones, and build your joke library.

Powered by Gemini's multimodal audio understanding — no heavy ML stack, no GPU, just two Python packages.

## What It Does

### Analyze a Set

Say **"analyze my set"** and the agent will:

- Transcribe the full recording with timestamps
- Detect every audience reaction (laughs, applause, groans) with intensity ratings (1-10) and duration
- Calculate laughs-per-minute, total laugh time, average intensity
- Find dead zones (20+ seconds without a reaction)
- Suggest where to tighten material to get to the next laugh faster
- Save a detailed report to `reports/`

### Build a Joke Library

Say **"extract jokes"** and the agent will:

- Transcribe the recording
- Identify individual joke boundaries (setup, punchline, tags/callbacks)
- Create a separate markdown file for each joke in `jokes/`
- Check for duplicates against your existing library
- Tag jokes by theme for easy searching

## Setup

### 1. Get a Gemini API Key

Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and create a free API key. The free tier is generous (1500 requests/day on Flash models).

### 2. Configure

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Edit `.env`:

```
GEMINI_API_KEY=your_key_here
```

### 3. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Google Drive Sync (Optional)

If you use Google Recorder and have Google Drive for Desktop installed, update `config.json` with your Recorder folder path:

```json
{
  "gdrive_recorder_path": "~/Library/CloudStorage/GoogleDrive-you@gmail.com/My Drive/Recorder"
}
```

To find your path:

```bash
ls ~/Library/CloudStorage/
```

## Project Structure

```
standupOS/
├── .cursor/skills/
│   ├── analyze-set/            # Set analysis skill
│   └── build-joke-library/     # Joke extraction skill
├── scripts/
│   ├── process_audio.py        # Gemini API wrapper
│   └── sync_recordings.py      # Google Drive sync
├── recordings/                 # Drop audio/video files here
├── jokes/                      # Individual joke files
├── reports/                    # Set analysis reports
├── config.json                 # Google Drive path + model settings
└── requirements.txt            # google-genai, python-dotenv
```

## Scripts

The scripts can also be used standalone outside of the agent skills.

```bash
source .venv/bin/activate

# Analyze a set (transcript + laughs + dead zones)
python scripts/process_audio.py analyze recordings/my-set.m4a

# Extract jokes
python scripts/process_audio.py jokes recordings/my-set.m4a

# Plain transcription
python scripts/process_audio.py transcribe recordings/my-set.m4a

# Sync new recordings from Google Drive
python scripts/sync_recordings.py
```

All commands output JSON to stdout.

## Supported Formats

`.m4a` `.mp3` `.wav` `.mp4` `.webm` `.mov` — anything Gemini can ingest.

## Joke File Format

Each joke is saved as a markdown file in `jokes/`:

```markdown
---
title: "Airplane Food"
date: 2026-03-09
tags: [travel, observational]
duration_sec: 45
source: "2026-03-09-open-mic.m4a"
---

# Airplane Food

## Setup
So I'm on this flight and they hand me a tray...

## Punchline
...and I said, that's not turbulence, that's my stomach.

## Tags
- "The pilot even came back to check on me"

## Full Text
> Complete verbatim text of the joke...
```

## License

MIT
