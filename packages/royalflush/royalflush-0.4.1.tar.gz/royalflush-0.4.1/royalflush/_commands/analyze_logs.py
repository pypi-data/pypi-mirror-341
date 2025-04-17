"""Command to analyze logs from a previous run."""

from pathlib import Path
from typing import List, Optional

import click
import pandas as pd
import plotly.express as px


def load_dataset(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def extract_agent_name(data: pd.DataFrame) -> pd.DataFrame:
    data["agent_name"] = data["agent"].str.split("@").str[0]
    return data


def preprocess_data(
    data: pd.DataFrame,
    max_round: Optional[int],
    whitelist_description: List[str],
    blacklist_description: List[str],
    whitelist_layer: List[str],
    blacklist_layer: List[str],
    x_unit: str,
) -> pd.DataFrame:
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    min_time = data["timestamp"].min()
    seconds = (data["timestamp"] - min_time).dt.total_seconds()

    # Convert to desired time units
    if x_unit == "minutes":
        data["x_axis"] = seconds / 60
    elif x_unit == "hours":
        data["x_axis"] = seconds / 3600
    else:
        data["x_axis"] = seconds

    data = data[data["weight_id"] == -1]

    if max_round is not None:
        data = data[data["algorithm_round"] <= max_round]

    if whitelist_description:
        data = data[data["description"].isin(whitelist_description)]
    if blacklist_description:
        data = data[~data["description"].isin(blacklist_description)]

    if whitelist_layer:
        data = data[data["layer"].isin(whitelist_layer)]
    if blacklist_layer:
        data = data[~data["layer"].isin(blacklist_layer)]

    return data


def get_unique_layers(data: pd.DataFrame) -> List[str]:
    return data["layer"].unique().tolist()


def generate_line_plots(
    data: pd.DataFrame,
    unique_layers: List[str],
    output_dir: Path,
    x_unit: str,
    fmt: str,
    show_only: bool,
) -> None:
    label_map = {
        "seconds": "Time (s)",
        "minutes": "Time (min)",
        "hours": "Time (h)",
    }

    if not show_only:
        output_dir.mkdir(parents=True, exist_ok=True)

    for layer in unique_layers:
        layer_data = data[data["layer"] == layer]

        fig = px.line(
            layer_data,
            x="x_axis",
            y="weight",
            color="agent_name",
            title=f"Weight Convergence – Layer: {layer}",
            labels={"x_axis": label_map.get(x_unit, "Time"), "weight": "Weight", "agent_name": "Agent"},
        )

        fig.update_layout(legend_title="Agents", title_x=0.5)

        if show_only:
            fig.show()
        else:
            save_path = output_dir / f"{layer.replace('.', '_')}.{fmt}"
            fig.write_image(str(save_path))


@click.command(name="analyze-logs")
@click.argument("experiment_folder", type=click.Path())
@click.option("--max-round", type=int, help="Maximum round to include.")
@click.option("--whitelist-description", multiple=True, help="Descriptions to include.")
@click.option("--blacklist-description", multiple=True, help="Descriptions to exclude.")
@click.option("--whitelist-layer", multiple=True, help="Layers to include.")
@click.option("--blacklist-layer", multiple=True, help="Layers to exclude.")
@click.option(
    "--x-unit",
    type=click.Choice(["seconds", "minutes", "hours"], case_sensitive=False),
    default="seconds",
    show_default=True,
    help="Time unit for X axis.",
)
@click.option(
    "--format",
    "image_format",
    type=click.Choice(["png", "svg", "jpeg", "webp", "pdf"], case_sensitive=False),
    default="png",
    show_default=True,
    help="Output format for the plots.",
)
@click.option(
    "--show-only",
    is_flag=True,
    help="Only show plots interactively instead of saving them.",
)
@click.pass_context
def analyze_logs_cmd(
    ctx: click.Context,
    experiment_folder: str,
    max_round: Optional[int],
    whitelist_description: List[str],
    blacklist_description: List[str],
    whitelist_layer: List[str],
    blacklist_layer: List[str],
    x_unit: str,
    image_format: str,
    show_only: bool,
) -> None:
    """
    Analyze logs from a previous run inside the given folder.

    Saves plots per layer in: experiment_folder/processed/convergence/
    """
    folder_path: Path = Path(experiment_folder)
    input_path: Path = folder_path / "raw"
    if not input_path.is_dir():
        click.echo(f"Error: '{input_path}' is not a valid directory.")
        return

    output_path: Path = folder_path / "processed"
    convergence_path: Path = output_path / "convergence"
    output_path.mkdir(parents=True, exist_ok=True)

    if ctx.obj.get("VERBOSE"):
        click.echo(f"Analyzing logs in folder: {folder_path}")

    file_path = str(input_path / "nn_convergence.csv")
    data = load_dataset(file_path)
    data = extract_agent_name(data)

    data = preprocess_data(
        data,
        max_round=max_round,
        whitelist_description=list(whitelist_description),
        blacklist_description=list(blacklist_description),
        whitelist_layer=list(whitelist_layer),
        blacklist_layer=list(blacklist_layer),
        x_unit=x_unit.lower(),
    )

    if data.empty:
        click.echo("No data remaining after filtering. Check your filters.")
        return

    unique_layers = get_unique_layers(data)
    generate_line_plots(
        data, unique_layers, convergence_path, x_unit=x_unit.lower(), fmt=image_format, show_only=show_only
    )

    click.echo(f"Log analysis complete. Plots saved in '{convergence_path}'.")
