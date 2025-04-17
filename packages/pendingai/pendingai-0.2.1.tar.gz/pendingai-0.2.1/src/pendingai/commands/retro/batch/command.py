#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import json
import os
import pathlib
import typing
from datetime import datetime

import rich
import rich.progress
import rich.prompt
import rich.table
import typer

from pendingai import config
from pendingai.commands.retro.batch.controller import RetroBatchController
from pendingai.commands.retro.batch.models import (
    Batch,
    BatchJobResult,
    BatchPage,
    BatchStatus,
)
from pendingai.commands.retro.controller import RetroController
from pendingai.context import Context
from pendingai.utils import formatters, regex_patterns

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)

app = typer.Typer(
    name="batch",
    help=(
        "Batch-based operations allowing for high-throughput large-"
        "scale retrosynthesis campaigns to explore molecule "
        "synthesizability."
    ),
    short_help="Batched operations for high-throughput synthesis screening.",
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
    rich_markup_mode=None,
)

# region callbacks -----------------------------------------------------


def tags_callback(value: list[str] | None) -> list[str] | None:
    """
    Batch tags callback with optional limit. Counts the number of tags
    does not go over a given limit.

    Args:
        value (list[str], optional): Batch tags.

    Raises:
        typer.BadParameter: Batch tags exceeds the limit.

    Returns:
        list[str]: Batch tags.
    """
    if value and len(value) > 3:
        raise typer.BadParameter("Up to 3 tag annotations allowed.")
    return value


def engine_callback(context: Context, engine: str | None) -> str:
    """
    Check an optional retrosynthesis engine id is available and exists
    in the database; if not provided then select a default engine or the
    latest alive engine.

    Args:
        context (Context): App runtime context.
        engine (str, optional): Retrosynthesis engine id.

    Raises:
        typer.BadParameter: Retrosynthesis engine id does not exist or
            is not currently available.

    Returns:
        str: Retrosynthesis engine id.
    """
    items: list = RetroController(context).retrieve_retrosynthesis_engines()
    items.sort(key=lambda x: x.last_alive, reverse=True)
    items.sort(key=lambda x: x.default, reverse=True)
    if engine and engine not in [x.id for x in items]:
        raise typer.BadParameter("Retrosynthesis engine not available.")
    elif len(items) == 0:
        raise typer.BadParameter("No retrosynthesis engine is available.")
    elif engine is None:
        engine = items[0].id
    return engine


def libraries_callback(context: Context, libraries: list[str] | None) -> list[str]:
    """
    Check an optional collection of building block libraries are
    available and exist in the database; if none exist then select all
    libraries that are currently available.

    Args:
        context (Context): App runtime context.
        libraries (list[str], optional): Building block library ids.

    Raises:
        typer.BadParameter: Building block library ids do not exist; if
            at least one is not found.

    Returns:
        list[str]: Building block library ids.
    """
    items: list = RetroController(context).retrieve_building_block_libraries()
    if len(items) == 0:
        raise typer.BadParameter("No building block library is available.")
    elif not libraries:
        libraries = [x.id for x in items]
    else:
        for library in libraries:
            if library not in [x.id for x in items]:
                raise typer.BadParameter(f"Building block library not found: {library}.")
    return libraries


def page_size_callback(page_size: int | None) -> int | None:
    """
    Page size options require an enumeration, to avoid this we do a
    quick lookup in the range [5, 25] with step size 5 to check it is a
    valid interval value.

    Args:
        page_size (int, optional): Page size option.

    Raises:
        typer.BadParameter: Page size value is not a valid interval.

    Returns:
        int: Page size option.
    """
    if page_size and page_size not in range(5, 26, 5):
        raise typer.BadParameter("Must be an interval of 5.")
    return page_size


