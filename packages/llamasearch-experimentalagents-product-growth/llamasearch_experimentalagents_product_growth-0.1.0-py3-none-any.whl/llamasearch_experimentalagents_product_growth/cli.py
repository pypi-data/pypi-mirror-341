"""
Command-line interface for LlamaSearch ExperimentalAgents: Product Growth.

This module provides a Typer-based CLI for the LlamaSearch system, allowing
users to analyze feedback, generate strategies, visualize results, and more.
"""

import json
import os
import time
from pathlib import Path
from typing import Annotated, List, Literal, Optional

import pandas as pd
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.markdown import Markdown

from llamasearch_experimentalagents_product_growth import __version__
from llamasearch_experimentalagents_product_growth.agents.analyzer import analyze_feedback
from llamasearch_experimentalagents_product_growth.agents.strategist import generate_growth_strategies
from llamasearch_experimentalagents_product_growth.core.llm_router import get_available_models
from llamasearch_experimentalagents_product_growth.utils.datasette import launch_datasette
from llamasearch_experimentalagents_product_growth.utils.logging import setup_logging
from llamasearch_experimentalagents_product_growth.utils.vector_store import get_vector_stores
from llamasearch_experimentalagents_product_growth.visualizations.growth_garden import GrowthVisualizer
from llamasearch_experimentalagents_product_growth.visualizations.insight_tree import InsightTreeVisualizer
from llamasearch_experimentalagents_product_growth.gui.launcher import launch_gui

# Initialize Typer app
app = typer.Typer(
    help="LlamaSearch ExperimentalAgents: Product Growth - AI-driven product growth engine",
    add_completion=False,
)

# Initialize console
console = Console()

# Set up logging
logger = setup_logging()


@app.callback()
def callback(
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Show version and exit")
    ] = False,
    debug: Annotated[
        bool, typer.Option("--debug", help="Enable debug logging")
    ] = False,
):
    """
    LlamaSearch ExperimentalAgents: Product Growth
    
    AI-powered product growth recommendation engine with OpenAI Agents,
    RAG, and MLX acceleration.
    """
    if debug:
        os.environ["LOG_LEVEL"] = "DEBUG"
        logger.setLevel("DEBUG")
        logger.debug("Debug logging enabled")
    
    if version:
        console.print(f"[bold]LlamaSearch ExperimentalAgents: Product Growth[/] version [cyan]{__version__}[/]")
        raise typer.Exit()


@app.command()
def analyze(
    feedback: Annotated[
        Path, typer.Argument(help="Path to CSV file containing customer feedback")
    ],
    output_dir: Annotated[
        Optional[Path], typer.Option("--output-dir", "-o", help="Directory to save analysis results")
    ] = None,
    text_column: Annotated[
        str, typer.Option("--text-column", "-t", help="Column name containing feedback text")
    ] = "feedback",
    visual: Annotated[
        Optional[Literal["garden", "tree", "none"]],
        typer.Option(help="Visualization type to display"),
    ] = "garden",
    clusters: Annotated[
        int, typer.Option("--clusters", "-c", help="Number of feedback clusters")
    ] = 5,
    backend: Annotated[
        Literal["auto", "mlx", "jax", "numpy"],
        typer.Option(help="NLP backend to use"),
    ] = "auto",
):
    """
    Analyze customer feedback and identify growth opportunities.
    
    This command processes customer feedback data from a CSV file, applies
    clustering and NLP techniques to identify key themes and sentiment,
    and optionally visualizes the results.
    """
    if not feedback.exists():
        console.print(f"[bold red]Error:[/] File {feedback} does not exist")
        raise typer.Exit(1)
    
    # Create output directory if specified
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path("./insights")
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Show welcome banner
    console.print(
        Panel.fit(
            "[bold green]LlamaSearch ExperimentalAgents[/] [bold yellow]Product Growth[/]",
            subtitle="AI-Powered Growth Strategy Engine",
            border_style="green",
        )
    )
    
    # Initialize visualizer
    visualizer = None
    if visual == "garden":
        visualizer = GrowthVisualizer()
    elif visual == "tree":
        visualizer = InsightTreeVisualizer()
    
    # Load and analyze feedback
    try:
        console.print(f"[bold]Loading feedback from[/] {feedback}")
        df = pd.read_csv(feedback)
        
        # Check if text column exists
        if text_column not in df.columns:
            available_cols = ", ".join(df.columns)
            console.print(f"[bold red]Error:[/] Column '{text_column}' not found in CSV. Available columns: {available_cols}")
            raise typer.Exit(1)
        
        console.print(f"[bold]Analyzing [blue]{len(df)}[/] feedback items using [cyan]{backend}[/] backend...[/]")
        
        # Run analysis
        results = analyze_feedback(
            feedback_df=df,
            text_column=text_column,
            n_clusters=clusters,
            backend=backend,
            visualizer=visualizer
        )
        
        # Save results
        output_path = output_dir / "analysis_results.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        console.print(f"[bold green]✓[/] Analysis complete! Results saved to {output_path}")
        
        # Display summary
        _display_analysis_summary(results)
        
        return results
    
    except Exception as e:
        console.print(f"[bold red]Error during analysis:[/] {str(e)}")
        logger.exception("Error during feedback analysis")
        raise typer.Exit(1)


