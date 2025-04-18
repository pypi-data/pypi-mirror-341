import glob
import json
import os
import textwrap
from collections import defaultdict, namedtuple
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from langchain_core.load import load
from PIL import Image, ImageDraw, ImageFont

# Named tuple to identify experiments
ExpKey = namedtuple("ExpKey", ["model", "algo", "target_model"])


def parse_metrics_line(line):
    parts = line.strip().split(",", 7)
    if len(parts) != 8:
        return None
    try:
        return {
            "x": float(parts[0]),
            "y": float(parts[1]),
            "x_label": parts[2],
            "metric": parts[3],
            "split": parts[4],
            "lower": float(parts[5]) if parts[5] else None,
            "upper": float(parts[6]) if parts[6] else None,
            "prompt": parts[7],
        }
    except (ValueError, IndexError):
        return None


def get_experiment_config(exp_dir):
    config_path = os.path.join(exp_dir, "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def get_experiment_key(config):
    if not config:
        return None
    try:
        # Check if this is a baseline experiment
        if "initial_prompt" in config and "model_config" in config["initial_prompt"]:
            target_model = config["initial_prompt"]["model_config"]["model"]
            target_model = (
                target_model.replace("openai:", "")
                .replace("anthropic:", "")
                .replace("claude-3-5-sonnet-20241022", "claude")
            )
            if target_model == "gpt-o1":
                target_model = "o1"
            target_model = target_model.title()
        else:
            target_model = "gpt-4o-mini"

        # Regular optimization experiment
        model = config.get("optimizer", {}).get("model", {}).get("model", "unknown")
        model = model.replace("openai:", "").replace(
            "claude-3-5-sonnet-20241022", "claude"
        )
        if model == "gpt-o1":
            model = "o1"
        model = model.title()

        algo = config.get("optimizer", {}).get("kind", "default")

        max_reasoning_steps = (
            config.get("optimizer", {}).get("max_reasoning_steps") or 0
        )
        algo_ = config.get("algorithm", {}).get("kind", "minibatch")
        if algo_ == "phaseevo":
            algo = "Evolutionary"
        elif algo == "feedback_guided":
            algo = "Gradient"
        elif algo == "fewshot":
            algo = "Few-shot"
            model = ""
        else:
            algo = "Metaprompt"
        if max_reasoning_steps > 1:
            algo += " + Reflect"
        return ExpKey(model=model, algo=algo, target_model=target_model)
    except Exception as e:
        print("Failed to get key", e)
        return None


def aggregate_with_ci(df):
    """
    Aggregator that returns a *single row* DataFrame with columns:
    ['x','y_mean','lower_mean','upper_mean','count'].
    """
    x_val = df["x"].iloc[0] if len(df) > 0 else np.nan
    y_mean = df["y"].mean()

    lower_mean = df["lower"].mean() if not df["lower"].isna().all() else np.nan
    upper_mean = df["upper"].mean() if not df["upper"].isna().all() else np.nan

    return pd.DataFrame(
        [
            {
                "x": x_val,
                "y_mean": y_mean,
                "lower_mean": lower_mean,
                "upper_mean": upper_mean,
                "count": len(df),
            }
        ]
    )


def group_dev_epoch(df):
    """
    Group the subset df by 'x', apply our aggregator.
    """
    if df.empty:
        return pd.DataFrame(
            columns=["x", "y_mean", "lower_mean", "upper_mean", "count"]
        )
    grouped = (
        df.groupby("x", group_keys=False)
        .apply(aggregate_with_ci)
        .reset_index(drop=True)
    )
    return grouped


def aggregate_by_group(metrics_dfs):
    """
    Takes a list of DataFrames, concatenates them, and aggregates dev/test data.
    """
    if not metrics_dfs:
        return (
            pd.DataFrame(columns=["x", "y_mean", "lower_mean", "upper_mean", "count"]),
            pd.DataFrame(columns=["x", "y_mean", "lower_mean", "upper_mean", "count"]),
            [],  # baseline list
            pd.Series({"y_mean": np.nan, "lower_mean": np.nan, "upper_mean": np.nan}),
        )

    combined = pd.concat(metrics_dfs, ignore_index=True)
    if combined.empty:
        return (
            pd.DataFrame(columns=["x", "y_mean", "lower_mean", "upper_mean", "count"]),
            pd.DataFrame(columns=["x", "y_mean", "lower_mean", "upper_mean", "count"]),
            [],
            pd.Series({"y_mean": np.nan, "lower_mean": np.nan, "upper_mean": np.nan}),
        )

    # Dev sets
    dev_epoch = group_dev_epoch(
        combined[(combined["split"] == "dev") & (combined["x_label"] == "epoch")]
    )
    dev_tokens = group_dev_epoch(
        combined[(combined["split"] == "dev") & (combined["x_label"] == "total tokens")]
    )

    # Test sets
    test_data = combined[
        (combined["split"] == "test") & (combined["x_label"].isin(["base", "final"]))
    ]
    baseline_test = test_data[test_data["x_label"] == "base"]["y"].tolist()
    final_rows = test_data[test_data["x_label"] == "final"]

    if final_rows.empty:
        best_prompt_test = pd.Series(
            {"y_mean": np.nan, "lower_mean": np.nan, "upper_mean": np.nan}
        )
    else:
        out_df = aggregate_with_ci(final_rows)
        best_prompt_test = out_df.iloc[0]

    return dev_epoch, dev_tokens, baseline_test, best_prompt_test


def is_baseline(rows):
    if len(rows) != 2:
        return False
    if all(r["split"] == "test" for r in rows):
        return True
    return False


def collect_experiment_data(root_dir):
    raw_experiments_with_time = defaultdict(list)
    baseline_experiments_with_time = defaultdict(list)
    experiment_prompts = defaultdict(list)  # Store prompts with their experiment keys

    for metrics_file in glob.glob(
        os.path.join(root_dir, "**/metrics.csv"), recursive=True
    ):
        exp_dir = os.path.dirname(metrics_file)
        exp_name = os.path.basename(exp_dir)

        try:
            dt_str = exp_name.split("exp-")[1]
            exp_time = datetime.strptime(dt_str, "%Y-%m-%d-%H-%M-%S")
        except (IndexError, ValueError):
            print(f"Skipping malformed experiment name: {exp_name}")
            continue

        config = get_experiment_config(exp_dir)
        exp_key = get_experiment_key(config)
        if not exp_key:
            continue

        rows = []
        with open(metrics_file, "r") as f:
            _ = f.readline()  # skip header
            for line in f:
                parsed = parse_metrics_line(line)
                if parsed is not None:
                    parsed["experiment"] = exp_name
                    parsed["model"] = exp_key.model
                    parsed["algo"] = exp_key.algo
                    parsed["target_model"] = exp_key.target_model
                    rows.append(parsed)
                    # Store prompts from test set final results
                    if parsed["split"] == "test" and parsed["x_label"] == "final":
                        experiment_prompts[exp_key].append((exp_time, parsed["prompt"]))

        if is_baseline(rows) and "few" not in exp_key.algo.lower():
            exp_key = ExpKey(
                model="", algo="Baseline", target_model=exp_key.target_model
            )
            for row in rows:
                row["algo"] = "Baseline"
                row["model"] = ""

        if rows:
            df = pd.DataFrame(rows)
            if exp_key.algo == "Baseline":
                baseline_experiments_with_time[exp_key].append((exp_time, df))
            else:
                raw_experiments_with_time[exp_key].append((exp_time, df))

    # Process regular experiments
    raw_experiments = {}
    best_prompts = {}  # Store best prompt for each experiment
    for exp_key, time_df_pairs in raw_experiments_with_time.items():
        if time_df_pairs:
            most_recent = sorted(time_df_pairs, key=lambda x: x[0], reverse=True)[0]
            raw_experiments[exp_key] = [most_recent[1]]
            # Get most recent prompt for this experiment
            if exp_key in experiment_prompts and experiment_prompts[exp_key]:
                most_recent_prompt = sorted(
                    experiment_prompts[exp_key], key=lambda x: x[0], reverse=True
                )[0]
                best_prompts[exp_key] = json.loads(
                    most_recent_prompt[1].replace('""', '"').strip('"')
                )
    # Process baseline experiments
    baseline_experiments = {}
    for exp_key, time_df_pairs in baseline_experiments_with_time.items():
        if time_df_pairs:
            most_recent = sorted(time_df_pairs, key=lambda x: x[0], reverse=True)[0]
            baseline_experiments[exp_key] = [most_recent[1]]

    # Exclude experiments with no "test set" data (i.e. no 'base' or 'final' in test split)
    valid_raw_experiments = {}
    for exp_key, dfs in raw_experiments.items():
        combined = pd.concat(dfs, ignore_index=True)
        test_data = combined[
            (combined["split"] == "test")
            & (combined["x_label"].isin(["base", "final"]))
        ]
        if not test_data.empty:
            valid_raw_experiments[exp_key] = dfs
        else:
            print("Skipping empty", exp_key)

    raw_experiments = valid_raw_experiments

    valid_baseline_experiments = {}
    for exp_key, dfs in baseline_experiments.items():
        combined = pd.concat(dfs, ignore_index=True)
        test_data = combined[
            (combined["split"] == "test")
            & (combined["x_label"].isin(["base", "final"]))
        ]
        if not test_data.empty:
            valid_baseline_experiments[exp_key] = dfs
        else:
            print("Skipping empty", exp_key)

    baseline_experiments = valid_baseline_experiments

    all_dfs = [df for dfs in raw_experiments.values() for df in dfs]
    all_baseline_dfs = [df for dfs in baseline_experiments.values() for df in dfs]

    if not all_dfs and not all_baseline_dfs:
        # Return empty placeholders
        return {
            "by_experiment": {
                "dev_epoch": [],
                "dev_tokens": [],
                "test_final": [],
                "base_scores": pd.DataFrame({"y": []}).agg({"y": ["mean", "std"]}),
                "best_prompts": {},
            },
            "by_model": defaultdict(list),
            "by_algo": defaultdict(list),
        }

    combined_df = pd.concat(all_dfs, ignore_index=True)

    processed_data = {
        "by_experiment": {
            "dev_epoch": [],
            "dev_tokens": [],
            "test_final": [],
            "base_scores": [],
            "best_prompts": best_prompts,  # Add best prompts to processed data
        },
        "by_model": defaultdict(list),
        "by_algo": defaultdict(list),
    }

    # 1. By experiment
    for exp_key, exp_dfs in raw_experiments.items():
        dev_epoch, dev_tokens, baseline_test, best_prompt_test = aggregate_by_group(
            exp_dfs
        )
        processed_data["by_experiment"]["dev_epoch"].append((exp_key, dev_epoch))
        processed_data["by_experiment"]["dev_tokens"].append((exp_key, dev_tokens))
        processed_data["by_experiment"]["test_final"].append(
            (exp_key, best_prompt_test)
        )
        processed_data["by_experiment"]["base_scores"].extend(baseline_test)

    for exp_key, exp_dfs in baseline_experiments.items():
        dev_epoch, dev_tokens, baseline_test, best_prompt_test = aggregate_by_group(
            exp_dfs
        )
        processed_data["by_experiment"]["dev_epoch"].append((exp_key, dev_epoch))
        processed_data["by_experiment"]["dev_tokens"].append((exp_key, dev_tokens))
        processed_data["by_experiment"]["test_final"].append(
            (exp_key, best_prompt_test)
        )
        processed_data["by_experiment"]["base_scores"].extend(baseline_test)

    # 2. By model
    for model in combined_df["model"].unique():
        if not model.strip():
            continue
        model_dfs = [df for df in all_dfs if df["model"].iloc[0] == model]
        dev_epoch, dev_tokens, baseline_test, best_prompt_test = aggregate_by_group(
            model_dfs
        )
        processed_data["by_model"]["dev_epoch"].append((model, dev_epoch))
        processed_data["by_model"]["dev_tokens"].append((model, dev_tokens))
        processed_data["by_model"]["test_final"].append((model, best_prompt_test))
        processed_data["by_model"]["base_scores"].extend(baseline_test)

    # 3. By algo
    for algo in combined_df["algo"].unique():
        algo_dfs = [df for df in all_dfs if df["algo"].iloc[0] == algo]
        dev_epoch, dev_tokens, baseline_test, best_prompt_test = aggregate_by_group(
            algo_dfs
        )
        processed_data["by_algo"]["dev_epoch"].append((algo, dev_epoch))
        processed_data["by_algo"]["dev_tokens"].append((algo, dev_tokens))
        processed_data["by_algo"]["test_final"].append((algo, best_prompt_test))
        processed_data["by_algo"]["base_scores"].extend(baseline_test)

    # Convert baseline test scores to mean/std for each grouping
    for grouping in ["by_experiment", "by_model", "by_algo"]:
        base_scores = processed_data[grouping]["base_scores"]
        if base_scores:
            base_scores_df = pd.DataFrame({"y": base_scores})
            processed_data[grouping]["base_scores"] = base_scores_df.agg(
                {"y": ["mean", "std"]}
            )
        else:
            processed_data[grouping]["base_scores"] = pd.DataFrame({"y": []}).agg(
                {"y": ["mean", "std"]}
            )

    return processed_data


def render_prompt_as_image(
    prompt_text, title, output_path, width=1200, min_height=800, font_size=24
):
    """
    Render a prompt representation as a PNG image with a title.

    Args:
        prompt_text (str): The text to render
        title (str): Title to display at the top of the image
        output_path (str): Path to save the PNG file
        width (int): Image width in pixels
        min_height (int): Minimum image height in pixels
        font_size (int): Base font size for the text
    """
    # Try to load a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        title_font = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", font_size * 1.5
        )
    except OSError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # Calculate text dimensions
    padding = 40
    title_padding = 60

    # Process text while preserving newlines
    wrapper = textwrap.TextWrapper(
        width=80, replace_whitespace=False, drop_whitespace=False
    )
    lines = prompt_text.split("\n")
    wrapped_lines = []
    for line in lines:
        if line.strip():  # If line is not empty
            wrapped_lines.extend(wrapper.wrap(line))
        else:
            wrapped_lines.append("")  # Preserve empty lines
    wrapped_text = "\n".join(wrapped_lines)

    # Create a temporary image to calculate text height
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    # Calculate text dimensions
    text_bbox = temp_draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=8)
    title_bbox = temp_draw.textbbox((0, 0), title, font=title_font)

    # Calculate required height
    text_height = text_bbox[3] - text_bbox[1]
    title_height = title_bbox[3] - title_bbox[1]
    total_height = max(min_height, text_height + title_height + padding * 3)

    # Create the actual image
    img = Image.new("RGB", (width, int(total_height)), color="white")
    draw = ImageDraw.Draw(img)

    # Draw title
    title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
    draw.text((title_x, padding), title, font=title_font, fill="black")

    # Draw main text
    text_y = title_height + padding * 2
    draw.multiline_text(
        (padding, text_y), wrapped_text, font=font, fill="black", spacing=8
    )

    # Save the image
    img.save(output_path, "PNG")


