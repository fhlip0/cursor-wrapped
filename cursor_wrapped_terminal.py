#!/usr/bin/env python3
"""
Cursor Wrapped - ASCII Terminal Summary
"""

import json
import sys
from datetime import datetime

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

def main():
    try:
        with open('cursor_wrapped_summary.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: cursor_wrapped_summary.json not found")
        print("Run: python3 cursor_wrapped.py")
        sys.exit(1)
    
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

if __name__ == '__main__':
    main()

