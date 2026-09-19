"""Read-only Windows file allocation inventory. Exit 2 means partial evidence."""

import argparse
import csv
import ctypes
from ctypes import wintypes
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import time

REPARSE = 0x400
OFFLINE_OR_RECALL = 0x1000 | 0x40000 | 0x400000
COMPRESSED_OR_SPARSE = 0x800 | 0x200
FIELDS = ("logical", "allocated_entries", "allocated_unique", "files", "estimated_bytes", "unknown_identity_files")


def stamp() -> str:
    return datetime.now().astimezone().isoformat()


def io_path(path: str) -> str:
    return path if path.startswith("\\\\?\\") else "\\\\?\\" + path


def inside(path: str, parent: str) -> bool:
    try:
        return os.path.normcase(os.path.commonpath([path, parent])) == os.path.normcase(parent)
    except ValueError:
        return False


def checked_path(value: str, must_exist: bool) -> str:
    path = Path(os.path.abspath(os.path.expanduser(value)))
    if str(path).startswith("\\\\"):
        raise ValueError("Use local drive paths, not UNC or extended-prefix input paths.")
    for part in [path, *path.parents]:
        try:
            meta = os.lstat(io_path(str(part)))
        except FileNotFoundError:
            if part == path and must_exist:
                raise
            continue
        if getattr(meta, "st_file_attributes", 0) & REPARSE:
            raise ValueError(f"Redirected path is not accepted: {part}")
    if must_exist and not os.path.isdir(io_path(str(path))):
        raise ValueError(f"Scan root is not a directory: {path}")
    return str(path)


class StandardInfo(ctypes.Structure):
    _fields_ = [("allocated", ctypes.c_longlong), ("end", ctypes.c_longlong),
                ("links", wintypes.DWORD), ("pending", ctypes.c_ubyte), ("directory", ctypes.c_ubyte)]


class WindowsAllocation:
    def __init__(self) -> None:
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.open = kernel.CreateFileW
        self.open.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                              wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        self.open.restype = wintypes.HANDLE
        self.info = kernel.GetFileInformationByHandleEx
        self.info.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.info.restype = wintypes.BOOL
        self.close = kernel.CloseHandle
        self.close.argtypes = [wintypes.HANDLE]
        self.compressed = kernel.GetCompressedFileSizeW
        self.compressed.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
        self.compressed.restype = wintypes.DWORD

    def read(self, path: str, attributes: int) -> int:
        native = io_path(path)
        if attributes & COMPRESSED_OR_SPARSE:
            high = wintypes.DWORD()
            ctypes.set_last_error(0)
            low = self.compressed(native, ctypes.byref(high))
            error = ctypes.get_last_error()
            if low == 0xFFFFFFFF and error:
                raise ctypes.WinError(error)
            return (high.value << 32) | low
        handle = self.open(native, 0, 7, None, 3, 0x02200000, None)
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            info = StandardInfo()
            if not self.info(handle, 1, ctypes.byref(info), ctypes.sizeof(info)):
                raise ctypes.WinError(ctypes.get_last_error())
            return max(info.allocated, 0)
        finally:
            self.close(handle)


def disk_snapshot(roots: list[str]) -> list[dict]:
    records = []
    for anchor in sorted({Path(p).anchor for p in roots}):
        try:
            usage = shutil.disk_usage(anchor)
            records.append({"root": anchor, "time": stamp(), "total": usage.total, "used": usage.used, "free": usage.free})
        except OSError as error:
            records.append({"root": anchor, "time": stamp(), "error": str(error)})
    return records