def create_subplot(
    data,
    subplot_data,
    ax,
    colors,
    plot_type="line",
    title="",
    skip_baseline: bool = False,
):
    if plot_type == "line":
        # Plot line charts (Dev sets)
        lines = []  # Store lines for legend
        labels = []  # Store labels for legend
        for (key, df), color in zip(subplot_data, colors):
            if df.empty:
                continue
            x_vals = df["x"]
            y_mean = df["y_mean"]
            y_lower = df["lower_mean"]
            y_upper = df["upper_mean"]

            # Create label based on key type
            if isinstance(key, ExpKey):
                label = f"{key.model} - {key.algo} ({key.target_model})"
            else:
                label = str(key)

            line = ax.plot(x_vals, y_mean, color=color, linewidth=2)[0]
            ax.fill_between(x_vals, y_lower, y_upper, alpha=0.2, color=color)

            lines.append(line)
            labels.append(label)

        # Add legend with explicit lines and labels
        if lines:
            leg = ax.legend(lines, labels, loc="center left", bbox_to_anchor=(1.0, 0.5))
            leg.set_draggable(True)  # Make legend draggable

    else:  # "bar" plot (Test set performance)
        # Create color mapping for algorithms
        all_algos = {"Baseline"}
        for key, _ in subplot_data:
            if isinstance(key, ExpKey):
                all_algos.add(key.algo)

        # Create a fixed color palette for algorithms
        algo_colors = dict(
            zip(sorted(all_algos), sns.color_palette("husl", n_colors=len(all_algos)))
        )

        subplot_data = sorted(subplot_data, key=lambda x: x[0])

        # Split data into baseline and optimization results
        if skip_baseline:
            baseline_data = []
        else:
            baseline_data = [
                (k, s)
                for k, s in subplot_data
                if isinstance(k, ExpKey) and k.algo == "Baseline"
            ]
        optimization_data = [
            (k, s)
            for k, s in subplot_data
            if not isinstance(k, ExpKey) or k.algo != "Baseline"
        ]

        width = 0.8  # Bar width

        # Add GPT-4o-mini baseline to baseline data
        baseline_score = data["base_scores"]["y"]["mean"]
        baseline_err = data["base_scores"]["y"]["std"]
        gpt4o_mini_series = pd.Series(
            {
                "y_mean": baseline_score,
                "lower_mean": baseline_score - baseline_err,
                "upper_mean": baseline_score + baseline_err,
            }
        )
        if not skip_baseline:
            baseline_data.insert(
                0,
                (
                    ExpKey(
                        model="Gpt4o-Mini", algo="Baseline", target_model="gpt4o-mini"
                    ),
                    gpt4o_mini_series,
                ),
            )

        # Plot baseline bars first
        for i, (key, best_series) in enumerate(baseline_data):
            y_mean = best_series.get("y_mean", np.nan)
            lower_mean = best_series.get("lower_mean", np.nan)
            upper_mean = best_series.get("upper_mean", np.nan)

            if not np.isnan(y_mean):
                if not np.isnan(lower_mean) and not np.isnan(upper_mean):
                    yerr = np.array([[y_mean - lower_mean], [upper_mean - y_mean]])
                else:
                    yerr = None

                ax.bar(
                    i,
                    y_mean,
                    width,
                    yerr=yerr,
                    color=algo_colors[key.algo],
                    capsize=5,
                    alpha=0.7,
                    hatch="//",
                )
                ax.text(
                    i,
                    y_mean / 2,
                    f"{y_mean:.3f}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    color="white",
                )

        # Plot optimization results
        start_idx = len(baseline_data)
        for i, (key, best_series) in enumerate(optimization_data):
            y_mean = best_series.get("y_mean", np.nan)
            lower_mean = best_series.get("lower_mean", np.nan)
            upper_mean = best_series.get("upper_mean", np.nan)

            if not np.isnan(y_mean):
                if not np.isnan(lower_mean) and not np.isnan(upper_mean):
                    yerr = np.array([[y_mean - lower_mean], [upper_mean - y_mean]])
                else:
                    yerr = None

                ax.bar(
                    start_idx + i,
                    y_mean,
                    width,
                    yerr=yerr,
                    color=(
                        algo_colors[key.algo]
                        if isinstance(key, ExpKey)
                        else colors[i % len(colors)]
                    ),
                    capsize=5,
                )
                ax.text(
                    start_idx + i,
                    y_mean / 2,
                    f"{y_mean:.3f}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    color="white",
                )

        # Add horizontal line for GPT-4o-mini baseline
        if "base_scores" in data and not data["base_scores"].empty:
            baseline_score = data["base_scores"]["y"]["mean"]
            ax.axhline(
                y=baseline_score,
                color="black",
                linestyle="--",
                linewidth=1,
                alpha=0.7,
            )

        # Set x-ticks and labels
        x_positions = np.arange(len(baseline_data) + len(optimization_data))
        ax.set_xticks(x_positions)
        labels = []
        for key, _ in baseline_data + optimization_data:
            if isinstance(key, ExpKey):
                if key.algo.lower() in ("baseline", "few-shot"):
                    label = f"{key.algo}\n→ {key.target_model}"
                else:
                    label = f"{key.model}\n{key.algo}"
            else:
                label = str(key)
            labels.append(label)
        ax.set_xticklabels(labels, rotation=45, ha="right")

    ax.set_title(title, pad=20)
    ax.grid(True, alpha=0.3)