def validate_input_file_upload_size(input_file: pathlib.Path) -> pathlib.Path:
    """
    Check file size of an input file being uploaded, used to prevent an
    oversized payload from exceeding the quote limit for the api layer.

    Args:
        input_file (pathlib.Path): Input filepath.

    Raises:
        typer.BadParameter: File exceeds upload size limit.

    Returns:
        pathlib.Path: Input filepath.
    """
    # check filesize upload limit is not exceeded by the input file
    # argument and raise appropriately if it does.
    if input_file and os.path.getsize(input_file) > config.FILE_SIZE_UPLOAD_LIMIT:
        upload_limit: float = config.FILE_SIZE_UPLOAD_LIMIT / 1e6
        raise typer.BadParameter(f"Exceeded size limit of {upload_limit:.1f}MB.")
    return input_file


def batch_id_callback(context: Context, batch_id: str | None) -> str | None:
    """
    Validate a batch id parameter by checking it follows a required
    regex pattern and then requesting the batch resource from the api
    layer to confirm it exists.

    Args:
        context (Context): App runtime context.
        batch_id (str, optional): Batch resource id.

    Raises:
        typer.BadParameter: Batch does not exist.

    Returns:
        str: Batch resource id.
    """
    if batch_id:
        controller = RetroBatchController(context)
        is_invalid: bool = regex_patterns.BATCH_ID_PATTERN.match(batch_id) is None
        if is_invalid or not controller.check_batch_exists(batch_id):
            raise typer.BadParameter("Batch does not exist.")
    return batch_id


# region command: submit -----------------------------------------------