def scan(roots: list[str], output: str, large_bytes: int) -> dict:
    allocation = WindowsAllocation()
    counters = {"files": 0, "directories": 0, "errors": 0, "skipped_entries": 0, "duplicate_hardlinks": 0}
    seen_links: set[tuple[int, int]] = set()
    root_totals = {}
    before = disk_snapshot(roots)
    started = stamp()
    last_progress = time.monotonic()
    out = Path(output)
    handles = []

    def writer(name: str, header: list[str]):
        stream = open(io_path(str(out / name)), "w", encoding="utf-8-sig", newline="")
        handles.append(stream)
        result = csv.writer(stream)
        result.writerow(header)
        return result

    try:
        directories = writer("directories.csv", ["path", *FIELDS, "direct_logical", "direct_allocated", "direct_unique", "direct_files"])
        large = writer("large-files.csv", ["path", "logical", "allocated", "allocated_unique", "links", "file_id", "modified", "attributes", "estimated"])
        errors = writer("errors.csv", ["path", "operation", "error"])
        skipped = writer("skipped.csv", ["path", "reason", "logical", "attributes"])

        def failure(path: str, operation: str, error: object) -> None:
            counters["errors"] += 1
            errors.writerow([path, operation, str(error)])

        for root in roots:
            # One frame per open directory; totals propagate when each iterator ends.
            stack = []

            def descend(path: str) -> None:
                counters["directories"] += 1
                totals, direct = [0] * len(FIELDS), [0] * len(FIELDS)
                try:
                    iterator = os.scandir(io_path(path))
                except OSError as error:
                    failure(path, "enumerate", error)
                    iterator = iter(())
                stack.append([path, iterator, totals, direct])

            descend(root)
            while stack:
                path, iterator, totals, direct = stack[-1]
                try:
                    entry = next(iterator)
                except (StopIteration, OSError) as error:
                    if isinstance(error, OSError):
                        failure(path, "enumerate", error)
                    if hasattr(iterator, "close"):
                        iterator.close()
                    combined = [a + b for a, b in zip(totals, direct)]
                    directories.writerow([path, *combined, *direct[:4]])
                    stack.pop()
                    if stack:
                        stack[-1][2][:] = [a + b for a, b in zip(stack[-1][2], combined)]
                    else:
                        root_totals[root] = dict(zip(FIELDS, combined))
                    continue
                current = os.path.join(path, entry.name)
                if inside(current, output):
                    continue
                if time.monotonic() - last_progress >= 10:
                    print(json.dumps({"time": stamp(), "current": current, **counters}, ensure_ascii=False), flush=True)
                    last_progress = time.monotonic()
                try:
                    meta = os.stat(io_path(current), follow_symlinks=False)
                    attrs = getattr(meta, "st_file_attributes", 0)
                    if attrs & (REPARSE | OFFLINE_OR_RECALL):
                        counters["skipped_entries"] += 1
                        skipped.writerow([current, "reparse-or-offline", meta.st_size, attrs])
                        continue
                    if attrs & 0x10:
                        descend(current)
                        continue
                    estimated = 0
                    try:
                        allocated = allocation.read(current, attrs)
                    except OSError as error:
                        # Logical length is a labelled estimate, never a physical claim.
                        allocated = meta.st_size
                        estimated = allocated
                        failure(current, "allocation-estimated-from-logical", error)
                    unknown_identity = int(not meta.st_ino or not meta.st_nlink)
                    if unknown_identity:
                        failure(current, "identity", "File identity/link count unavailable; deduplication may be incomplete")
                    identity = (meta.st_dev, meta.st_ino)
                    unique = allocated
                    if meta.st_nlink > 1 and not unknown_identity:
                        if identity in seen_links:
                            unique = 0
                            counters["duplicate_hardlinks"] += 1
                        seen_links.add(identity)
                    values = [meta.st_size, allocated, unique, 1, estimated if unique else 0, unknown_identity]
                    direct[:] = [a + b for a, b in zip(direct, values)]
                    counters["files"] += 1
                    if max(meta.st_size, allocated) >= large_bytes:
                        large.writerow([current, meta.st_size, allocated, unique, meta.st_nlink,
                                        f"{meta.st_dev}:{meta.st_ino}", datetime.fromtimestamp(meta.st_mtime).isoformat(), attrs, bool(estimated)])
                except OSError as error:
                    failure(current, "metadata", error)
    finally:
        for handle in handles:
            handle.close()
    after = disk_snapshot(roots)
    partial = bool(counters["errors"] or counters["skipped_entries"] or any("error" in d for d in before + after))
    summary = {"schema": 1, "started": started, "finished": stamp(), "partial": partial,
               "roots": root_totals, "counts": counters, "before": before, "after": after,
               "method": "Metadata only; StandardInfo allocation, compressed/sparse size API, global hardlink identity dedup; reparse/offline entries excluded; estimated bytes separately labelled.",
               "limitations": "Not a volume snapshot. Root totals omit filesystem metadata, alternate streams, unreadable files and skipped entries. Hardlinks are attributed to the first enumerated entry, not necessarily reclaimable by deleting that subtree."}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="Outputs: directories.csv, large-files.csv, errors.csv, skipped.csv, summary.json. Exit 0: enumerated scope complete; 2: partial coverage; 1: invalid input or fatal failure.")
    parser.add_argument("--root", action="append", required=True, help="Explicit local directory, repeatable; overlapping or redirected roots are rejected")
    parser.add_argument("--output", required=True, help="New output directory; excluded when inside a scan root")
    parser.add_argument("--large-mib", type=float, default=32, help="Large-file threshold, default 32 MiB")
    args = parser.parse_args()
    if os.name != "nt":
        parser.error("This scanner requires Windows.")
    output = None
    reserved = False
    try:
        if not 0 <= args.large_mib < float("inf"):
            raise ValueError("--large-mib must be a finite nonnegative number")
        roots = [checked_path(p, True) for p in args.root]
        for i, root in enumerate(roots):
            if any(inside(root, other) or inside(other, root) for other in roots[:i]):
                raise ValueError("Roots overlap or are duplicated")
        output = checked_path(args.output, False)
        if os.path.lexists(io_path(output)):
            raise ValueError("Output already exists; choose a new snapshot directory")
        if any(inside(root, output) for root in roots):
            raise ValueError("Output cannot contain a scan root")
        os.makedirs(io_path(output), exist_ok=False)
        reserved = True
        summary = scan(roots, output, int(args.large_mib * 1024 * 1024))
        print(json.dumps({"output": output, "partial": summary["partial"], **summary["counts"]}, ensure_ascii=False))
        return 2 if summary["partial"] else 0
    except (OSError, ValueError) as error:
        if reserved:
            (Path(output) / "fatal.json").write_text(json.dumps({"time": stamp(), "error": str(error), "partial": True}), encoding="utf-8")
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