def create_consolidated_plots(data, output_prefix=None):
    if not output_prefix:
        return

    # Create prompt images for each experiment
    prompts = data.get("by_experiment", {}).get("best_prompts", {})
    for exp_key, prompt_data in prompts.items():
        try:
            # Get the prompt representation
            prompt_repr = load(prompt_data["manifest"]).first.pretty_repr()

            # Create a title from the experiment key
            if isinstance(exp_key, ExpKey):
                if exp_key.algo.lower() == "baseline":
                    title = "Baseline"
                elif exp_key.algo.lower() == "few-shot":
                    title = "Few-shot"
                else:
                    title = f"{exp_key.model} - {exp_key.algo}"
            else:
                title = str(exp_key)

            # Save the prompt image
            prompt_image_path = f"{output_prefix}_prompt_{title.replace(' ', '_')}.png"
            render_prompt_as_image(prompt_repr, title, prompt_image_path)
        except Exception as e:
            print(f"Failed to render prompt for {exp_key}: {e}")

    groupings = ["by_experiment", "by_model", "by_algo"]
    valid_groupings = [g for g in groupings if g in data]
    if not valid_groupings:
        return

    # Define relative widths for each plot type
    width_ratios = {"by_experiment": 15, "by_model": 8, "by_algo": 8}
    total_width = sum(width_ratios[g] for g in valid_groupings)

    # Create figure for line charts with extra space for legend
    fig_lines, axes_lines = plt.subplots(
        1,
        len(valid_groupings),
        figsize=(total_width, 6),
        dpi=300,
        gridspec_kw={"width_ratios": [width_ratios[g] for g in valid_groupings]},
    )
    if len(valid_groupings) == 1:
        axes_lines = [axes_lines]

    # Create figure for bar charts with extra bottom margin
    fig_bars, axes_bars = plt.subplots(
        1,
        len(valid_groupings),
        figsize=(total_width, 6),
        dpi=300,
        gridspec_kw={"width_ratios": [width_ratios[g] for g in valid_groupings]},
    )
    if len(valid_groupings) == 1:
        axes_bars = [axes_bars]

    for idx, grouping_name in enumerate(valid_groupings):
        group_data = data[grouping_name]

        # Calculate colors for this group
        max_len = max(
            len(group_data["dev_epoch"]),
            len(group_data["test_final"]),
            1,
        )
        colors = sns.color_palette("husl", n_colors=max_len)

        # Plot line chart (dev set)
        skip_baseline = grouping_name != "by_experiment"
        create_subplot(
            group_data,
            group_data["dev_epoch"],
            axes_lines[idx],
            colors,
            plot_type="line",
            title=f"Dev Set by Epoch ({grouping_name})",
            skip_baseline=skip_baseline,
        )
        axes_lines[idx].set_xlabel("Epoch")
        axes_lines[idx].set_ylabel("Score")

        # For bar chart, filter out non-GPT-4o-mini baselines if this is the model chart
        if grouping_name == "by_model":
            test_final_data = [
                (k, s)
                for k, s in group_data["test_final"]
                if not isinstance(k, ExpKey) or k.algo != "Baseline"
            ]
        else:
            test_final_data = group_data["test_final"]

        create_subplot(
            group_data,
            test_final_data,
            axes_bars[idx],
            colors,
            plot_type="bar",
            title=f"Test Set Performance ({grouping_name})",
            skip_baseline=skip_baseline,
        )
        axes_bars[idx].set_ylabel("Score")

    # Adjust layout for line charts with extra space for legend
    fig_lines.tight_layout(rect=[0, 0, 0.9, 1])

    # Adjust layout for bar charts with extra bottom margin for labels
    fig_bars.tight_layout(rect=[0, 0.2, 1, 1])  # Increase bottom margin

    if output_prefix:
        plt.figure(fig_lines.number)
        plt.savefig(
            f"{output_prefix}_dev_epochs.svg",
            format="svg",
            bbox_inches="tight",
            dpi=300,
            facecolor="white",
            edgecolor="none",
        )
        plt.savefig(
            f"{output_prefix}_dev_epochs.png",
            format="png",
            bbox_inches="tight",
            dpi=900,
            facecolor="white",
            edgecolor="none",
        )

    # Adjust layout and save bar charts
    if output_prefix:
        plt.figure(fig_bars.number)
        plt.savefig(
            f"{output_prefix}_test_performance.svg",
            format="svg",
            bbox_inches="tight",
            dpi=300,
            facecolor="white",
            edgecolor="none",
        )
        plt.savefig(
            f"{output_prefix}_test_performance.png",
            format="png",
            bbox_inches="tight",
            dpi=300,
            facecolor="white",
            edgecolor="none",
        )
    else:
        plt.show()

    plt.close(fig_lines)
    plt.close(fig_bars)


