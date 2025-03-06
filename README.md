# Event to Google Calendar URL Generator

A simple tool that uses Claude to parse event information and generate Google Calendar invitation URLs.

## What it does

This script takes event information (from text, clipboard, or a file), parses it using Claude, and generates a shareable Google Calendar URL. When someone clicks this URL, a pre-filled calendar event opens with all the extracted information.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/event-to-gcal-generator.git
   cd event-to-gcal-generator
   ```

2. Install required packages:
   ```
   pip install anthropic pyperclip
   ```

3. Set your Anthropic API key as an environment variable:
   ```
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

Run the script in one of these ways:

```
# Parse text from clipboard
python event_to_gcal.py

# Parse text from a file
python event_to_gcal.py event_info.txt

# Parse directly provided text
python event_to_gcal.py "Cinnamon Rools, Thursday Mar 6 at 7:00pm, 123 Event St San Francisco, CA"
```

The script will:
1. Extract event details (title, date, time, location, description)
2. Generate a Google Calendar URL
3. Print the URL and copy it to your clipboard
4. Automatically open the URL in your default web browser

## Example

Input:
```
Cinnamon Rools
Thursday, Mar 6
7:00pm
Hosted by M
123 Event St
San Francisco, CA
Hi! we're gonna do at least three things:
1. make cinnamon rools
2. eat cinnamon rools
3. secret activity! (don't eat too many cinnamon rools before this!)
```

Output:
```
Extracted Event Information:
title: Cinnamon Rools
date: 2025-03-06
start_time: 19:00
location: 123 Event St, San Francisco, CA
description: Hi! we're gonna do at least three things:
1. make cinnamon rools
2. eat cinnamon rools
3. secret activity! (don't eat too many cinnamon rools before this!)

Google Calendar URL:
https://calendar.google.com/calendar/u/0/r/eventedit?text=Cinnamon%20Rools&dates=20250306T190000/20250306T200000&details=Hi%21%20we%27re%20gonna%20do%20at%20least%20three%20things%3A%0A1.%20make%20cinnamon%20rools%0A2.%20eat%20cinnamon%20rools%0A3.%20secret%20activity%21%20%28don%27t%20eat%20too%20many%20cinnamon%20rools%20before%20this%21%29&location=123%20Event%20St%2C%20San%20Francisco%2C%20CA

URL copied to clipboard!
Opening URL in web browser...
```

## Requirements

- Python 3.6+
- Anthropic API key (Claude API access)
- `anthropic` Python package
- `pyperclip` Python package