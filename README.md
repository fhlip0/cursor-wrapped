# Cursor Wrapped 2025

A Spotify Wrapped-style summary of your Cursor usage for the year.

## Getting Your Data

To export your Cursor usage data:

1. Go to [https://cursor.com/dashboard?tab=usage](https://cursor.com/dashboard?tab=usage)
2. Set your date range (e.g., the full year)
3. Click the export button to download your CSV file

## Usage

Simply run the script with your CSV file:

```bash
python3 cursor_wrapped_terminal.py usage-events-2025-12-04.csv
```

The script will:
1. Parse the CSV file
2. Calculate statistics (totals, models, peak times, cache efficiency, etc.)
3. Display a beautifully formatted ASCII summary in your terminal

### Optional: Save JSON Summary

To also save the summary data as JSON:

```bash
python3 cursor_wrapped_terminal.py usage-events-2025-12-04.csv --json summary.json
```

## Statistics Included

- **Total Activity**: Number of requests and total tokens processed
- **Daily Averages**: Tokens per day and days active
- **Cost Analysis**: Total cost breakdown
- **Model Usage**: Top models by usage count and token consumption
- **Peak Times**: Most productive hours, days, and weekdays
- **Cache Efficiency**: Cache hit rate and tokens saved
- **Token Statistics**: Average, median, and maximum tokens per request

## Example Output

The terminal summary displays:

- Total activity and tokens processed
- Daily averages and statistics
- Total cost breakdown
- Top 5 models used
- Peak coding hours, days, and weekdays
- Cache efficiency metrics

## Regenerating

To regenerate the summary with updated data:

1. Go to [https://cursor.com/dashboard?tab=usage](https://cursor.com/dashboard?tab=usage)
2. Set your date range and export a new CSV
3. Run `python3 cursor_wrapped_terminal.py your-new-file.csv`