def plot_results_svg(data, output_prefix=None):
    """
    Creates two consolidated plots:
    1. Line charts showing dev set performance over epochs for all groupings
    2. Bar charts showing test set performance for all groupings
    """
    plt.style.use("seaborn-v0_8-whitegrid")

    create_consolidated_plots(data, output_prefix)


# import shutil

# # keep
# root_dirs = [
#     "experiments/email_elon",
#     "experiments/email_cs",
#     "experiments/email_cs10",
#     # "experiments/cs_tooluse",
#     "experiments/math_multi",
#     "experiments/email_cs_simple",
# ]
# figures_dir = os.path.join(
#     "experiments", "figures"
# )  ## os.path.join(root_dir, "figures")
# # Remove the entire figures directory and its contents if it exists
# if os.path.exists(figures_dir):
#     shutil.rmtree(figures_dir)
# # Create a new empty figures directory
# os.makedirs(figures_dir, exist_ok=True)
# results_list = []
# all_prompts = {}
# for root_dir in root_dirs:
#     print("For root", root_dir)
#     results = collect_experiment_data(root_dir)
#     all_prompts[root_dir] = results["by_experiment"]["best_prompts"]
#     results_list.append(results)
#     plot_results_svg(
#         results,  # output_prefix=os.path.join(figures_dir, root_dir.split("/")[-1])
#     )


