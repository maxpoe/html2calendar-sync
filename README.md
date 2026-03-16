# THWS Calendar Sync

This repository contains a script to automatically scrape the THWS schedule (specifically `BMG WiSe 24-25 4 BMG 4. Sem. SoSe 26`) and convert it into a subscribable iCalendar (`.ics`) file.

The script runs nightly via GitHub Actions to ensure the calendar is always up to date.

## Subscribe to the Calendar

To add this schedule to your Apple Calendar (or any other calendar app that supports `.ics` subscriptions):

1. **Copy the link to the generated `.ics` file**:
   Navigate to `schedule.ics` in this repository, click **Raw**, and copy the resulting URL.
   *(Once you push this to your repository, it will look something like `https://raw.githubusercontent.com/username/thws-calendar-sync/main/schedule.ics`)*

2. **Add to Apple Calendar**:
   - Open the **Calendar** app on your Mac or iPhone.
   - Go to **File** > **New Calendar Subscription...**
   - Paste the copied Raw URL.
   - Click **Subscribe**.
   - You can choose the auto-refresh interval (e.g., Every day).

## Development

To run the script locally:
```bash
pip install -r requirements.txt
python sync.py
```
