#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import http

import httpx
import pydantic
import rich

from pendingai import config
from pendingai.api import ApiClient
from pendingai.commands.retro.models import BuildingBlockLibrary, RetrosynthesisEngine
from pendingai.context import Context

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)


class RetroController:
    """
    Controller for `pendingai retro` subcommands. Controls specific
    retrosynthesis operations for captured named commands in the app
    like retrieving engines and libraries or operating on tags.

    Args:
        context (Context): App runtime context.
    """

    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.api: ApiClient = ApiClient(
            base_url=config.API_BASE_URLS[self.context.obj.environment],
            subdomain=config.RETRO_SUBDOMAIN,
            bearer_token=self.context.obj.cache.access_token,
        )

    def retrieve_retrosynthesis_engines(self) -> list[RetrosynthesisEngine]:
        """
        Retrieve all retrosynthesis engine resources from the api layer
        and coerce into the expected data model. Ignore any items that
        do not validate correctly.

        Returns:
            list[RetrosynthesisEngine]: Retrosynthesis engines.
        """
        # provide a spinner to show the request is being made to get all
        # retrosynthesis engines from the api client.
        retrosynthesis_engines: list[RetrosynthesisEngine] = []
        with console.status("Retrieving retrosythesis engines..."):
            r: httpx.Response = self.api.get("/engines")

        if r.status_code == http.HTTPStatus.OK and isinstance(r.json(), list):
            # iterate over each response list resource item, validate
            # against the required pydantic model and append to the
            # response list; ignore any that raise an exception.
            for item in r.json():
                try:
                    o: RetrosynthesisEngine = RetrosynthesisEngine.model_validate(item)
                    retrosynthesis_engines.append(o)
                except pydantic.ValidationError:
                    continue

        return retrosynthesis_engines

    def retrieve_building_block_libraries(self) -> list[BuildingBlockLibrary]:
        """
        Retrieve all building block library resources from the api layer
        and coerce into the expected data model. Ignore any items that
        do not validate correctly.

        Returns:
            list[BuildingBlockLibrary]: Building block libraries.
        """
        # provide a spinner to show the request is being made to get all
        # building block libraries from the api client.
        building_block_libraries: list[BuildingBlockLibrary] = []
        with console.status("Retrieving building block libraries..."):
            r: httpx.Response = self.api.get("/libraries")

        if r.status_code == http.HTTPStatus.OK and isinstance(r.json(), list):
            # iterate over each response list resource item, validate
            # against the required pydantic model and append to the
            # response list; ignore any that raise an exception.
            for item in r.json():
                try:
                    o: BuildingBlockLibrary = BuildingBlockLibrary.model_validate(item)
                    building_block_libraries.append(o)
                except pydantic.ValidationError:
                    continue

        return building_block_libraries

    def retrieve_tags(self) -> list[str]:
        """
        Retrieve all unique retrosynthesis job tags belonging to a user
        in the database.

        Returns:
            list[str]: Unique retrosynthesis job tags.
        """
        # provide a spinner status while performing the api request to
        # give feedback to the user when a request may be taking longer
        # than expected; this is a high load request.
        with console.status("Retrieving retrosynthesis job tags..."):
            r: httpx.Response = self.api.get("/query_tags")
        if r.status_code == http.HTTPStatus.OK:
            return sorted(r.json())
        return []

    def retrieve_tag_count(self, tag: str) -> int:
        """
        Count all retrosynthesis jobs that contains the matching tag.
        The job can contain other tags also. Yield the number counted.

        Args:
            tag (str): Tag to retrieve a count for.

        Returns:
            int: Number of matched jobs with the tag.
        """
        # provide a spinner status while performing the api request to
        # give feedback to the user when a request may be taking longer
        # than expected; this is a high load request.
        with console.status(f"Finding jobs with tag: '{tag}'..."):
            r: httpx.Response = self.api.get(f"/query_tags/{tag}/count")
        if r.status_code == http.HTTPStatus.OK:
            return r.json().get("count", 0)
        return 0

    def delete_tag(self, tag: str) -> int:
        """
        Delete all retrosynthesis jobs that contains the matching tag.
        The job can contain other tags also. Yield the number deleted.

        Args:
            tag (str): Tag to delete jobs from.

        Returns:
            int: Number of deleted jobs with the tag.
        """
        # provide a spinner status while performing the api request to
        # give feedback to the user when a request may be taking longer
        # than expected; this is a high load request.
        with console.status(f"Deleting jobs with tag: '{tag}'..."):
            r: httpx.Response = self.api.delete(f"/query_tags/{tag}")
        if r.status_code == http.HTTPStatus.OK:
            return r.json().get("count", 0)
        return 0