## The aggregate scores

# Old code
# def compute_normalized_scores(results_list):
#     """
#     Compute normalized scores across datasets relative to GPT-4o-mini baseline.
#     Returns normalized scores for each experiment type with confidence intervals.
#     """
#     normalized_data = defaultdict(list)

#     for results in results_list:
#         # Get baseline score for this dataset
#         baseline_score = results["by_experiment"]["base_scores"]["y"]["mean"]
#         if baseline_score == 0:
#             continue

#         # Process test final scores
#         for exp_key, series in results["by_experiment"]["test_final"]:
#             if exp_key.algo == "Baseline":
#                 continue

#             # Compute relative improvement
#             score = series["y_mean"]
#             relative_improvement = (score - baseline_score) / baseline_score

#             # Store as (model, algo) tuple for easier aggregation
#             exp_type = (exp_key.model, exp_key.algo)
#             normalized_data[exp_type].append(relative_improvement)

#     # Compute statistics for each experiment type
#     aggregated_stats = {}
#     for exp_type, scores in normalized_data.items():
#         if len(scores) < 2:  # Need at least 2 points for confidence interval
#             continue

#         scores_array = np.array(scores)
#         mean_improvement = np.mean(scores_array)

#         # Compute 95% confidence interval using bootstrapping
#         n_bootstrap = 10000
#         bootstrap_means = []
#         for _ in range(n_bootstrap):
#             bootstrap_sample = np.random.choice(
#                 scores_array, size=len(scores_array), replace=True
#             )
#             bootstrap_means.append(np.mean(bootstrap_sample))

#         ci_lower = np.percentile(bootstrap_means, 2.5)
#         ci_upper = np.percentile(bootstrap_means, 97.5)

#         aggregated_stats[exp_type] = {
#             "mean": mean_improvement,
#             "ci_lower": ci_lower,
#             "ci_upper": ci_upper,
#             "n_datasets": len(scores),
#         }

#     return aggregated_stats


# def plot_normalized_results(results_list, output_prefix=None):
#     """
#     Create plots showing normalized performance across datasets.
#     """
#     plt.style.use("seaborn-v0_8-whitegrid")

#     # Get normalized statistics
#     exp_stats = compute_normalized_scores(results_list)

#     # Create figure with three subplots
#     fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), dpi=300)

#     # 1. Plot by experiment (model + algo)
#     exp_items = sorted(exp_stats.items())
#     x_pos = np.arange(len(exp_items))
#     colors = sns.color_palette("husl", n_colors=len(exp_items))

#     for i, ((model, algo), stats) in enumerate(exp_items):
#         mean = stats["mean"] * 100
#         ci_lower = stats["ci_lower"] * 100
#         ci_upper = stats["ci_upper"] * 100

#         ax1.bar(i, mean, color=colors[i], alpha=0.7)
#         yerr = np.array([[mean - ci_lower], [ci_upper - mean]])
#         ax1.errorbar(
#             i,
#             mean,
#             yerr=yerr,
#             color="black",
#             alpha=0.3,
#             capsize=5,
#             capthick=1,
#             fmt="none",
#         )

#         # Add text labels
#         ax1.text(i, mean, f"{mean:.1f}%", ha="center", va="bottom")
#         ax1.text(i, ci_upper, f"↑{ci_upper:.1f}%", ha="center", va="bottom", fontsize=8)
#         ax1.text(i, ci_lower, f"↓{ci_lower:.1f}%", ha="center", va="top", fontsize=8)

#     ax1.set_xticks(x_pos)
#     ax1.set_xticklabels(
#         [f"{m}\n{a}" for (m, a), _ in exp_items], rotation=45, ha="right"
#     )
#     ax1.set_title("Performance by Model + Algorithm")
#     ax1.set_ylabel("% Improvement over GPT-4o-mini")
#     ax1.grid(True, alpha=0.3)

#     # 2. Plot by model (averaging over algorithms)
#     model_stats = defaultdict(list)
#     for (model, _), stats in exp_stats.items():
#         model_stats[model].append((stats["mean"], stats["ci_lower"], stats["ci_upper"]))

#     model_items = sorted(
#         (model, stat_list) for model, stat_list in model_stats.items() if model
#     )
#     x_pos = np.arange(len(model_items))
#     colors = sns.color_palette("husl", n_colors=len(model_items))

#     for i, (model, stat_list) in enumerate(model_items):
#         means = [s[0] for s in stat_list]
#         mean = np.mean(means) * 100
#         ci_lower = np.min([s[1] for s in stat_list]) * 100
#         ci_upper = np.max([s[2] for s in stat_list]) * 100

#         ax2.bar(i, mean, color=colors[i], alpha=0.7)
#         yerr = np.array([[mean - ci_lower], [ci_upper - mean]])
#         ax2.errorbar(
#             i,
#             mean,
#             yerr=yerr,
#             color="black",
#             alpha=0.3,
#             capsize=5,
#             capthick=1,
#             fmt="none",
#         )

#         # Add text labels
#         ax2.text(i, mean, f"{mean:.1f}%", ha="center", va="bottom")
#         ax2.text(i, ci_upper, f"↑{ci_upper:.1f}%", ha="center", va="bottom", fontsize=8)
#         ax2.text(i, ci_lower, f"↓{ci_lower:.1f}%", ha="center", va="top", fontsize=8)

#     ax2.set_xticks(x_pos)
#     ax2.set_xticklabels([m for m, _ in model_items], rotation=45, ha="right")
#     ax2.set_title("Performance by Optimizer Model")
#     ax2.set_ylabel("% Improvement over Baseline Prompt")
#     ax2.grid(True, alpha=0.3)

#     # 3. Plot by algorithm (averaging over models)
#     algo_stats = defaultdict(list)
#     for (_, algo), stats in exp_stats.items():
#         algo_stats[algo].append((stats["mean"], stats["ci_lower"], stats["ci_upper"]))

#     algo_items = sorted(algo_stats.items())
#     x_pos = np.arange(len(algo_items))
#     colors = sns.color_palette("husl", n_colors=len(algo_items))

#     for i, (algo, stat_list) in enumerate(algo_items):
#         means = [s[0] for s in stat_list]
#         mean = np.mean(means) * 100
#         ci_lower = np.min([s[1] for s in stat_list]) * 100
#         ci_upper = np.max([s[2] for s in stat_list]) * 100

