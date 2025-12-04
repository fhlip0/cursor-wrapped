# Cursor Wrapped 2025

A Spotify Wrapped-style summary of your Cursor usage for the year.

## Files

- `usage-events-2025-12-04.csv` - Your Cursor usage data export
- `cursor_wrapped.py` - Python script that analyzes the CSV and generates statistics
- `cursor_wrapped_summary.json` - Generated JSON summary with all statistics
- `cursor_wrapped_terminal.py` - Terminal script that displays a formatted ASCII summary

## Getting Your Data

To export your Cursor usage data:

1. Go to [https://cursor.com/dashboard?tab=usage](https://cursor.com/dashboard?tab=usage)
2. Set your date range (e.g., the full year)
3. Click the export button to download your CSV file
4. Save the CSV file in this directory (or update the filename in the script)

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

### View Terminal Summary

Display a beautifully formatted ASCII summary in your terminal:

```bash
python3 cursor_wrapped_terminal.py
```

The terminal summary displays:

- Total activity and tokens processed
- Daily averages and statistics
- Total cost breakdown
- Top 5 models used
- Peak coding hours, days, and weekdays
- Cache efficiency metrics

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

1. Go to [https://cursor.com/dashboard?tab=usage](https://cursor.com/dashboard?tab=usage)
2. Set your date range and export a new CSV
3. Replace `usage-events-2025-12-04.csv` (or update the filename in the script)
4. Run `python3 cursor_wrapped.py` again to regenerate the JSON
5. Run `python3 cursor_wrapped_terminal.py` to view the updated summary

