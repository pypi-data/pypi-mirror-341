#!/usr/bin/env python3
"""
LlamaSearch ExperimentalAgents Product Growth Demo
================================================

This script demonstrates the capabilities of the LlamaSearch ExperimentalAgents
Product Growth tool by analyzing sample customer feedback data and generating
growth strategy recommendations.
"""

import os
import time
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from llamasearch.agents.analyzer import analyze_feedback
from llamasearch.agents.strategist import generate_growth_strategies
from llamasearch.llama_animations.growth_garden import GrowthVisualizer
from llamasearch.llama_animations.insight_tree import InsightTreeVisualizer

# Initialize console
console = Console()

def create_sample_data(output_path):
    """Create sample customer feedback data."""
    console.print("[bold]Creating sample customer feedback data...[/]")
    
    data = [
        {"feedback": "I love the new dashboard interface, so intuitive and easy to use!", "source": "app", "user_type": "paid"},
        {"feedback": "Can't find how to export my data, very frustrating after searching for 20 minutes", "source": "email", "user_type": "paid"},
        {"feedback": "The mobile app crashes every time I try to upload a file, please fix this ASAP", "source": "app", "user_type": "free"},
        {"feedback": "Great customer support, they resolved my issue quickly and were very friendly", "source": "email", "user_type": "paid"},
        {"feedback": "Wish there were more customization options for reports, current options are too limited", "source": "app", "user_type": "paid"},
        {"feedback": "Dashboard is slow to load with large datasets, takes over 30 seconds sometimes", "source": "app", "user_type": "paid"},
        {"feedback": "Love the new export feature, saves me so much time on my weekly reporting", "source": "email", "user_type": "paid"},
        {"feedback": "The UI is confusing and hard to navigate, took me forever to find settings", "source": "app", "user_type": "free"},
        {"feedback": "Would be great to have more templates for reports, current ones don't fit my needs", "source": "email", "user_type": "paid"},
        {"feedback": "Can't connect to my database, error messages aren't helpful at all", "source": "app", "user_type": "paid"},
        {"feedback": "The new collaboration feature is amazing, our team loves it!", "source": "app", "user_type": "paid"},
        {"feedback": "Would love to see better integration with other tools we use daily", "source": "survey", "user_type": "paid"},
        {"feedback": "Search functionality doesn't return relevant results, needs improvement", "source": "app", "user_type": "free"},
        {"feedback": "Your pricing is too high compared to competitors with similar features", "source": "email", "user_type": "free"},
        {"feedback": "The onboarding tutorial was very helpful for getting started quickly", "source": "survey", "user_type": "new"},
        {"feedback": "Need better documentation for the API, current docs are too basic", "source": "email", "user_type": "paid"},
        {"feedback": "App performance has improved a lot with the latest update, much faster now", "source": "app", "user_type": "paid"},
        {"feedback": "The analytics dashboard doesn't show the metrics I care about most", "source": "survey", "user_type": "paid"},
        {"feedback": "Love the clean design and intuitive layout, makes my job easier", "source": "app", "user_type": "new"},
        {"feedback": "Missing key features that competitors offer, considering switching", "source": "email", "user_type": "paid"},
        {"feedback": "The mobile app is fantastic, use it all the time on the go", "source": "survey", "user_type": "paid"},
        {"feedback": "Too many clicks required to complete common tasks, needs streamlining", "source": "app", "user_type": "paid"},
        {"feedback": "Customer service was unhelpful when I reported a critical bug", "source": "email", "user_type": "paid"},
        {"feedback": "Data visualization options are great, love the customizable charts", "source": "survey", "user_type": "paid"},
        {"feedback": "Need more advanced filtering options for large datasets", "source": "app", "user_type": "paid"}
    ]
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    
    console.print(f"[green]✓[/] Sample data created: {output_path} ({len(df)} feedback items)")
    return df

def run_analysis_demo(feedback_df, output_dir):
    """Run the feedback analysis demo."""
    console.print("\n[bold]Running Feedback Analysis Demo[/]")
    
    # Show using garden visualizer
    console.print("\n[bold]Analysis with Growth Garden Visualization:[/]")
    garden_visualizer = GrowthVisualizer()
    
    analysis_results = analyze_feedback(
        feedback_df,
        n_clusters=5,
        backend="auto",  # Will use MLX on Apple Silicon if available
        visualizer=garden_visualizer
    )
    
    # Save results
    output_path = output_dir / "analysis_results.json"
    import json
    with open(output_path, "w") as f:
        json.dump(analysis_results, f, indent=2)
    
    console.print(f"[green]✓[/] Analysis complete! Results saved to {output_path}")
    
    # Print summary
    console.print("\n[bold]Analysis Summary:[/]")
    console.print(f"Total feedback items: {analysis_results['num_feedback_items']}")
    console.print(f"Number of clusters: {analysis_results['num_clusters']}")
    
    # Show cluster information
    console.print("\n[bold]Feedback Clusters:[/]")
    table = rich.table.Table(show_header=True)
    table.add_column("Cluster")
    table.add_column("Size")
    table.add_column("Sentiment", style="bold")
    table.add_column("Key Themes")
    
    for cluster_id in range(analysis_results['num_clusters']):
        cluster_str = str(cluster_id)
        size = analysis_results['cluster_sizes'].get(cluster_str, 0)
        sentiment = analysis_results['cluster_sentiments'].get(cluster_str, 0)
        
        # Format sentiment with color
        if sentiment > 0.2:
            sentiment_text = f"[green]{sentiment:.2f}[/]"
        elif sentiment < -0.2:
            sentiment_text = f"[red]{sentiment:.2f}[/]"
        else:
            sentiment_text = f"[yellow]{sentiment:.2f}[/]"
        
        # Get themes
        themes = analysis_results['cluster_themes'].get(cluster_str, [])
        theme_text = ", ".join(themes[:3])
        
        table.add_row(cluster_str, str(size), sentiment_text, theme_text)
    
    console.print(table)
    
    return analysis_results