@app.command(
    "submit",
    help=(
        "Create a batch of retrosynthesis jobs by submitting an input "
        "file containing line-delimited molecule SMILES with optional "
        "shared job parameters."
    ),
    short_help="Submit a batch of retrosynthesis jobs.",
)
def create_batch(
    context: Context,
    input_file: typing.Annotated[
        pathlib.Path,
        typer.Argument(
            metavar="MOL_FILE",
            help=(
                "Input file containing line-delimited molecule SMILES "
                "corresponding to separate retrosynthesis job. Repeated "
                "SMILES will be removed automatically."
            ),
            callback=validate_input_file_upload_size,
            resolve_path=True,
            file_okay=True,
            dir_okay=False,
            exists=True,
        ),
    ],
    retrosynthesis_engine: typing.Annotated[
        str | None,
        typer.Option(
            "--engine",
            help="Retrosynthesis engine id. Defaults to primary engine.",
            callback=engine_callback,
        ),
    ] = None,
    building_block_libraries: typing.Annotated[
        list[str] | None,
        typer.Option(
            "--library",
            help="Building block library ids. Defaults to all available libraries.",
            callback=libraries_callback,
        ),
    ] = None,
    number_of_routes: typing.Annotated[
        int,
        typer.Option(
            "--num-routes",
            help="Maximum number of retrosynthetic routes to generate. Defaults to 20.",
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=50,
        ),
    ] = 20,
    processing_time: typing.Annotated[
        int,
        typer.Option(
            "--time-limit",
            help="Maximum processing time in seconds. Defaults to 300.",
            show_default=False,
            metavar="INTEGER",
            min=60,
            max=600,
        ),
    ] = 300,
    reaction_limit: typing.Annotated[
        int,
        typer.Option(
            "--reaction-limit",
            help=(
                "Maximum number of times a specific reaction can "
                "appear in generated retrosynthetic routes. Defaults "
                "to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    building_block_limit: typing.Annotated[
        int,
        typer.Option(
            "--block-limit",
            help=(
                "Maximum number of times a building block can appear "
                "in a single retrosynthetic route. Default to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    batch_tags: typing.Annotated[
        list[str],
        typer.Option(
            "--tag",
            help=(
                "Up to 3 retrosynthesis job tag annotations. Allows for "
                "tag-based operations to be performed on batch jobs."
            ),
            callback=tags_callback,
        ),
    ] = [],
) -> str:
    """
    Submit a batch of retrosynthesis jobs for a given input file with
    line-delimited smiles; validate request input file data and send a
    batch submission request.

    Args:
        context (Context): App runtime context.
        input_file (pathlib.Path): Filepath containing line-delimited
            molecule smiles mapping to individual jobs.
        retrosynthesis_engine (str, optional): Retrosynthesis engine
            id. Defaults to primary engine.
        building_block_libraries (list[str], optional): Building block
            library ids. Defaults to all available libraries.
        number_of_routes (int, optional): Maximum number of
            retrosynthetic routes to generate. Defaults to 20.
        processing_time (int, optional): Maximum processing time in
            seconds. Defaults to 300.
        reaction_limit (int, optional): Maximum number of times a
            specific reaction can appear in generated retrosynthetic
            routes. Defaults to 3.
        building_block_limit (int, optional): Maximum number of times a
            building block can appear in a single retrosynthetic route.
            Default to 3.
        job_tags (list[str], optional): Attached optional tags when
            annotating a retrosynthesis job.

    Raises:
        typer.BadParameter: An input molecule has invalid regex pattern.

    Returns:
        str: Batch resource id.
    """
    controller = RetroBatchController(context)

    # add additional tags for the date and filename to be added to the
    # given batch tags to help users with referencing individual jobs.
    datetime_tag: str = f"date:{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
    filename_tag: str = f"file:{formatters.format_filename(input_file.name)[:123]}"
    console.print(f"[success]✓ Adding extra batch tag: [not b yellow]{datetime_tag}")
    console.print(f"[success]✓ Adding extra batch tag: [not b yellow]{filename_tag}")
    batch_tags.append(datetime_tag)
    batch_tags.append(filename_tag)

    # iterate over the input file and validate each line as a mol smiles
    # and error on invalid smiles pointing to a line number.
    desc: str = f"Parsing molecules from input file: {input_file}"
    opts: dict = {"pulse_style": None, "transient": True}
    with rich.progress.open(input_file, "rb", description=desc, **opts) as file:
        for line_no, line in enumerate(file, start=1):
            smiles: str = line.decode("utf-8").strip()
            if regex_patterns.SMILES_PATTERN.match(smiles) is None:
                err_msg: str = f"Molecule SMILES is invalid '{smiles}' (line {line_no})."
                raise typer.BadParameter(err_msg, param_hint="--input-file / -i")

    # submit the batch of smiles and return the batch id to the user on
    # success; otherwise exit.
    n: int = sum(1 for _ in input_file.open("rb"))
    console.print(f"[warn][not b]! Found {n} valid jobs from input file.")
    batch: Batch = controller.create_batch(
        input_file,
        retrosynthesis_engine,  # type: ignore
        building_block_libraries,  # type: ignore
        number_of_routes,
        processing_time,
        reaction_limit,
        building_block_limit,
        batch_tags,
    )

    # report outcome from the submit; show the batch id and the number
    # of unique submitted molecules.
    console.print(f"[success]✓ Batch submitted successfully with id: {batch.batch_id}")
    console.print(f"[success][not b]- Number of unique jobs: {batch.number_of_jobs}")
    return batch.batch_id


# region command: status -----------------------------------------------


@app.command(
    "status",
    help=(
        "Retrieve the status of a retrosynthesis batch. The status "
        "will indicate the overall progress of the entire batch. For "
        "example, if only one job is running, the status will indicate "
        "the batch is in-progress."
    ),
    short_help="Check the status of a retrosynthesis batch.",
)
def retrieve_batch_status_by_batch_id(
    context: Context,
    batch_id: typing.Annotated[
        str,
        typer.Argument(
            help="Unique batch id to retrieve the current status of.",
            callback=batch_id_callback,
        ),
    ],
) -> str:
    """
    Retrieve the status of a batch from the api layer for a resource id.
    Status flags from the api will depend on precedence; at least one
    job is in progress, at least one job is failed, at least one job is
    submitted, all jobs a completed.

    Args:
        context (Context): App runtime context.
        batch_id (str): Batch resource id to retrieve the status for.

    Returns:
        str: Batch status.
    """
    # request the batch status from the api controller and output a
    # status note depending on the returned flag.
    controller = RetroBatchController(context)
    status: BatchStatus = controller.retrieve_batch_status_by_batch_id(batch_id)
    if status == BatchStatus.COMPLETED:
        console.print("[success]✓ Batch was completed successfully.")
    elif status == BatchStatus.FAILED:
        console.print("[fail]Batch has failed, contact support for more information.")
    elif status == BatchStatus.PROCESSING:
        console.print("[warn]! Batch is currently in progress.")
    else:
        console.print("[warn]! Batch is waiting to be processed.")
    return status


# region command: result -----------------------------------------------


@app.command(
    "result",
    help=(
        "Retrieve a collection of results for all retrosynthesis batch "
        "jobs providing synthesizability screening information per "
        "job. Each entry informs about the job outcome and whether or "
        "not the query molecule can be synthesized with a job id to help "
        "retrieve more information or depict retrosynthetic routes."
    ),
    short_help="Get retrosynthesis screening results for a batch.",
)
def retrieve_batch_result_by_batch_id(
    context: Context,
    batch_id: typing.Annotated[
        str,
        typer.Argument(
            help="Unique batch id for retrieving screening results.",
            callback=batch_id_callback,
            metavar="BATCH_ID",
        ),
    ],
    output_file: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "--output-file",
            "-o",
            show_default=False,
            help=(
                "Specified JSON output file for writing results to. Defaults to "
                "an ISO-8601 formatted filename in the working directory."
            ),
            resolve_path=True,
            file_okay=True,
            writable=True,
            dir_okay=False,
        ),
    ] = pathlib.Path(f"batch_result_{datetime.now().isoformat('T', 'seconds')}.json"),
) -> None:
    """
    Retrieve results for a batch of retrosynthesis jobs. Coerce into the
    expected response format and then write to an output file in a json
    format reporting on additional metadata during the process.

    Args:
        context (Context): App runtime context.
        batch_id (str): Batch resource id to retrieve results for.
        output_file (pathlib.Path, optional): Output path to write json
            results to; confirms with user if overwriting an existing
            output filepath.

    Raises:
        typer.Exit: Overwriting file that already exists is stopped by
            the user from an input prompt.
        typer.Exit: No results are returned for the batch from the api
            controller layer.
    """
    controller = RetroBatchController(context)

    # first validate that the output file does not already exist and if
    # it does then confirm overwriting the file with the user and exit
    # if they decline the prompt.
    prompt: str = f"[warn][not b]! Are you sure you want to overwrite: {output_file}?"
    if output_file.exists() and not rich.prompt.Confirm.ask(prompt, console=console):
        raise typer.Exit(0)

    # don't retrieve results unless the batch is completed.
    status: BatchStatus = controller.retrieve_batch_status_by_batch_id(batch_id)
    if status not in [BatchStatus.COMPLETED, BatchStatus.FAILED]:
        console.print(
            "[warn]! Batch has not completed, try [code]pendingai retro "
            f"batch status {batch_id}[/code] to monitor its status."
        )
        raise typer.Exit(0)

    # retrieve the list of batch results for the batch id from the api
    # controller, check that at least one result was given in return and
    # then write results to a json file.
    result: list[BatchJobResult] = controller.retrieve_batch_result_by_batch_id(batch_id)
    if len(result) == 0:
        console.print("[warn]! No batch data was found.")
        raise typer.Exit(1)
    console.print(f"[success][not b]✓ Retrieved {len(result)} results successfully.")
    with open(output_file, "w") as fp:
        json.dump([x.model_dump(by_alias=True) for x in result], fp, indent=2)
    filesize: str = formatters.format_filesize(os.path.getsize(output_file))
    console.print(f"[success][not b]✓ Saved results to file: {output_file} ({filesize})")


# region command: list -------------------------------------------------


@app.command(
    "list",
    help=(
        "List all submitted batches in a paginated format. Provide an "
        "additional key to retrieve the next page of batches."
    ),
    short_help="List submitted retrosynthesis batches.",
)
def retrieve_batch_list(
    context: Context,
    pagination_key: typing.Annotated[
        str | None,
        typer.Option(
            "--pagination-key",
            help=(
                "Pagination batch id key for retrieving any batches "
                "that were submitted afterwards. If no key is "
                "provided, the first page of results will be returned "
                "with your next pagination key."
            ),
            callback=batch_id_callback,
        ),
    ] = None,
    page_size: typing.Annotated[
        int,
        typer.Option(
            "--page-size",
            help=(
                "Number of batches returned in the list; must be a multiple "
                "of 5. Defaults to 10."
            ),
            callback=page_size_callback,
            metavar="INTEGER",
            min=5,
            max=25,
            show_default=False,
        ),
    ] = 10,
) -> None:
    """
    Retrieve a paginated list of submitted batches for a user. Provide
    summary feedback of the page data and help with looking up the next
    offset for a new page.

    Args:
        context (Context): App runtime context.
        pagination_key (str, optional): Batch resource id that points to
            the offset location for the pagination lookup.
        page_size (int, optional): Number of batch resources returned by
            the page; requires a multiple of 5 in the range [5, 25].

    Raises:
        typer.Exit: No batch resources were returned in the page.
    """
    # request for the page of batch resources; exit if no batch data was
    # returned in the list with zero status.
    controller = RetroBatchController(context)
    batch_page: BatchPage = controller.retrieve_batch_list(pagination_key, page_size)
    if len(batch_page.data) == 0:
        console.print("[warn]! No batches found.")
        raise typer.Exit(0)

    # build rich table to summarise the batch resources in a minimal and
    # easy to read format; add each row to the table; paged batches are
    # also sorted in chronological descending order from when they were
    # created since page lookup returns batches after that point.
    table = rich.table.Table(
        rich.table.Column("Batch ID"),
        rich.table.Column("Created"),
        rich.table.Column("Tags", style="dim"),
        rich.table.Column("Jobs", justify="right"),
        box=rich.table.box.SQUARE,
    )
    batch_page.data.sort(key=lambda x: x.created_at, reverse=True)
    for batch in batch_page.data:
        table.add_row(
            batch.batch_id,
            formatters.localize_datetime(batch.created_at).isoformat(" ", "seconds"),
            ",".join(batch.tags),
            str(batch.number_of_jobs),
        )

    # output table with added data and a final extra line with next page
    # lookup key if there is more data that exists for the user.
    console.print(table)
    if len(batch_page.data) == page_size:
        console.print(
            "[warn][not b]! Retrieve the next page of batches using "
            f"'--pagination-key {batch_page.data[-1].batch_id}'"
        )


# region command: archive ----------------------------------------------


@app.command(
    "archive",
    help=(
        "Archive a batch and all encompassing retrosynthesis jobs. "
        "Batches cannot be archived when in progress, wait until it "
        "has completed before trying again."
    ),
    short_help="Archive a batch by id.",
)
def archive_batch(
    context: Context,
    batch_id: typing.Annotated[
        str,
        typer.Argument(
            help="Unique id of the batch being archived.",
            callback=batch_id_callback,
        ),
    ],
) -> None:
    """
    Archive a batch resource by id.

    Args:
        context (Context): App runtime context.
        batch_id (str): Batch resource id to be archived.

    Raises:
        typer.Exit: Batch resource id does not exist.
    """
    controller = RetroBatchController(context)
    controller.archive_batch(batch_id)
