#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Manages globally cached variables."""


__all__ = ["Cache"]


import os
import os.path
import warnings

import yaml


class YamlNoAliasDumper(yaml.SafeDumper):
    """YAML Dumper that does not write out aliases and anchors."""

    def ignore_aliases(self, data):
        return True


class Cache:
    """
    Global object holding variables cached in-between runs.

    Tries to load cache file from YAML files in default locations
    (/var/cache/{module}.yml, ~/.cache/{module}.yml,
    %LOCALAPPDATA%/{module}.yml, ${XDG_CACHE_HOME}/{module}.yml).

    """

    def __init__(self, cache=None, cache_file_basename=None):
        """Initialise a Cache object, load cache from file."""
        self._cache = {}

        if cache_file_basename is None:
            cache_file_basename = self.__module__.split(".")[0]

        self._cache_file = os.path.abspath(
            os.path.join(
                (
                    os.environ.get("LOCALAPPDATA")
                    or os.environ.get("XDG_CACHE_HOME")
                    or os.path.join(os.environ["HOME"], ".cache")
                ),
                f"{cache_file_basename}.yml",
            )
        )

        self._cache = self._load_cache()
        if cache is not None:
            self._cache.update(cache)

    def _load_cache(self):
        cache = {}

        try:
            cache.update(yaml.safe_load(open(self._cache_file, "r", encoding="utf-8")))
        except FileNotFoundError:
            pass

        if cache == {}:
            warnings.warn(f"No cache found in file {self._cache_file}, starting empty")

        return cache

    def _save_cache(self):
        try:
            yaml.dump(
                self._cache,
                open(self._cache_file, "w", encoding="utf-8"),
                Dumper=YamlNoAliasDumper,
            )
        except PermissionError:
            warnings.warn(f"Could not write cache to {self._cache_file}")

    def __getitem__(self, pos):
        """Retrieve a cache entry."""
        return self._cache[pos]

    def __setitem__(self, pos, value):
        """Set the value of a cache entry."""
        self._cache[pos] = value
        self._save_cache()  # don’t rely on this!
        # if you update items inside a dict,
        # __setitem__ is not called
        #
        # rather, use the context manager:
        # ```
        # with Cache() as cache:
        #     cache["key1"]["key2"] = "value"

    def __delitem__(self, pos):
        """Delete a cache entry."""
        del self._cache[pos]
        self._save_cache()

    def __iter__(self):
        """Iterate over all entries in the cache."""
        return iter(self._cache)

    def __enter__(self):
        """Enter cache context."""
        self._load_cache()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit cache context."""
        self._save_cache()
