# PDF2ICS Calendar Sync

This repository contains a script to automatically scrape a hosted PDF schedule and convert it into a subscribable Calendar (`.ics`) file.

The script runs nightly via GitHub Actions to ensure the calendar is always up to date.

## Subscribe to the Calendar

To add this schedule to your Calendar (`.ics` supported):

1. **Copy the link to the generated `.ics` file**:
   Navigate to `schedule.ics` in this repository, click **Raw**, and copy the resulting URL.

2. **Add to Calendar**:
   - Open the **Calendar** app on your device.
   - Go to **File** > **New Calendar Subscription...**
   - Paste the copied Raw URL.
   - Click **Subscribe**.
   - You can choose the auto-refresh interval (e.g., Every day).

## Setup & Configuration

This project requires you to specify the schedule URL as an environment variable to prevent hardcoding PII/Specific links.

1. **GitHub Actions**: Add a Repository Secret named `SCHEDULE_URL` containing the link to the schedule PDF.
2. **Local Development**: Run the script by passing the environment variable:

```bash
pip3 install -r requirements.txt
SCHEDULE_URL="https://fas.thws.de/..." python3 sync.py
```

## License

This project is open-source and available under the MIT License.
