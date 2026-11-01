# -*- coding: utf-8 -*-
"""
Runs the DETERMINISTIC test cases of the scripts (lookup, linter, command validator)
and, optionally, the citation verifier. No network.
Uso: python -I tests/run_script_tests.py [--dockhb <txt>] [--k8sb <txt>]
     (copy outside the package: set the PKG_DIR environment variable to the package folder)
Output: PASS/FAIL per case; exit code 1 if any fails.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(os.environ.get("PKG_DIR", os.path.dirname(HERE)), "scripts")  # PKG_DIR: package folder (use when running the copy in _agents_tests)


def run(script, args, stdin=None):
    p = subprocess.run([sys.executable, "-I", os.path.join(S, script)] + args, input=stdin, capture_output=True,
                       text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


BAD = """FROM ubuntu
RUN apt-get update && apt-get install build-essential libpcre3-dev -y
ADD ./src.tar.gz /src
COPY . .
RUN npm install
RUN apt-get remove build-essential -y
ENV DB_PASSWORD=secret
CMD npm start
"""
GOOD = """# stage one
FROM node:lts-alpine as builder
RUN apk add --no-cache python make g++
WORKDIR /app
COPY ./package.json .
RUN npm install --only=prod
# stage two
FROM node:lts-alpine
EXPOSE 3000
ENV NODE_ENV=production
USER node
RUN mkdir -p /home/node/app
WORKDIR /home/node/app
COPY . .
COPY --from=builder /app/node_modules  /home/node/app/node_modules
CMD [ "node", "bin/www" ]
"""

CASES = [
    # (id, script, args, stdin, must_contain, must_not_contain, expected_exit)
    ("S01", "docker_lookup.py", ["multi-stage"], None, ["DOCKHB p.97-98", "COPY --from=builder"], [], 0),
    ("S02", "docker_lookup.py", ["healthcheck"], None, ["NOT COVERED DIRECTLY", "HEALTHCHECK"], ["DOCKHB p."], 0),
    ("S03", "docker_lookup.py", ["twelve-factor"], None, ["unusable source", "extrapolation"], [], 0),
    ("S04", "docker_lookup.py", ["kubectl pods"], None, ["K8SB p.1", "NOT IN THE SOURCE"], [], 0),
    ("S05", "docker_lookup.py", ["xyzzy-inexistente"], None, ["NOT COVERED"], [], 0),
    ("S06", "docker_lookup.py", ["rede dns bridge"], None, ["user-defined bridge", "DOCKHB p.106-107"], [], 0),
    ("S07", "docker_lookup.py", ["compose"], None, ["[DATED]", "p.129"], [], 0),
    ("S08", "dockerfile_lint.py", ["-"], BAD, ["DF003", "DF007", "DF015", "DF002", "DF005", "DF009", "DOCKHB p.75"], [], 1),
    ("S09", "dockerfile_lint.py", ["-"], GOOD, ["100/100", "No findings"], ["DF0"], 0),
    ("S10", "dockerfile_lint.py", ["-"], "RUN echo oi\n", ["DF001"], [], 1),
    ("S11", "docker_cmd_check.py", ["docker container run fhsinchy/hello-dock --publish 8080:80"], None, ["AFTER the image name", "DOCKHB p.32"], [], 0),
    ("S12", "docker_cmd_check.py", ["docker run -p abc:80 nginx"], None, ["[ERROR]", "DOCKHB p.31"], [], 1),
    ("S13", "docker_cmd_check.py", ["docker container run --rm -v ./data:/zone img"], None, ["relative", "DOCKHB p.51"], [], 1),
    ("S14", "docker_cmd_check.py", ["docker run ubuntu"], None, ["without -it", "DOCKHB p.45-46"], [], 0),
    ("S15", "docker_cmd_check.py", ["docker run -it ubuntu"], None, ["Legacy short form"], ["without -it", "together"], 0),
    ("S16", "docker_cmd_check.py", ["docker-compose down --volumes"], None, ["[DATED]", "REMOVES the named volumes", "DOCKHB p.140"], [], 0),
    ("S17", "docker_cmd_check.py", ["docker compose up -d"], None, ["extrapolation"], ["[ERROR]"], 0),
    ("S18", "docker_cmd_check.py", ["docker container prune"], None, ["Destructive", "DOCKHB p.42"], [], 0),
    ("S19", "docker_cmd_check.py", ["docker kubectl get pods"], None, ["outside what the book covers"], [], 0),
    ("S20", "docker_cmd_check.py", ["docker image push custom-nginx:latest"], None, ["<user>/", "DOCKHB p.84"], [], 0),
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dockhb")
    ap.add_argument("--k8sb")
    a = ap.parse_args()
    fails = 0
    for cid, script, args, stdin, must, mustnot, code in CASES:
        rc, out = run(script, args, stdin)
        problems = [m for m in must if m not in out] + [f"forbidden:{m}" for m in mustnot if m in out]
        if rc != code:
            problems.append(f"exit {rc} != {code}")
        print(f"{'PASS' if not problems else 'FAIL'} {cid} {script} {args if len(str(args)) < 70 else args[0][:60]}")
        if problems:
            fails += 1
            print("     ", problems)
    if a.dockhb and a.k8sb:
        rc, out = run("verify_citations.py", ["--dockhb", a.dockhb, "--k8sb", a.k8sb])
        ok = rc == 0 and "Failures: 0" in out
        print(f"{'PASS' if ok else 'FAIL'} V01 verify_citations.py :: {out.strip().splitlines()[-1]}")
        fails += 0 if ok else 1
    print(f"\nSummary: {len(CASES)} script cases; failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
