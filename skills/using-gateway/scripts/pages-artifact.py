#!/usr/bin/env python3
"""Prepare deterministic Gateway Pages archives and read MCP-sized chunks."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import tarfile
import tempfile

CHUNK_MAX = 1024 * 1024


def fail(message: str) -> None:
    raise SystemExit(message)


def normalized_info(info: tarfile.TarInfo, executable: bool = False) -> tarfile.TarInfo:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    info.mode = 0o755 if info.isdir() or executable else 0o644
    return info


def iter_entries(source: Path):
    for root, dirnames, filenames in os.walk(source, followlinks=False):
        dirnames.sort()
        filenames.sort()
        root_path = Path(root)
        for dirname in dirnames:
            path = root_path / dirname
            if path.is_symlink():
                fail(f"Refusing symlink in Pages artifact: {path}")
            yield path
        for filename in filenames:
            path = root_path / filename
            if path.is_symlink():
                fail(f"Refusing symlink in Pages artifact: {path}")
            if not path.is_file():
                fail(f"Refusing non-regular file in Pages artifact: {path}")
            yield path


def prepare(source_arg: str, output_arg: str) -> None:
    source = Path(source_arg).expanduser().resolve()
    if not source.is_dir():
        fail(f"Pages source directory does not exist: {source}")
    output = Path(output_arg).expanduser().resolve()
    if output == source or source in output.parents:
        fail("Pages archive output must be outside the source directory")
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".gateway-pages-", delete=False) as handle:
        temporary = Path(handle.name)
    file_count = 0
    try:
        with temporary.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                    for path in iter_entries(source):
                        relative = path.relative_to(source).as_posix()
                        stat = path.stat()
                        info = normalized_info(
                            archive.gettarinfo(str(path), arcname=relative), executable=bool(stat.st_mode & 0o111)
                        )
                        if path.is_dir():
                            archive.addfile(info)
                        else:
                            file_count += 1
                            with path.open("rb") as item:
                                archive.addfile(info, item)
        if file_count == 0:
            fail("Pages source directory contains no files")
        temporary.replace(output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    digest = hashlib.sha256()
    size = 0
    with output.open("rb") as archive_file:
        while block := archive_file.read(CHUNK_MAX):
            size += len(block)
            digest.update(block)
    if size < 1:
        fail("Pages archive is empty")
    print(json.dumps({"archive": str(output), "size": size, "sha256": digest.hexdigest()}))


def chunk(archive_arg: str, offset: int, size: int) -> None:
    archive = Path(archive_arg).expanduser().resolve()
    if not archive.is_file():
        fail(f"Pages archive does not exist: {archive}")
    total = archive.stat().st_size
    if offset < 0 or offset > total:
        fail(f"Offset {offset} is outside archive size {total}")
    if size < 1 or size > CHUNK_MAX:
        fail(f"Chunk size must be between 1 and {CHUNK_MAX}")
    with archive.open("rb") as handle:
        handle.seek(offset)
        data = handle.read(size)
    next_offset = offset + len(data)
    print(json.dumps({
        "offset": offset,
        "nextOffset": next_offset,
        "eof": next_offset >= total,
        "contentBase64": base64.b64encode(data).decode("ascii"),
    }))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Create a deterministic tar.gz archive")
    prepare_parser.add_argument("source")
    prepare_parser.add_argument("--output", required=True)

    chunk_parser = subparsers.add_parser("chunk", help="Read one base64-encoded MCP upload chunk")
    chunk_parser.add_argument("archive")
    chunk_parser.add_argument("--offset", type=int, required=True)
    chunk_parser.add_argument("--size", type=int, default=CHUNK_MAX)

    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.source, args.output)
    else:
        chunk(args.archive, args.offset, args.size)


if __name__ == "__main__":
    main()