#         ax3.bar(i, mean, color=colors[i], alpha=0.7)
#         yerr = np.array([[mean - ci_lower], [ci_upper - mean]])
#         ax3.errorbar(
#             i,
#             mean,
#             yerr=yerr,
#             color="black",
#             alpha=0.3,
#             capsize=5,
#             capthick=1,
#             fmt="none",
#         )

#         # Add text labels
#         ax3.text(i, mean, f"{mean:.1f}%", ha="center", va="bottom")
#         ax3.text(i, ci_upper, f"↑{ci_upper:.1f}%", ha="center", va="bottom", fontsize=8)
#         ax3.text(i, ci_lower, f"↓{ci_lower:.1f}%", ha="center", va="top", fontsize=8)

#     ax3.set_xticks(x_pos)
#     ax3.set_xticklabels([a for a, _ in algo_items], rotation=45, ha="right")
#     ax3.set_title("Performance by Algorithm")
#     ax3.set_ylabel("% Improvement over GPT-4o-mini")
#     ax3.grid(True, alpha=0.3)

#     plt.tight_layout()

#     if output_prefix:
#         plt.savefig(
#             f"{output_prefix}_normalized.svg",
#             format="svg",
#             bbox_inches="tight",
#             dpi=300,
#             facecolor="white",
#             edgecolor="none",
#         )
#         plt.savefig(
#             f"{output_prefix}_normalized.png",
#             format="png",
#             bbox_inches="tight",
#             dpi=300,
#             facecolor="white",
#             edgecolor="none",
#         )
#     else:
#         plt.show()

#     plt.close()




# Named tuple or something similar for experiments.
# We'll assume your code already has ExpKey for (model, algo, target_model).
# from collections import namedtuple
# ExpKey = namedtuple("ExpKey", ["model", "algo", "target_model"])


def wilson_confint(k: int, n: int, alpha=0.05):
    """
    Returns the Wilson confidence interval [low, high] for a binomial proportion p = k/n.
    """
    if n == 0:
        return (0.0, 1.0)
    z = 1.96  # ~95%
    p = k / n
    denom = 1 + (z**2 / n)
    center = p + (z**2) / (2 * n)
    num = z * np.sqrt(p * (1 - p) / n + (z**2) / (4 * n * n))
    lower = (center - num) / denom
    upper = (center + num) / denom
    return (lower, upper)


def assign_ranks_descending(scores_dict):
    """
    Given a dict {method_key: score}, return a dict {method_key: rank}.
    Rank is 1/position, so higher is better. Best gets 1.0, second gets 0.5, etc.
    Ties get the average of their inverse positions.

    Example:
        scores_dict = {"A": 0.8, "B": 0.7, "C": 0.7}
        => ranks {"A": 1.0, "B": 0.4, "C": 0.4}  # average of 1/2 and 1/3 for ties
    """
    # Sort by descending score
    items_sorted = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    # We'll iterate in sorted order, keep track of position, handle ties
    ranks_out = {}
    current_pos = 1  # Start from position 1
    while items_sorted:
        # All items with the same score
        score = items_sorted[0][1]
        tied = [x for x in items_sorted if x[1] == score]
        # The average rank for these ties is the mean of 1/position for their positions
        tie_count = len(tied)
        avg_rank = np.mean(
            [1.0 / pos for pos in range(current_pos, current_pos + tie_count)]
        )
        # Assign that rank to each tied item
        for item in tied:
            ranks_out[item[0]] = avg_rank
        # Remove them, update position
        items_sorted = items_sorted[tie_count:]
        current_pos += tie_count
    return ranks_out


def compute_aggregated_stats(
    results_list,
    aggregator="percent",
    group_by_model=False,
):
    """
    Computes aggregator-values across multiple "results" (datasets).
      - aggregator in {"percent", "absolute", "rank", "winrate_all"}
      - if group_by_model=True, we combine all methods for the same 'model' in a dataset
        by picking the *best method's score* (i.e. max) before aggregator logic.

    Returns:
      aggregator_data: dict[(model, algo)] -> list of aggregator-values across datasets
        (For rank or winrate_all, the aggregator-value is the rank or average win fraction.)
    """

    aggregator_data = defaultdict(list)

    for results_idx, results in enumerate(results_list):
        # 1) Extract baseline
        base_scores_df = results["by_experiment"]["base_scores"]
        if base_scores_df.empty or "mean" not in base_scores_df["y"]:
            # No baseline => skip
            continue
        baseline_val = base_scores_df["y"]["mean"]

        # 2) Gather each method's final test score
        #    key is (model, algo), value is float score
        method_scores = {}
        for exp_key, series in results["by_experiment"]["test_final"]:
            if not hasattr(exp_key, "algo"):
                continue  # skip weird keys
            score = series.get("y_mean", np.nan)
            if np.isnan(score):
                continue

            # For percent/absolute, we don't want to include baseline
            if (
                aggregator in ("percent", "absolute")
                and exp_key.algo.lower() == "base prompt"
            ):
                continue

            # Possibly group by model, meaning we only store the *best score*
            if group_by_model:
                # We'll just use the model name alone as the dictionary key
                # (rather than (model, algo)).
                # Then we pick the best among all algos for that model on this dataset.
                model_key = exp_key.model
                if model_key not in method_scores:
                    method_scores[model_key] = score
                else:
                    # keep best
                    method_scores[model_key] = max(method_scores[model_key], score)
            else:
                # Normal mode: keep (model, algo) distinct
                method_scores[(exp_key.model, exp_key.algo)] = score

        # If aggregator is "percent" or "absolute", we do a direct difference with baseline
        if aggregator in ("percent", "absolute"):
            for method_key, final_score in method_scores.items():
                if aggregator == "percent":
                    if baseline_val == 0:
                        val = np.nan
                    else:
                        val = (final_score - baseline_val) / baseline_val
                else:  # aggregator == "absolute"
                    val = final_score - baseline_val
                aggregator_data[method_key].append(val)

        elif aggregator == "winrate_all":
            # We compare each method's score to all others in this dataset
            # for a "fraction of methods beaten".
            # If you have M methods, for method i,
            #    #wins_i = sum( final_score_i > final_score_j for j in others ),
            #    fraction_i = #wins_i / (M-1).
            # Then store fraction_i as aggregator_data[method_key].
            if len(method_scores) < 2:
                # Can't do a comparison with fewer than 2 methods
                continue
            keys_list = list(method_scores.keys())
            for i, key_i in enumerate(keys_list):
                score_i = method_scores[key_i]
                wins = 0
                for j, key_j in enumerate(keys_list):
                    if i == j:
                        continue
                    if score_i > method_scores[key_j]:
                        wins += 1
                fraction_win = wins / (len(keys_list) - 1)
                aggregator_data[key_i].append(fraction_win)
            print(f"SUMMARY: {aggregator_data}")
            print(f"TOTAL: {sum(aggregator_data.values())}")
            print(f"MEAN: {np.mean(list(aggregator_data.values()))}")

        elif aggregator == "rank":
            # 1 = best rank, 2 = second, etc.
            # We'll sort by descending score, assign ranks,
            # then aggregator_data[method_key] gets that rank.
            # Ties => average rank.
            if not method_scores:
                continue
            rank_dict = assign_ranks_descending(method_scores)
            # rank_dict is {method_key: rank_value}
            for mkey, rank in rank_dict.items():
                aggregator_data[mkey].append(rank)

    return aggregator_data


