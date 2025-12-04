# Cursor Wrapped 2025

A Spotify Wrapped-style summary of your Cursor usage for the year.

## Files

- `usage-events-2025-12-04.csv` - Your Cursor usage data export
- `cursor_wrapped.py` - Python script that analyzes the CSV and generates statistics
- `cursor_wrapped_summary.json` - Generated JSON summary with all statistics
- `cursor_wrapped.html` - Interactive web visualization (Spotify Wrapped style)

## Usage

### Generate Summary

Run the Python script to analyze your usage data:

```bash
python3 cursor_wrapped.py
```

This will:
1. Parse the CSV file
2. Calculate statistics (totals, models, peak times, cache efficiency, etc.)
3. Print a text summary to the console
4. Generate `cursor_wrapped_summary.json` with all the data

### View Interactive Visualization

Open `cursor_wrapped.html` in your web browser:

```bash
open cursor_wrapped.html
```

The HTML file will automatically load data from `cursor_wrapped_summary.json` and display an interactive slideshow with:

- Total activity and tokens processed
- Daily averages
- Total cost
- Top models used
- Peak coding hours
- Most productive days
- Cache efficiency metrics
- Token statistics

### Navigation

- **Auto-advance**: Slides automatically advance every 5 seconds
- **Keyboard**: Use arrow keys (← → ↑ ↓) to navigate
- **Dots**: Click the navigation dots at the bottom to jump to any slide

## Statistics Included

- **Total Activity**: Number of requests and total tokens processed
- **Daily Averages**: Tokens per day and days active
- **Cost Analysis**: Total cost breakdown
- **Model Usage**: Top models by usage count and token consumption
- **Peak Times**: Most productive hours, days, and weekdays
- **Cache Efficiency**: Cache hit rate and tokens saved
- **Token Statistics**: Average, median, and maximum tokens per request

## Regenerating

To regenerate the summary with updated data:

1. Export a new CSV from Cursor
2. Replace `usage-events-2025-12-04.csv` (or update the filename in the script)
3. Run `python3 cursor_wrapped.py` again
4. Refresh the HTML page

