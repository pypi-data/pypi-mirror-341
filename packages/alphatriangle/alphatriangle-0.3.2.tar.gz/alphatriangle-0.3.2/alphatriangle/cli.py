import logging
import sys
from typing import Annotated

import typer

from alphatriangle import config, utils
from alphatriangle.app import Application
from alphatriangle.config import (
    MCTSConfig,
    PersistenceConfig,
    TrainConfig,
)
from alphatriangle.training.runners import (
    run_training_headless_mode,
    run_training_visual_mode,
)

app = typer.Typer(
    name="alphatriangle",
    help="AlphaZero implementation for a triangle puzzle game.",
    add_completion=False,
)

LogLevelOption = Annotated[
    str,
    typer.Option(
        "--log-level",
        "-l",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
        case_sensitive=False,
    ),
]

SeedOption = Annotated[
    int,
    typer.Option(
        "--seed",
        "-s",
        help="Random seed for reproducibility.",
    ),
]


def setup_logging(log_level_str: str):
    """Configures root logger based on string level."""
    log_level_str = log_level_str.upper()
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = log_level_map.get(log_level_str, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,  # Override existing config
    )
    logging.getLogger("ray").setLevel(logging.WARNING)  # Keep Ray less verbose
    logging.getLogger("matplotlib").setLevel(
        logging.WARNING
    )  # Keep Matplotlib less verbose
    logging.info(f"Root logger level set to {logging.getLevelName(log_level)}")


def run_interactive_mode(mode: str, seed: int, log_level: str):
    """Runs the interactive application."""
    setup_logging(log_level)
    logger = logging.getLogger(__name__)  # Get logger after setup
    logger.info(f"Running in {mode.capitalize()} mode...")
    utils.set_random_seeds(seed)

    # Instantiate MCTSConfig needed for validation function
    # Pydantic models with defaults can be instantiated without args
    mcts_config = MCTSConfig()
    # Pass MCTSConfig instance to validation
    config.print_config_info_and_validate(mcts_config)

    try:
        app_instance = Application(mode=mode)
        app_instance.run()
    except ImportError as e:
        # This catch block might be less relevant now imports are simplified,
        # but keep it for general import issues during runtime.
        logger.error(f"Runtime ImportError: {e}")
        logger.error("Please ensure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Exiting.")
    sys.exit(0)


@app.command()
def play(
    log_level: LogLevelOption = "INFO",
    seed: SeedOption = 42,
):
    """Run the game in interactive Play mode."""
    run_interactive_mode(mode="play", seed=seed, log_level=log_level)


@app.command()
def debug(
    log_level: LogLevelOption = "INFO",
    seed: SeedOption = 42,
):
    """Run the game in interactive Debug mode."""
    run_interactive_mode(mode="debug", seed=seed, log_level=log_level)


@app.command()
def train(
    headless: Annotated[
        bool,
        typer.Option("--headless", "-H", help="Run training without visualization."),
    ] = False,
    log_level: LogLevelOption = "INFO",
    seed: SeedOption = 42,
    # Add options to override specific TrainConfig parameters if desired
    # e.g., run_name: Annotated[Optional[str], typer.Option("--run-name")] = None
):
    """Run the AlphaTriangle training pipeline."""
    setup_logging(log_level)
    logger = logging.getLogger(__name__)  # Get logger after setup

    # --- Configuration Overrides ---
    # Create default configs first by calling constructors without args
    # Pydantic models with defaults are expected to work correctly.
    train_config_override = TrainConfig()
    persist_config_override = PersistenceConfig()

    # Apply overrides from CLI options if they were added
    # if run_name:
    #     train_config_override.RUN_NAME = run_name
    #     persist_config_override.RUN_NAME = run_name

    # Set seed in config
    train_config_override.RANDOM_SEED = seed

    if headless:
        logger.info("Starting training in Headless mode...")
        exit_code = run_training_headless_mode(
            log_level_str=log_level,
            train_config_override=train_config_override,
            persist_config_override=persist_config_override,
        )
    else:
        logger.info("Starting training in Visual mode...")
        exit_code = run_training_visual_mode(
            log_level_str=log_level,
            train_config_override=train_config_override,
            persist_config_override=persist_config_override,
        )

    logger.info(f"Training finished with exit code {exit_code}.")
    sys.exit(exit_code)


if __name__ == "__main__":
    app()
