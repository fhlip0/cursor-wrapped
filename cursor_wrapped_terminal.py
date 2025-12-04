#!/usr/bin/env python3
"""
Cursor Wrapped - ASCII Terminal Summary
Accepts a CSV file path as a command-line argument
"""

import csv
import json
import sys
import argparse
from datetime import datetime
from collections import defaultdict
from statistics import mean, median

def parse_csv(filename):
    """Parse the CSV file and return structured data"""
    events = []
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse date
            try:
                date_str = row['Date'].strip('"')
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                continue
            
            # Parse numeric fields
            try:
                input_cache = int(row['Input (w/ Cache Write)']) if row['Input (w/ Cache Write)'] else 0
                input_no_cache = int(row['Input (w/o Cache Write)']) if row['Input (w/o Cache Write)'] else 0
                cache_read = int(row['Cache Read']) if row['Cache Read'] else 0
                output_tokens = int(row['Output Tokens']) if row['Output Tokens'] else 0
                total_tokens = int(row['Total Tokens']) if row['Total Tokens'] else 0
                cost = float(row['Cost']) if row['Cost'] and row['Cost'] != 'NaN' else 0.0
            except:
                continue
            
            events.append({
                'date': date,
                'kind': row['Kind'],
                'model': row['Model'],
                'max_mode': row['Max Mode'],
                'input_cache': input_cache,
                'input_no_cache': input_no_cache,
                'cache_read': cache_read,
                'output_tokens': output_tokens,
                'total_tokens': total_tokens,
                'cost': cost
            })
    
    return events

def analyze_usage(events):
    """Analyze usage patterns and generate statistics"""
    
    # Filter out errored events
    valid_events = [e for e in events if e['kind'] == 'Included' and e['total_tokens'] > 0]
    
    stats = {
        'total_events': len(valid_events),
        'date_range': {
            'start': min(e['date'] for e in valid_events),
            'end': max(e['date'] for e in valid_events)
        },
        'total_tokens': sum(e['total_tokens'] for e in valid_events),
        'total_output_tokens': sum(e['output_tokens'] for e in valid_events),
        'total_input_tokens': sum(e['input_cache'] + e['input_no_cache'] for e in valid_events),
        'total_cache_read': sum(e['cache_read'] for e in valid_events),
        'total_cost': sum(e['cost'] for e in valid_events),
        'model_usage': defaultdict(int),
        'model_tokens': defaultdict(int),
        'model_cost': defaultdict(float),
        'hourly_usage': defaultdict(int),
        'daily_usage': defaultdict(int),
        'monthly_usage': defaultdict(int),
        'weekday_usage': defaultdict(int),
        'token_distribution': [],
        'cache_efficiency': [],
    }
    
    # Analyze each event
    for event in valid_events:
        model = event['model']
        date = event['date']
        
        # Model statistics
        stats['model_usage'][model] += 1
        stats['model_tokens'][model] += event['total_tokens']
        stats['model_cost'][model] += event['cost']
        
        # Time-based statistics
        hour = date.hour
        day = date.date()
        month = date.strftime('%Y-%m')
        weekday = date.strftime('%A')
        
        stats['hourly_usage'][hour] += event['total_tokens']
        stats['daily_usage'][day] += event['total_tokens']
        stats['monthly_usage'][month] += event['total_tokens']
        stats['weekday_usage'][weekday] += event['total_tokens']
        
        # Cache efficiency
        total_input = event['input_cache'] + event['input_no_cache'] + event['cache_read']
        if total_input > 0:
            cache_ratio = event['cache_read'] / total_input
            stats['cache_efficiency'].append(cache_ratio)
        
        # Token distribution
        stats['token_distribution'].append(event['total_tokens'])
    
    return stats

