import hashlib
import pickle
import subprocess


def append_to(item, bucket=[]):
    bucket.append(item)
    return bucket


def ok_append(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


class Point:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return self.x == other.x


class Hashable:
    def __eq__(self, other):
        return True

    def __hash__(self):
        return 1


def checks(value, names):
    if value == None:
        pass
    if value == True:
        pass
    if value is "abc":
        pass
    try:
        risky()
    except:
        pass
    try:
        risky()
    except Exception:
        pass
    for n in names:
        if n == "x":
            names.remove(n)
    for k in list(names):
        names.remove(k)


def finals():
    for i in range(3):
        try:
            risky()
        finally:
            continue


def dangerous(user_text, blob):
    eval(user_text)
    pickle.loads(blob)
    subprocess.run(user_text, shell=True)
    return hashlib.md5(b"x").hexdigest()


def risky():
    pass


def shadowed():
    try:
        open("x")
    except Exception:
        pass
    except FileNotFoundError:
        pass
    try:
        open("y")
    except FileNotFoundError:
        pass
    except OSError:
        pass
    try:
        open("z")
    except (KeyError, OSError):
        pass
    except PermissionError:
        pass
