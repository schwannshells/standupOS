---
name: build-joke-library
description: "Extract individual jokes from a standup comedy recording and save them as separate files in a joke library. Transcribes audio, identifies joke boundaries (setup, punchline, tags), and creates markdown files for each joke. Use when the user says 'add to joke library', 'extract jokes', 'build joke library', 'transcribe my jokes', 'break out my jokes', or mentions splitting a recording into individual jokes."
---

# Build Joke Library

Extract individual jokes from a standup comedy recording and add them to the joke library in `jokes/`.

## Prerequisites Check

Before running, verify the environment is ready:

1. Check `.env` exists at project root with `GEMINI_API_KEY` set. If missing, tell user to get a free key at https://aistudio.google.com/apikey
2. Check if `google-genai` and `python-dotenv` are installed. If not: `pip install -r requirements.txt`

## Workflow

### Step 1: Get the audio file

Ask the user how they want to provide the recording:

- **Local file**: User provides a path to an audio/video file, or points to a file already in `recordings/`
- **Google Drive sync**: Run `python scripts/sync_recordings.py` to pull new recordings from Google Drive. Then list files in `recordings/` and ask user which one to process.

### Step 2: Get recording metadata

Ask the user:
- **Date of recording** (for the filename). Default to today if they don't know.
- **Any context**: venue, open mic, type of set (new material, polished, etc.)

### Step 3: Extract jokes

```bash
python scripts/process_audio.py jokes <path_to_audio_file>
```

This sends the audio to Gemini and returns JSON with:
- `jokes[]`: each joke with title, tags, setup, punchline, callbacks, full_text, timestamps

Capture the JSON output.

### Step 4: Check for duplicates

Before creating files, scan existing files in `jokes/` for similar content. For each extracted joke:

1. Read existing joke files and compare the `full_text` / punchline
2. If a joke is substantially similar to an existing one (same premise and punchline), flag it and ask the user:
   - **Update**: replace the existing file with the new version
   - **Skip**: don't create a file for this joke
   - **New version**: create a new file (useful for tracking how a joke evolves)

### Step 5: Create joke files

Read [references/joke-format.md](references/joke-format.md) for the file format.

For each new joke, create a markdown file in `jokes/` with:
- **Filename**: `YYYY-MM-DD-slug.md` where slug is a short kebab-case version of the title (e.g., `2026-03-09-airplane-food.md`)
- If the filename already exists, append a number: `2026-03-09-airplane-food-2.md`

### Step 6: Summarize

After creating all files, tell the user:
- How many jokes were extracted
- How many were new vs duplicates
- List each joke title and its file path