def summarize_aggregated_stats(aggregator_data, aggregator="percent"):
    """
    aggregator_data: dict of {method_key: [vals across datasets]}
    aggregator in {"percent", "absolute", "winrate_all", "rank"}

    We produce a summary: mean, ci_lower, ci_upper, count n.
    By default we do a simple normal approximation for the mean ± 1.96 * std / sqrt(n).

    For rank or for difference data, that might be passable if n is not too small.
    For winrate_all, we might do a normal approximation OR a binomial approach.
      - But note that 'winrate_all' is not strictly a single binomial (like p = #wins/n),
        it's an average of fractions across tasks, so a normal approx is often fine.
    """
    summary = {}

    for method_key, values in aggregator_data.items():
        arr = np.array(values, dtype=float)
        arr = arr[~np.isnan(arr)]
        n = len(arr)
        if n == 0:
            continue
        mean_val = np.mean(arr)
        std_val = np.std(arr, ddof=1)
        se = std_val / np.sqrt(n)
        z = 1.96
        ci_lower = mean_val - z * se
        ci_upper = mean_val + z * se
        summary[method_key] = {
            "mean": mean_val,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "n": n,
        }
    return summary


def plot_aggregated_stats(
    stats_summary, aggregator="percent", output_prefix=None, by_type="all"
):
    """
    Given a dict {method_key: {"mean", "ci_lower", "ci_upper", "n"}}, plot a bar chart.
    method_key might be (model, algo) or just model if group_by_model was used.
    by_type: one of ["all", "model", "algo"] to control what to plot
    """
    # Filter out empty model cases for all plots, but keep few-shot
    if by_type == "all":
        stats_summary = {
            k: v
            for k, v in stats_summary.items()
            if isinstance(k, tuple) and (k[0] or k[1] == "Few-shot")
        }
    elif by_type == "model":
        stats_summary = {
            k: v for k, v in stats_summary.items() if k and isinstance(k, str)
        }  # Keep non-empty string models

    # For algorithm plots, extract just the algorithm name from (model, algo) tuples
    if by_type == "algo":
        algo_stats = defaultdict(list)
        for (model, algo), stats in stats_summary.items():
            if not isinstance(model, str) or (not model and algo != "Few-shot"):
                continue
            algo_stats[algo].append(stats)

        # Average the stats for each algorithm
        stats_summary = {}
        for algo, stat_list in algo_stats.items():
            means = [s["mean"] for s in stat_list]
            mean_val = np.mean(means)
            ci_lower = min(s["ci_lower"] for s in stat_list)
            ci_upper = max(s["ci_upper"] for s in stat_list)
            n = sum(s["n"] for s in stat_list)
            stats_summary[algo] = {
                "mean": mean_val,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "n": n,
            }

    # Sort in a stable manner
    sorted_keys = sorted(stats_summary.keys(), key=lambda x: str(x))
    labels = []
    means = []
    err_low = []
    err_high = []

    for key in sorted_keys:
        s = stats_summary[key]
        mean_val = s["mean"]
        ci_l = s["ci_lower"]
        ci_u = s["ci_upper"]

        # Format label based on key type
        if isinstance(key, tuple):
            model, algo = key
            if algo == "Few-shot":
                label = "Few-shot"
            else:
                label = f"{model}\n{algo}"
        else:
            label = str(key)

        labels.append(label)
        means.append(mean_val)
        err_low.append(mean_val - ci_l)
        err_high.append(ci_u - mean_val)

    x = np.arange(len(labels))
    colors = sns.color_palette("husl", n_colors=len(labels))

    plt.figure(figsize=(10, 5), dpi=150)
    plt.style.use("seaborn-v0_8-whitegrid")

    # Plot bars directly instead of using sns.barplot
    for i, (mean, color) in enumerate(zip(means, colors)):
        plt.bar(i, mean, color=color, alpha=0.7, edgecolor="black")

    plt.errorbar(
        x,
        means,
        yerr=[err_low, err_high],
        fmt="none",
        ecolor="black",
        elinewidth=1.5,
        capsize=5,
    )

    plt.xticks(x, labels, rotation=45, ha="right")

    # Better titles and labels based on aggregator and by_type
    if by_type == "all":
        entity = "Method"
    elif by_type == "model":
        entity = "Optimizer Model"  # Clarify this is about the optimizer
    else:  # algo
        entity = "Algorithm"

    if aggregator == "percent":
        plt.ylabel("Improvement over Base Prompt (%)")
        plt.title(f"Relative Performance by {entity}")
    elif aggregator == "absolute":
        plt.ylabel("Score Difference vs. Base Prompt")
        plt.title(f"Absolute Performance Gain by {entity}")
    elif aggregator == "winrate_all":
        plt.ylabel("Win Rate vs. Other Methods")
        plt.title(f"Head-to-Head Performance by {entity}")
        plt.ylim([0, 1])
    elif aggregator == "rank":
        plt.ylabel("Inverse Rank Score (1=best)")
        plt.title(f"Relative Ranking by {entity}")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_prefix:
        suffix = ""
        if by_type == "model":
            suffix = "_by_optimizer"
        elif by_type == "algo":
            suffix = "_by_algorithm"
        plt.savefig(f"{output_prefix}_{aggregator}{suffix}.png", dpi=200)
        plt.savefig(f"{output_prefix}_{aggregator}{suffix}.svg")
    else:
        plt.show()
    plt.close()


