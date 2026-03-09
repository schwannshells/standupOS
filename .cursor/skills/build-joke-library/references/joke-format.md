# Joke File Format

Use this format for every joke file in `jokes/`.

---

```markdown
---
title: "Short descriptive title"
date: 2026-03-09
tags: [dating, relationships, observational]
duration_sec: 45
source: "2026-03-09-open-mic.m4a"
---

# Short Descriptive Title

## Setup

The premise and story leading to the punchline. This is everything the
comedian says to frame the joke before delivering the funny part.

## Punchline

The payoff line that gets the laugh.

## Tags

Additional follow-up lines that get more laughs on the same premise:

- "First tag-back line"
- "Second tag-back line"

## Full Text

> Complete verbatim text of the joke from start to finish, including
> setup, punchline, and all tags as one continuous block.
```

## Guidelines

- `title`: short and descriptive, captures the essence of the joke (not the punchline itself)
- `date`: date of the recording, not the date the file was created
- `tags`: 2-5 theme/topic tags in lowercase
- `duration_sec`: approximate duration of the joke in the recording
- `source`: filename of the source recording
- The Full Text section should be the verbatim transcript, useful for performing the joke later
- Keep setup and punchline as clean/tight as possible -- these represent the "essence" of the joke structure