@app.command()
def strategize(
    insights: Annotated[
        Path, typer.Argument(help="Path to JSON file containing analysis insights")
    ],
    output: Annotated[
        Optional[Path], typer.Option(help="Path to save strategy recommendations")
    ] = None,
    max_strategies: Annotated[
        int, typer.Option(help="Maximum number of strategies to generate")
    ] = 5,
    use_openai: Annotated[
        bool, typer.Option(help="Use OpenAI for strategy generation (requires API key)")
    ] = False,
    model: Annotated[
        Optional[str], typer.Option(help="LLM model to use for strategy generation")
    ] = None,
):
    """
    Generate growth strategies based on feedback insights.
    
    This command takes the analysis results from the 'analyze' command and
    generates actionable growth strategies with priority levels, sentiment
    scores, and Go-to-Market approaches.
    """
    if not insights.exists():
        console.print(f"[bold red]Error:[/] File {insights} does not exist")
        raise typer.Exit(1)
    
    # Load insights
    try:
        with open(insights) as f:
            insight_data = json.load(f)
        
        console.print(f"[bold]Generating growth strategies based on [blue]{insights}[/]...[/]")
        
        # Determine provider based on use_openai flag
        provider = "openai" if use_openai else None
        
        # Generate strategies
        strategies = generate_growth_strategies(
            analysis_results=insight_data,
            max_strategies=max_strategies,
            provider=provider,
            model=model,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        
        # Save strategies if output path specified
        if output:
            output_dir = output.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output, "w") as f:
                json.dump([s.to_dict() for s in strategies], f, indent=2)
            
            console.print(f"[bold green]✓[/] Strategies saved to {output}")
        
        # Display strategies
        _display_strategies(strategies)
        
        return strategies
    
    except Exception as e:
        console.print(f"[bold red]Error generating strategies:[/] {str(e)}")
        logger.exception("Error during strategy generation")
        raise typer.Exit(1)


@app.command()
def visualize(
    data: Annotated[
        Path, typer.Argument(help="Path to JSON file containing growth data")
    ],
    type: Annotated[
        Literal["garden", "tree"],
        typer.Option(help="Visualization type"),
    ] = "garden",
    duration: Annotated[
        int, typer.Option(help="Duration in seconds for the animation")
    ] = 30,
):
    """
    Create a visualization of growth strategies or insights.
    
    This command generates rich terminal visualizations of growth strategies
    using either a garden metaphor or an insight tree visualization.
    """
    if not data.exists():
        console.print(f"[bold red]Error:[/] File {data} does not exist")
        raise typer.Exit(1)
    
    try:
        # Load data
        with open(data) as f:
            data_dict = json.load(f)
        
        # Initialize visualizer
        if type == "garden":
            console.print("[bold]Growth Garden Visualization[/]")
            console.print("[dim](Animation will run for {duration} seconds...)[/]")
            visualizer = GrowthVisualizer()
            visualizer.animate_full_garden(data_dict, duration=duration)
        elif type == "tree":
            console.print("[bold]Insight Tree Visualization[/]")
            console.print("[dim](Animation will run for {duration} seconds...)[/]")
            visualizer = InsightTreeVisualizer()
            visualizer.animate_full_tree(data_dict, duration=duration)
    
    except Exception as e:
        console.print(f"[bold red]Error during visualization:[/] {str(e)}")
        logger.exception("Error during visualization")
        raise typer.Exit(1)


@app.command()
def app(
    debug: Annotated[
        bool, typer.Option(help="Launch in debug mode with developer tools")
    ] = False,
):
    """
    Launch the Tauri desktop application.
    
    This command starts the LlamaSearch Product Growth GUI application
    built with Tauri and Next.js, providing a full graphical interface
    for all functionality.
    """
    try:
        console.print("[bold]Launching LlamaSearch Product Growth desktop application...[/]")
        launch_gui(debug=debug)
    except Exception as e:
        console.print(f"[bold red]Error launching GUI:[/] {str(e)}")
        logger.exception("Error launching GUI")
        raise typer.Exit(1)