def format_number(num):
    """Format large numbers nicely"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    return str(int(num))

def format_hour(hour):
    """Format hour as 12-hour time"""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"

def print_box(title, content, width=70):
    """Print a box with title and content"""
    print("┌" + "─" * (width - 2) + "┐")
    print(f"│ {title:<{width-4}} │")
    print("├" + "─" * (width - 2) + "┤")
    for line in content:
        print(f"│ {line:<{width-4}} │")
    print("└" + "─" * (width - 2) + "┘")
    print()

def generate_summary(stats):
    """Generate summary data structure"""
    
    # Calculate date range in days
    date_range = stats['date_range']
    days_active = (date_range['end'] - date_range['start']).days + 1
    
    # Top models
    top_models_by_usage = sorted(stats['model_usage'].items(), key=lambda x: x[1], reverse=True)[:5]
    top_models_by_tokens = sorted(stats['model_tokens'].items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Peak times
    peak_hour = max(stats['hourly_usage'].items(), key=lambda x: x[1])
    peak_day = max(stats['daily_usage'].items(), key=lambda x: x[1])
    peak_month = max(stats['monthly_usage'].items(), key=lambda x: x[1])
    peak_weekday = max(stats['weekday_usage'].items(), key=lambda x: x[1])
    
    # Cache efficiency
    avg_cache_efficiency = mean(stats['cache_efficiency']) * 100 if stats['cache_efficiency'] else 0
    
    # Token stats
    avg_tokens = mean(stats['token_distribution']) if stats['token_distribution'] else 0
    median_tokens = median(stats['token_distribution']) if stats['token_distribution'] else 0
    max_tokens = max(stats['token_distribution']) if stats['token_distribution'] else 0
    
    # Calculate tokens per day
    tokens_per_day = stats['total_tokens'] / days_active if days_active > 0 else 0
    
    summary = {
        'year': date_range['end'].year,
        'days_active': days_active,
        'date_range': {
            'start': date_range['start'].strftime('%B %d, %Y'),
            'end': date_range['end'].strftime('%B %d, %Y')
        },
        'totals': {
            'events': stats['total_events'],
            'tokens': stats['total_tokens'],
            'tokens_formatted': format_number(stats['total_tokens']),
            'output_tokens': stats['total_output_tokens'],
            'output_tokens_formatted': format_number(stats['total_output_tokens']),
            'input_tokens': stats['total_input_tokens'],
            'input_tokens_formatted': format_number(stats['total_input_tokens']),
            'cache_read': stats['total_cache_read'],
            'cache_read_formatted': format_number(stats['total_cache_read']),
            'cost': stats['total_cost'],
            'cost_formatted': f"${stats['total_cost']:.2f}",
            'tokens_per_day': int(tokens_per_day),
            'tokens_per_day_formatted': format_number(tokens_per_day)
        },
        'top_models': {
            'by_usage': [{'model': m, 'count': c} for m, c in top_models_by_usage],
            'by_tokens': [{'model': m, 'tokens': t, 'tokens_formatted': format_number(t)} for m, t in top_models_by_tokens]
        },
        'peak_times': {
            'hour': {'hour': peak_hour[0], 'tokens': peak_hour[1], 'tokens_formatted': format_number(peak_hour[1])},
            'day': {'date': peak_day[0].strftime('%B %d, %Y'), 'tokens': peak_day[1], 'tokens_formatted': format_number(peak_day[1])},
            'month': {'month': peak_month[0], 'tokens': peak_month[1], 'tokens_formatted': format_number(peak_month[1])},
            'weekday': {'day': peak_weekday[0], 'tokens': peak_weekday[1], 'tokens_formatted': format_number(peak_weekday[1])}
        },
        'cache_stats': {
            'efficiency_percent': round(avg_cache_efficiency, 1),
            'total_cache_read': stats['total_cache_read'],
            'total_cache_read_formatted': format_number(stats['total_cache_read'])
        },
        'token_stats': {
            'average': int(avg_tokens),
            'average_formatted': format_number(avg_tokens),
            'median': int(median_tokens),
            'median_formatted': format_number(median_tokens),
            'max': max_tokens,
            'max_formatted': format_number(max_tokens)
        },
        'model_breakdown': [
            {
                'model': model,
                'usage_count': stats['model_usage'][model],
                'total_tokens': stats['model_tokens'][model],
                'total_tokens_formatted': format_number(stats['model_tokens'][model]),
                'cost': stats['model_cost'][model],
                'cost_formatted': f"${stats['model_cost'][model]:.2f}",
                'percentage': round((stats['model_tokens'][model] / stats['total_tokens']) * 100, 1) if stats['total_tokens'] > 0 else 0
            }
            for model in sorted(stats['model_tokens'].keys(), key=lambda m: stats['model_tokens'][m], reverse=True)
        ]
    }
    
    return summary

def display_summary(data):
    """Display the summary in a formatted terminal output"""
    
    # Header
    print("\n" + "=" * 70)
    print(" " * 20 + "🎉 CURSOR WRAPPED 2025 🎉")
    print(" " * 25 + "Your Year in Code")
    print("=" * 70 + "\n")
    
    # Total Activity
    content = [
        f"Total Requests:     {data['totals']['events']:,}",
        f"Total Tokens:       {data['totals']['tokens_formatted']}",
        f"Days Active:        {data['days_active']} days",
        f"Date Range:         {data['date_range']['start']} to {data['date_range']['end']}",
    ]
    print_box("📊 TOTAL ACTIVITY", content)
    
    # Daily Stats
    content = [
        f"Tokens per Day:     {data['totals']['tokens_per_day_formatted']}",
        f"Average per Request: {data['token_stats']['average_formatted']}",
        f"Median per Request:  {data['token_stats']['median_formatted']}",
        f"Largest Request:     {data['token_stats']['max_formatted']}",
    ]
    print_box("📈 DAILY STATISTICS", content)
    
    # Cost
    content = [
        f"Total Cost:         {data['totals']['cost_formatted']}",
        f"Average per Day:    ${data['totals']['cost'] / data['days_active']:.2f}",
    ]
    print_box("💰 YOUR INVESTMENT", content)
    
    # Top Models
    content = []
    for i, model in enumerate(data['model_breakdown'][:5], 1):
        model_name = model['model'].replace('claude-', '').replace('-', ' ')
        model_name = ' '.join(word.capitalize() for word in model_name.split())
        content.append(f"{i}. {model_name:<25} {model['total_tokens_formatted']:>12} ({model['percentage']:>5.1f}%)")
    print_box("🤖 TOP 5 MODELS", content)
    
    # Peak Times
    content = [
        f"Peak Hour:          {format_hour(data['peak_times']['hour']['hour'])} ({data['peak_times']['hour']['tokens_formatted']})",
        f"Peak Day:           {data['peak_times']['day']['date']} ({data['peak_times']['day']['tokens_formatted']})",
        f"Peak Weekday:       {data['peak_times']['weekday']['day']} ({data['peak_times']['weekday']['tokens_formatted']})",
        f"Peak Month:         {data['peak_times']['month']['month']} ({data['peak_times']['month']['tokens_formatted']})",
    ]
    print_box("⏰ PEAK TIMES", content)
    
    # Cache Efficiency
    content = [
        f"Cache Hit Rate:     {data['cache_stats']['efficiency_percent']}%",
        f"Tokens from Cache:  {data['cache_stats']['total_cache_read_formatted']}",
    ]
    print_box("⚡ CACHE EFFICIENCY", content)
    
    # Footer
    print("=" * 70)
    print(" " * 25 + "Thanks for coding!")
    print(" " * 20 + "See you next year 🚀")
    print("=" * 70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Generate a Spotify Wrapped-style summary of your Cursor usage',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python3 cursor_wrapped_terminal.py usage-events-2025-12-04.csv

To export your data:
  1. Go to https://cursor.com/dashboard?tab=usage
  2. Set your date range
  3. Export the CSV file
        """
    )
    parser.add_argument('csv_file', help='Path to the Cursor usage CSV file')
    parser.add_argument('--json', help='Optional: Save summary to JSON file', metavar='OUTPUT_FILE')
    
    args = parser.parse_args()
    
    # Parse and analyze
    print(f"Analyzing Cursor usage data from {args.csv_file}...")
    try:
        events = parse_csv(args.csv_file)
        print(f"Loaded {len(events)} events")
    except FileNotFoundError:
        print(f"Error: File '{args.csv_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not events:
        print("Error: No valid events found in CSV file", file=sys.stderr)
        sys.exit(1)
    
    stats = analyze_usage(events)
    summary = generate_summary(stats)
    
    # Display summary
    display_summary(summary)
    
    # Save JSON if requested
    if args.json:
        try:
            with open(args.json, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print(f"Summary saved to {args.json}")
        except Exception as e:
            print(f"Warning: Could not save JSON file: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
