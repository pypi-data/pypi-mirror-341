import click
from datetime import datetime
import time  # <-- import the standard library time module
from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.models import EntryProcessingStatsDTO
from elog_cli.elog_management_backend_client.types import UNSET

console = Console()

@click.command()
@click.argument("event_at_start", nargs=1)
@click.argument("event_at_end", nargs=1)
@click.option(
    "--wait-until-complete",
    is_flag=True,
    default=False,
    help="Wait until the ngram update job is completed."
)
@click.pass_context
def update_ngram(ctx, event_at_start:str, event_at_end:str, wait_until_complete:bool):
    """
    Update the entries ngram vector.

    This command updates the ngram vector for entries in the Elog system.
    
  Parameters:
        event_at_start (str): Represents the evetAt to start including entries (YYYY-MM-DDTHH:MM:SS+00.00).
        event_at_end (str): Represents the event at that contains the end of the entries (YYYY-MM-DDTHH:MM:SS+00.00).
        wait_until_complete (bool): If True, wait until the ngram update job is completed.
    Raises:
        click.ClickException: If the update fails due to an API error.
    """
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        jobId:str = None
        #check if event_at_start if after event_at_end
        if datetime.fromisoformat(event_at_start) > datetime.fromisoformat(event_at_end):
            jobId = elog_api.update_ngram_for_entries(event_at_end, event_at_start)
            console.print(f"NGram vector update started with id: {jobId}")
        else:
            jobId = elog_api.update_ngram_for_entries(event_at_start, event_at_end)
            console.print(f"NGram vector update started with id: {jobId}")


        if wait_until_complete:
            stat:EntryProcessingStatsDTO = None
            while True:
                stat = elog_api.get_stat_for_ngram_task(jobId)
                print_stat(stat)
                if stat.completed:
                    break
                time.sleep(1)  # now uses the correct time module
            console.print("NGram vector update completed.")
    except ElogAPIError as e:
        raise click.ClickException(e)
    
def print_stat(stat: EntryProcessingStatsDTO):
    """
    Print the statistics of the entry processing in-place.

    Args:
        stat (EntryProcessingStats): The statistics to print.
    """
    from rich.live import Live
    from rich.table import Table

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Processed entries")
    table.add_column("Failed entries")
    table.add_column("Completed")
    table.add_column("Last update 'event at'")
    table.add_column("Error message")

    table.add_row(
        str(stat.processed_entries),
        str(stat.failed_entries),
        str(stat.completed),
        str(stat.last_updated if stat.last_updated != UNSET else ""),
        str(stat.error_message if stat.error_message != UNSET else "")
    )

    # Use Live to update the table in-place
    if not hasattr(print_stat, "_live"):
        print_stat._live = Live(table, refresh_per_second=4, console=console)
        print_stat._live.__enter__()
    else:
        print_stat._live.update(table)

    if stat.completed and hasattr(print_stat, "_live"):
        print_stat._live.__exit__(None, None, None)
        del print_stat._live