def _plot_single_comparison(
    stats_summary, aggregator="percent", by_type="all", ax=None
):
    """Helper function to plot a single comparison chart"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)

    # Filter stats and prepare data
    if by_type == "all":
        # Keep all method-level data, excluding baseline for percent/absolute
        stats_summary = {
            k: v
            for k, v in stats_summary.items()
            if isinstance(k, tuple)
            and (aggregator in ("winrate_all", "rank") or k[1] != "Base Prompt")
        }
    elif by_type == "model":
        # Keep only model-level data
        stats_summary = {
            k: v for k, v in stats_summary.items() if k and isinstance(k, str)
        }

    # For algorithm plots, extract just the algorithm name from (model, algo) tuples
    if by_type == "algo":
        algo_stats = defaultdict(list)
        for (model, algo), stats in stats_summary.items():
            if not isinstance(model, str) or (
                algo == "Base Prompt" and aggregator not in ("winrate_all", "rank")
            ):
                continue
            algo_stats[algo].append(stats)

        # Average the stats for each algorithm
        stats_summary = {}
        for algo, stat_list in algo_stats.items():
            means = [s["mean"] for s in stat_list]
            mean_val = np.mean(means)
            ci_lower = min(s["ci_lower"] for s in stat_list)
            ci_upper = max(s["ci_upper"] for s in stat_list)
            n = sum(s["n"] for s in stat_list)
            stats_summary[algo] = {
                "mean": mean_val,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "n": n,
            }

    # Sort and prepare data
    sorted_keys = sorted(stats_summary.keys(), key=lambda x: str(x))
    labels = []
    means = []
    err_low = []
    err_high = []

    for key in sorted_keys:
        s = stats_summary[key]
        mean_val = s["mean"]
        ci_l = s["ci_lower"]
        ci_u = s["ci_upper"]

        # Format label based on key type
        if isinstance(key, tuple):
            model, algo = key
            if algo == "Few-shot":
                label = "Few-shot"
            elif algo == "Base Prompt":
                label = "Base Prompt"
            else:
                label = f"{model}\n{algo}"
        else:
            label = str(key)

        labels.append(label)
        means.append(mean_val)
        err_low.append(mean_val - ci_l)
        err_high.append(ci_u - mean_val)

    x = np.arange(len(labels))
    colors = sns.color_palette("husl", n_colors=len(labels))

    # Plot bars
    for i, (mean, color) in enumerate(zip(means, colors)):
        ax.bar(i, mean, color=color, alpha=0.7, edgecolor="black")

        # Add value annotations
        ax.text(i, mean, f"{mean:.2f}", ha="center", va="bottom")

        # Add CI bound annotations with reduced precision and no arrows
        ci_l = mean - err_low[i]
        ci_u = mean + err_high[i]
        ax.text(i, ci_u, f"{ci_u:.2f}", ha="center", va="bottom", fontsize=8)
        ax.text(i, ci_l, f"{ci_l:.2f}", ha="center", va="top", fontsize=8)

    # Add error bars
    ax.errorbar(
        x,
        means,
        yerr=[err_low, err_high],
        fmt="none",
        ecolor="black",
        elinewidth=1.5,
        capsize=5,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")

    # Add baseline
    ax.axhline(y=0, color="black", linestyle="--", alpha=0.3)

    # Better titles and labels based on aggregator and by_type
    if by_type == "all":
        entity = "Method"
    elif by_type == "model":
        entity = "Optimizer Model"  # Clarify this is about the optimizer
    else:  # algo
        entity = "Algorithm"

    if aggregator == "percent":
        ax.set_ylabel("Improvement over Base Prompt (%)")
        ax.set_title(f"Relative Performance by {entity}")
    elif aggregator == "absolute":
        ax.set_ylabel("Score Difference vs. Base Prompt")
        ax.set_title(f"Absolute Performance Gain by {entity}")
    elif aggregator == "winrate_all":
        ax.set_ylabel("Win Rate vs. Other Methods")
        ax.set_title(f"Head-to-Head Performance by {entity}")
        ax.set_ylim([0, 1])
    elif aggregator == "rank":
        ax.set_ylabel("Inverse Rank Score (1=best)")
        ax.set_title(f"Relative Ranking by {entity}")

    ax.grid(True, alpha=0.3)


def run_comparisons(results_list, output_prefix=None):
    """
    Example usage: runs multiple aggregator strategies,
    both normal (model+algo) and grouped by model.
    """
    for aggregator in ["absolute", "percent", "winrate_all", "rank"]:
        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), dpi=300)

        # 1) method-level (model + algo)
        agg_data = compute_aggregated_stats(
            results_list, aggregator=aggregator, group_by_model=False
        )
        stats_summ = summarize_aggregated_stats(agg_data, aggregator=aggregator)
        _plot_single_comparison(
            stats_summ, aggregator=aggregator, by_type="all", ax=ax1
        )

        # 2) model-level (best algo per model on each dataset)
        agg_data_m = compute_aggregated_stats(
            results_list, aggregator=aggregator, group_by_model=True
        )
        stats_summ_m = summarize_aggregated_stats(agg_data_m, aggregator=aggregator)
        _plot_single_comparison(
            stats_summ_m, aggregator=aggregator, by_type="model", ax=ax2
        )

        # 3) algorithm-level (averaging over models)
        _plot_single_comparison(
            stats_summ, aggregator=aggregator, by_type="algo", ax=ax3
        )

        plt.tight_layout()
        if output_prefix:
            plt.savefig(f"{output_prefix}_{aggregator}.png", dpi=200)
            plt.savefig(f"{output_prefix}_{aggregator}.svg")
        else:
            plt.show()
        plt.close()


agent_mem = StoreMemory(
    variable="agent_mem",  # Default to None meaning it will append it at the end of the system prompt
    label="Agent instructions",
    configurable="user_id",
    update_instructions="Update if you are learning something general to be shared across all users",
    # scope=None  # default: unscoped / shared
    # schema=None  # default: string
    kind="incontext",  # or vector
)

user_mem = StoreMemory(
    label="User memories",
    scope="user_id",
    kind="vector",
    config={
        "search": {}  # Add search configuration as needed
    }
)

org_mem = StoreMemory(
    label="Organization information",
    scope="organization_id",
    kind="vector",
)

memory_prompt = Memory(
    prompt="You are a helpful assistant with access to various types of memory.",  # Define your base prompt
    segments=[agent_mem, user_mem, org_mem],
)

# Create agent with memory integration
agent = create_agent(
    "openai:gpt-o3-mini",
    prompt=memory_prompt,
    tools=[memory_prompt.update_memory],  # Include memory update tool
)

result = agent.invoke({"messages": [("user", "I hate pie.")]})
# Alternatively, if you didn't want the agent to memory its own memory:

hippocampus_prompt = Memory(
    prompt="You are a helpful assistant with access to various types of memory. Only update memories. No need to respond to the user.",  # Define your base prompt
    segments=[agent_mem, user_mem, org_mem],
)
hippocampus = create_agent(
    "openai:gpt-o3-mini",
    prompt=hippocampus_prompt,
    tools=[hippocampus_prompt.update_memory],
)
hippocampus.invoke({"messages": result["messages"] + [("user", 'reflect on the above conversation and update whatever memory is needed')]})
