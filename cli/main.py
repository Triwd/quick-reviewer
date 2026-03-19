from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from cli.config import load_config
from cli.llm import create_client
from cli.parser import chunk_text, read_paper
from cli.prompts import build_prompts
from cli.report import ensure_report_dir, save_report

app = typer.Typer(
    name="quick-reviewer",
    help="学术论文智能审查框架",
    no_args_is_help=True,
)
console = Console()

# Common option types
ApiKeyOpt = Annotated[Optional[str], typer.Option("--api-key", help="API key")]
ModelOpt = Annotated[Optional[str], typer.Option("--model", help="Model name")]
ProviderOpt = Annotated[
    Optional[str], typer.Option("--provider", help="LLM provider (anthropic|openai)")
]
BaseUrlOpt = Annotated[
    Optional[str], typer.Option("--base-url", help="API base URL")
]
OutputOpt = Annotated[
    Optional[Path], typer.Option("--output", "-o", help="Output report path")
]


async def _run_review(
    mode: str,
    file: Path,
    api_key: str | None,
    model: str | None,
    provider: str | None,
    base_url: str | None,
    output: Path | None,
) -> None:
    config = load_config(
        provider=provider, api_key=api_key, model=model, base_url=base_url
    )

    if not config.api_key:
        console.print(
            "[red]Error: No API key configured. "
            "Set ANTHROPIC_API_KEY or OPENAI_API_KEY, or use --api-key.[/red]"
        )
        raise typer.Exit(1)

    # Read and parse paper
    console.print(f"[dim]Reading {file}...[/dim]")
    try:
        paper_content = read_paper(file)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    chunks = chunk_text(paper_content)

    if len(chunks) > 1:
        console.print(f"[dim]Document split into {len(chunks)} chunks[/dim]")

    # Build prompts
    filename = file.name
    system_prompt, user_prompt = build_prompts(mode, paper_content, filename)

    # Create client and stream
    client = create_client(config)
    console.print(
        f"[dim]Using {config.provider} / {config.resolve_model()}[/dim]"
    )
    console.print()

    collected: list[str] = []

    with Live(console=console, refresh_per_second=4) as live:
        async for text in client.stream(system_prompt, user_prompt):
            collected.append(text)
            full_text = "".join(collected)
            live.update(Markdown(full_text))

    full_text = "".join(collected)

    # Save report
    output_path = ensure_report_dir(output, source_file=filename)
    save_report(full_text, output_path, source_file=filename)
    console.print(f"\n[green]Report saved to {output_path}[/green]")


@app.command()
def review(
    file: Annotated[Path, typer.Argument(help="Paper file path")],
    api_key: ApiKeyOpt = None,
    model: ModelOpt = None,
    provider: ProviderOpt = None,
    base_url: BaseUrlOpt = None,
    output: OutputOpt = None,
) -> None:
    """对学术论文进行全面审查"""
    asyncio.run(_run_review("review", file, api_key, model, provider, base_url, output))


@app.command()
def quick(
    file: Annotated[Path, typer.Argument(help="Paper file path")],
    api_key: ApiKeyOpt = None,
    model: ModelOpt = None,
    provider: ProviderOpt = None,
    base_url: BaseUrlOpt = None,
    output: OutputOpt = None,
) -> None:
    """快速预审论文"""
    asyncio.run(_run_review("quick", file, api_key, model, provider, base_url, output))


@app.command()
def check(
    dimension: Annotated[
        str,
        typer.Argument(help="Check dimension: grammar|references|figures|structure|logic|ai"),
    ],
    file: Annotated[Path, typer.Argument(help="Paper file path")],
    api_key: ApiKeyOpt = None,
    model: ModelOpt = None,
    provider: ProviderOpt = None,
    base_url: BaseUrlOpt = None,
    output: OutputOpt = None,
) -> None:
    """专项审查论文"""
    valid_dimensions = {"grammar", "references", "figures", "structure", "logic", "ai"}
    if dimension not in valid_dimensions:
        console.print(
            f"[red]Unknown dimension: {dimension}. "
            f"Choose from: {', '.join(sorted(valid_dimensions))}[/red]"
        )
        raise typer.Exit(1)

    asyncio.run(
        _run_review(dimension, file, api_key, model, provider, base_url, output)
    )


if __name__ == "__main__":
    app()
