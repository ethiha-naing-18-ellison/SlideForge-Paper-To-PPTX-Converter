"""SlideForge CLI implementation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.models.schema import PaperMetadata
from app.services.extractor import extract_text_from_pdf
from app.services.sectionizer import split_into_sections
from app.services.summarizer import TextRankSummarizer, HFTransformerSummarizer
from app.services.ppt import build_presentation
from app.utils.fileio import get_output_path

app = typer.Typer(
    name="slideforge",
    help="SlideForge - Paper-to-PPTX Converter",
    add_completion=False
)
console = Console()


@app.command()
def generate(
    pdf: Optional[Path] = typer.Option(
        None, "--pdf", "-p", help="Path to PDF file"
    ),
    doi: Optional[str] = typer.Option(
        None, "--doi", "-d", help="DOI identifier"
    ),
    url: Optional[str] = typer.Option(
        None, "--url", "-u", help="Paper URL"
    ),
    theme: str = typer.Option(
        "academic", "--theme", "-t", 
        help="Presentation theme (academic, minimal, corporate)"
    ),
    max_bullets: int = typer.Option(
        6, "--max-bullets", "-b",
        help="Maximum bullets per section (1-10)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--out", "-o", help="Output file path"
    ),
    summarizer: str = typer.Option(
        "textrank", "--summarizer", "-s",
        help="Summarization method (textrank, hf_transformer)"
    )
):
    """Generate PowerPoint presentation from research paper."""
    
    # Validate input
    if not pdf and not doi and not url:
        console.print("[red]Error: Either --pdf, --doi, or --url must be provided[/red]")
        raise typer.Exit(1)
    
    if pdf and not pdf.exists():
        console.print(f"[red]Error: PDF file not found: {pdf}[/red]")
        raise typer.Exit(1)
    
    if max_bullets < 1 or max_bullets > 10:
        console.print("[red]Error: max-bullets must be between 1 and 10[/red]")
        raise typer.Exit(1)
    
    # Configure logging
    configure_logging()
    logger = get_logger(__name__)
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Process PDF
            if pdf:
                task = progress.add_task("Processing PDF...", total=None)
                
                # Extract text
                progress.update(task, description="Extracting text from PDF...")
                text = extract_text_from_pdf(str(pdf))
                
                # Extract sections
                progress.update(task, description="Detecting sections...")
                sections = split_into_sections(text)
                
                # Extract metadata
                progress.update(task, description="Extracting metadata...")
                metadata = _extract_metadata_from_text(text)
                
                # Summarize sections
                progress.update(task, description="Summarizing sections...")
                summarized_sections = _summarize_sections(
                    sections, max_bullets, summarizer, logger
                )
                
                # Generate PowerPoint
                progress.update(task, description="Generating PowerPoint...")
                
                if output:
                    output_path = output
                else:
                    output_path = get_output_path("presentation.pptx")
                
                pptx_path, slide_count = build_presentation(
                    metadata, summarized_sections, theme, str(output_path)
                )
                
                progress.update(task, description="Complete!")
                
                # Display results
                _display_results(metadata, slide_count, pptx_path)
            
            else:
                # TODO: Implement DOI/URL processing
                console.print("[yellow]DOI/URL processing not yet implemented[/yellow]")
                raise typer.Exit(1)
                
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def info():
    """Show SlideForge information."""
    console.print("[bold blue]SlideForge - Paper-to-PPTX Converter[/bold blue]")
    console.print("Version: 0.1.0")
    console.print("A tool to convert research papers into PowerPoint presentations")
    
    # Show configuration
    settings = get_settings()
    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Summarizer Backend", settings.summarizer_backend)
    table.add_row("Upload Directory", settings.upload_dir)
    table.add_row("Output Directory", settings.output_dir)
    table.add_row("Log Level", settings.log_level)
    
    console.print(table)


def _extract_metadata_from_text(text: str) -> PaperMetadata:
    """Extract metadata from text."""
    lines = text.split('\n')
    
    # Find title
    title = "Research Paper"
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) > 10 and len(line) < 200:
            if not any(char.isdigit() for char in line):
                title = line
                break
    
    return PaperMetadata(
        title=title,
        authors=[],
        venue=None,
        year=None,
        doi=None,
        url=None,
        abstract=None
    )


def _summarize_sections(sections, max_bullets: int, summarizer_type: str, logger) -> list:
    """Summarize sections using specified summarizer."""
    # Initialize summarizer
    if summarizer_type == "hf_transformer":
        try:
            summarizer = HFTransformerSummarizer()
        except Exception as e:
            logger.warning(f"HF transformer failed, falling back to TextRank: {e}")
            summarizer = TextRankSummarizer()
    else:
        summarizer = TextRankSummarizer()
    
    # Summarize each section
    summarized_sections = []
    for section_name, content in sections.sections.items():
        if content and len(content.strip()) > 50:
            bullets = summarizer.summarize_section(content, max_bullets)
            
            from app.models.schema import SummarizedSection
            summarized_sections.append(
                SummarizedSection(name=section_name, bullets=bullets)
            )
    
    return summarized_sections


def _display_results(metadata: PaperMetadata, slide_count: int, pptx_path: str) -> None:
    """Display generation results."""
    console.print("\n[bold green]✓ Presentation generated successfully![/bold green]\n")
    
    # Metadata table
    table = Table(title="Paper Information")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Title", metadata.title)
    if metadata.authors:
        table.add_row("Authors", ", ".join(metadata.authors[:3]))
    if metadata.venue:
        table.add_row("Venue", metadata.venue)
    if metadata.year:
        table.add_row("Year", str(metadata.year))
    
    console.print(table)
    
    # Results
    console.print(f"\n[bold]Results:[/bold]")
    console.print(f"• Slides generated: {slide_count}")
    console.print(f"• Output file: {pptx_path}")
    console.print(f"• File size: {Path(pptx_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    app()
