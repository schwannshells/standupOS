---
name: analyze-set
description: "Analyze a standup comedy set recording for audience reactions, laugh metrics, and dead zones. Transcribes audio, detects laughs (with intensity and duration), finds stretches without laughs, and generates a performance report. Use when the user says 'analyze set', 'analyze my recording', 'how did my set go', 'check my set', or mentions analyzing a standup performance, open mic, or comedy show recording."
---

# Analyze Standup Set

Analyze a recorded standup comedy set to produce a performance report with laugh metrics, audience reaction timeline, and dead zone analysis.

## Prerequisites Check

Before running, verify the environment is ready:

1. Check `.env` exists at project root with `GEMINI_API_KEY` set. If missing, tell user to get a free key at https://aistudio.google.com/apikey
2. Check if `google-genai` and `python-dotenv` are installed. If not: `pip install -r requirements.txt`

## Workflow

### Step 1: Get the audio file

Ask the user how they want to provide the recording:

- **Local file**: User provides a path to an audio/video file (`.m4a`, `.mp3`, `.wav`, `.mp4`, `.webm`, `.mov`), or points to a file already in `recordings/`
- **Google Drive sync**: Run `python scripts/sync_recordings.py` to pull new recordings from Google Drive Recorder folder. Then list files in `recordings/` and ask user which one to analyze.

### Step 2: Determine recording type

Ask: "Is this a live performance (with audience) or solo practice?"

- **Live performance**: proceed with full analysis (Step 3)
- **Solo practice**: skip to Step 5 (transcript-only analysis)

### Step 3: Run analysis

```bash
python scripts/process_audio.py analyze <path_to_audio_file>
```

This sends the audio to Gemini and returns JSON to stdout with:
- `transcript`: timestamped segments
- `reactions`: every audience reaction with type, duration, intensity (1-10)
- `dead_zones`: stretches of 20+ seconds without audience reaction

Capture the JSON output.

### Step 4: Generate the report

Read [references/report-template.md](references/report-template.md) for the report format.

Using the JSON output, create a markdown report at `reports/YYYY-MM-DD-<venue-or-description>.md`. Ask the user for the venue/event name if not obvious from context.

The report must include:
- **Summary stats**: total set time, total laugh time, laughs-per-minute, average intensity
- **Full transcript with inline markers**: insert `[LAUGH 2.3s intensity:7]` or `[APPLAUSE 1.5s]` at the appropriate positions in the transcript
- **Reaction timeline**: list every reaction chronologically with timestamp, type, duration, intensity
- **Dead zones**: table of every 20+ second stretch without reactions, including the transcript text spoken during that stretch and word count
- **Tightening suggestions**: for each dead zone, highlight which words/phrases could potentially be cut or tightened to get to the next laugh faster

Skip to Step 6.

### Step 5: Solo practice analysis

For practice recordings without an audience:

```bash
python scripts/process_audio.py transcribe <path_to_audio_file>
```

Generate a simplified report with:
- Full transcript with timestamps
- Word count per segment
- Total duration and words-per-minute
- Highlight any segments where the pace slows significantly

### Step 6: Present findings

After saving the report, give the user a brief verbal summary:
- Total set time and total laugh time
- Best moment (highest intensity reaction)
- Worst dead zone (longest stretch without laughs)
- Top 2-3 suggestions for tightening
