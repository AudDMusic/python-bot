# super lazy reader implementation $noqa$
import sys
import os
import re


def _read_env(env=".env"):
    try:
        with open(env) as f:
            content = f.read()
    except IOError:
        content = ""

    for line in content.splitlines():
        m1 = re.match(r"\A([A-Za-z_0-9]+)=(.*)\Z", line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r"\\(.)", r"\1", m3.group(1))
            os.environ.setdefault(key, val)


def read_argv():
    script, *flags = sys.argv

    if flags and flags[0] == "--env":
        file = ".env"
        if len(flags) == 2:
            file = flags[1]
        if os.path.exists(file):
            _read_env(file)

        else:
            raise FileNotFoundError("Environment file was not found")