@app.command()
def explore_logs(
    port: Annotated[
        int, typer.Option(help="Port to run Datasette on")
    ] = 8001,
):
    """
    Explore agent logs and memory using Datasette.
    
    This command launches a Datasette web interface to browse and query
    the SQLite database containing agent interactions, logs, and memory.
    """
    try:
        # Determine database path from environment or use default
        db_path = os.environ.get("SQLITE_DB_PATH", "data/agent_memory.db")
        db_path = Path(db_path)
        
        if not db_path.exists():
            console.print(f"[bold yellow]Warning:[/] Database file {db_path} does not exist yet.")
            console.print("Creating empty database file...")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(db_path, "wb") as f:
                pass
        
        console.print(f"[bold]Launching Datasette explorer on port {port}...[/]")
        console.print(f"Database: {db_path}")
        console.print("[dim]Press Ctrl+C to stop.[/]")
        
        # Launch Datasette
        datasette_url = launch_datasette(db_path, port=port)
        console.print(f"[bold green]✓[/] Datasette running at: [link={datasette_url}]{datasette_url}[/link]")
        
        # Keep process running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[bold]Stopping Datasette...[/]")
    
    except Exception as e:
        console.print(f"[bold red]Error launching Datasette:[/] {str(e)}")
        logger.exception("Error launching Datasette")
        raise typer.Exit(1)


@app.command()
def models():
    """
    List available LLM models for use with the system.
    
    This command displays information about which LLM models are available
    locally and through configured API providers.
    """
    try:
        console.print("[bold]Available LLM Models:[/]")
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Discovering models...", total=None)
            available_models = get_available_models()
            progress.update(task, completed=1)
        
        # Group by provider
        providers = {}
        for model in available_models:
            provider = model["provider"]
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model)
        
        # Display models by provider
        for provider, models in providers.items():
            console.print(f"\n[bold]{provider.upper()}[/]")
            table = Table(show_header=True)
            table.add_column("Model Name")
            table.add_column("Context Size")
            table.add_column("Hardware")
            table.add_column("Status")
            
            for model in models:
                status = "[green]Available[/]" if model["available"] else "[red]Unavailable[/]"
                table.add_row(
                    model["name"],
                    str(model.get("context_size", "N/A")),
                    model.get("hardware", "N/A"),
                    status
                )
            
            console.print(table)
    
    except Exception as e:
        console.print(f"[bold red]Error listing models:[/] {str(e)}")
        logger.exception("Error listing LLM models")
        raise typer.Exit(1)


@app.command()
def vector_stores():
    """
    List available vector stores for use with the system.
    
    This command displays information about which vector stores are available
    and their status.
    """
    try:
        console.print("[bold]Available Vector Stores:[/]")
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Checking vector stores...", total=None)
            stores = get_vector_stores()
            progress.update(task, completed=1)
        
        table = Table(show_header=True)
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Location")
        table.add_column("Status")
        table.add_column("Vectors")
        
        for store in stores:
            status = "[green]Available[/]" if store["available"] else "[red]Unavailable[/]"
            table.add_row(
                store["name"],
                store["type"],
                store["location"],
                status,
                str(store.get("vector_count", "N/A"))
            )
        
        console.print(table)
    
    except Exception as e:
        console.print(f"[bold red]Error listing vector stores:[/] {str(e)}")
        logger.exception("Error listing vector stores")
        raise typer.Exit(1)


def _display_analysis_summary(results):
    """Display a summary of analysis results."""
    console.print("\n[bold]Analysis Summary:[/]")
    console.print(f"Total feedback items: {results['num_feedback_items']}")
    console.print(f"Number of clusters: {results['num_clusters']}")
    console.print(f"Backend used: {results['backend_used']}")
    
    # Show cluster information
    console.print("\n[bold]Feedback Clusters:[/]")
    table = Table(show_header=True)
    table.add_column("Cluster")
    table.add_column("Size")
    table.add_column("Sentiment", style="bold")
    table.add_column("Key Themes")
    
    for cluster_id in range(results['num_clusters']):
        cluster_str = str(cluster_id)
        size = results['cluster_sizes'].get(cluster_str, 0)
        sentiment = results['cluster_sentiments'].get(cluster_str, 0)
        
        # Format sentiment with color
        if sentiment > 0.2:
            sentiment_text = f"[green]{sentiment:.2f}[/]"
        elif sentiment < -0.2:
            sentiment_text = f"[red]{sentiment:.2f}[/]"
        else:
            sentiment_text = f"[yellow]{sentiment:.2f}[/]"
        
        # Get themes
        themes = results['cluster_themes'].get(cluster_str, [])
        theme_text = ", ".join(themes[:3])
        
        table.add_row(cluster_str, str(size), sentiment_text, theme_text)
    
    console.print(table)


def _display_strategies(strategies):
    """Display generated growth strategies."""
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


if __name__ == "__main__":
    app() 