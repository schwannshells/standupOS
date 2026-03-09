#!/usr/bin/env python3
"""Send audio files to Gemini for standup comedy analysis.

Modes:
  analyze   - Transcribe + detect laughs + find dead zones
  jokes     - Transcribe + identify individual joke boundaries
  transcribe - Plain transcription with timestamps
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_config():
    config_path = PROJECT_ROOT / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.", file=sys.stderr)
        print("Get a free key at https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)


PROMPTS = {
    "analyze": """You are analyzing a standup comedy recording. Do the following:

1. Transcribe the entire audio with timestamps (MM:SS format for start of each segment).
2. Identify EVERY audience reaction: laughter, applause, groans, heckling, or any non-comedian sound. For each reaction note:
   - "start": timestamp in seconds (float)
   - "end": timestamp in seconds (float)  
   - "duration_sec": duration in seconds (float)
   - "type": one of "chuckle", "laugh", "big_laugh", "applause", "groan", "other"
   - "intensity": 1-10 scale (1 = barely audible, 10 = roaring)
3. Identify dead zones: stretches of 20+ seconds of comedian talking with zero audience reaction.

Return valid JSON with this exact structure:
{
  "total_duration_sec": <float>,
  "transcript": [
    {"start": <float>, "end": <float>, "text": "<segment text>"}
  ],
  "reactions": [
    {"start": <float>, "end": <float>, "duration_sec": <float>, "type": "<type>", "intensity": <int>}
  ],
  "dead_zones": [
    {"start": <float>, "end": <float>, "duration_sec": <float>, "text": "<transcript text during this zone>"}
  ]
}

Be thorough - do not miss any audience reactions, even small ones. Timestamps should be as accurate as possible.""",

    "jokes": """You are analyzing a standup comedy recording to extract individual jokes.

1. Transcribe the entire audio.
2. Identify the boundaries of each individual joke or bit. A joke typically includes:
   - A setup (the premise or story leading to the punchline)
   - A punchline (the funny payoff)
   - Optional tags (follow-up lines that get additional laughs on the same premise)
3. Note topic transitions, audience reactions, and natural pauses to determine boundaries.

Return valid JSON with this exact structure:
{
  "source_duration_sec": <float>,
  "jokes": [
    {
      "index": <int>,
      "title": "<short descriptive title for this joke>",
      "tags": ["<theme1>", "<theme2>"],
      "start": <float>,
      "end": <float>,
      "duration_sec": <float>,
      "setup": "<the setup text>",
      "punchline": "<the punchline text>",
      "callbacks": ["<any tag-backs or callback lines>"],
      "full_text": "<complete joke text from setup through all tags>"
    }
  ]
}

Be generous with joke boundaries - it's better to include transition words than to cut off mid-thought.""",

    "transcribe": """Transcribe this audio recording with timestamps.

Return valid JSON with this exact structure:
{
  "total_duration_sec": <float>,
  "transcript": [
    {"start": <float>, "end": <float>, "text": "<segment text>"}
  ]
}

Transcribe every word accurately. Use natural sentence/phrase boundaries for segments.""",
}


def process(audio_path: str, mode: str):
    if mode not in PROMPTS:
        print(f"Error: Unknown mode '{mode}'. Use: analyze, jokes, transcribe", file=sys.stderr)
        sys.exit(1)

    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"Error: File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    config = get_config()
    model = config.get("gemini_model", "gemini-2.5-flash")
    client = get_client()

    print(f"Uploading {audio_file.name}...", file=sys.stderr)
    uploaded = client.files.upload(file=str(audio_file))

    print(f"Processing with {model} (mode: {mode})...", file=sys.stderr)
    response = client.models.generate_content(
        model=model,
        contents=[PROMPTS[mode], uploaded],
        config={
            "response_mime_type": "application/json",
        },
    )

    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        print("Warning: Response was not valid JSON, returning raw text.", file=sys.stderr)
        print(response.text)
        return

    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Process standup comedy audio with Gemini")
    parser.add_argument("mode", choices=["analyze", "jokes", "transcribe"],
                        help="Processing mode")
    parser.add_argument("audio_file", help="Path to audio/video file")
    args = parser.parse_args()
    process(args.audio_file, args.mode)


if __name__ == "__main__":
    main()
