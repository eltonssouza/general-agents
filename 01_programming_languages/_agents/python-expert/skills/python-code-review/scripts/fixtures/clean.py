"""Fixture with no point of attention: the scanner must report nothing."""
import json


def append_to(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


class Point:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x

    def __hash__(self):
        return hash(self.x)


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except ValueError as exc:
        raise RuntimeError("invalid json") from exc


def drop_even(values):
    return [v for v in values if v % 2]


def cleanup_with_inner_loop(items):
    try:
        return len(items)
    finally:
        # break/continue of a loop INSIDE the finally do not leave the finally: not a finding
        for i in items:
            if i:
                break
            continue

        def helper():
            return 1  # return of a nested function is not a finding

        helper()