def run_strategy_demo(analysis_results, output_dir):
    """Run the strategy generation demo."""
    console.print("\n[bold]Running Strategy Generation Demo[/]")
    
    # Generate strategies
    console.print("\n[bold]Generating Growth Strategies:[/]")
    
    strategies = generate_growth_strategies(
        analysis_results,
        max_strategies=5,
        use_openai=False  # Switch to True with API key for better results
    )
    
    # Save results
    output_path = output_dir / "strategies.json"
    import json
    with open(output_path, "w") as f:
        strategies_dict = [s.model_dump() for s in strategies]
        json.dump(strategies_dict, f, indent=2)
    
    console.print(f"[green]✓[/] Strategy generation complete! Results saved to {output_path}")
    
    # Print strategies
    console.print("\n[bold]Growth Strategy Recommendations:[/]")
    
    for i, strategy in enumerate(strategies, 1):
        priority_color = {
            "low": "blue",
            "medium": "yellow",
            "high": "red",
        }[strategy.priority]
        
        panel = Panel(
            f"[bold]{strategy.feature}[/]\n\n"
            f"Priority: [{priority_color}]{strategy.priority}[/]\n"
            f"Sentiment: {strategy.sentiment_score:.2f}\n"
            f"Expected Impact: {strategy.expected_impact:.2f}\n\n"
            f"GTM Strategies: [green]{', '.join(strategy.gtm_strategies)}[/]",
            title=f"Strategy {i}",
            border_style=priority_color,
        )
        console.print(panel)
    
    return strategies

def run_visualization_demo(strategies):
    """Run the visualization demo."""
    console.print("\n[bold]Running Visualization Demo[/]")
    
    # Convert strategies to dict format
    strategy_dicts = [s.model_dump() for s in strategies]
    
    # Show Garden Visualization
    console.print("\n[bold]Growth Garden Visualization:[/]")
    console.print("[dim](Animation will run for 20 seconds...)[/]")
    
    garden_vis = GrowthVisualizer()
    garden_vis.animate_full_garden(strategy_dicts, duration=20)
    
    # Show Tree Visualization
    console.print("\n[bold]Insight Tree Visualization:[/]")
    console.print("[dim](Animation will run for 20 seconds...)[/]")
    
    tree_vis = InsightTreeVisualizer()
    tree_vis.animate_full_tree(strategy_dicts, duration=20)

def main():
    """Run the full demo."""
    # Show welcome banner
    console.print(
        Panel.fit(
            "[bold green]LlamaSearch ExperimentalAgents[/] [bold yellow]Product Growth[/]",
            subtitle="[bold]Demo Script: AI-Powered Growth Strategy Engine[/]",
            border_style="green",
        )
    )
    
    # Create output directory
    output_dir = Path("./demo_output")
    output_dir.mkdir(exist_ok=True)
    
    # Create sample data
    sample_data_path = output_dir / "sample_feedback.csv"
    if sample_data_path.exists():
        console.print(f"[bold]Loading existing sample data from {sample_data_path}[/]")
        feedback_df = pd.read_csv(sample_data_path)
    else:
        feedback_df = create_sample_data(sample_data_path)
    
    # Run analysis demo
    analysis_results = run_analysis_demo(feedback_df, output_dir)
    
    # Run strategy generation demo
    strategies = run_strategy_demo(analysis_results, output_dir)
    
    # Run visualization demo
    run_visualization_demo(strategies)
    
    # Show completion message
    console.print(
        Panel(
            "[bold green]Demo Complete![/]\n\n"
            "You've seen the core capabilities of LlamaSearch ExperimentalAgents Product Growth:\n"
            "- Customer feedback analysis with NLP clustering\n"
            "- Strategic growth recommendations generation\n"
            "- Rich visualizations for insights communication\n\n"
            "Explore the generated files in the [bold]demo_output[/] directory.",
            border_style="green",
        )
    )

if __name__ == "__main__":
    main()
