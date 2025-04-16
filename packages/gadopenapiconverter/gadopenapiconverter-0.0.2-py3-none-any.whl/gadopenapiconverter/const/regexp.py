import re

REGEXP_CLASS_DEFINITION = re.compile(r"class\s+([A-Za-z0-9_]+)\s*[\(:]")
REGEXP_NON_ALPHANUMERIC = re.compile(r"[^a-zA-Z0-9]")
REGEXP_SEPARATOR = re.compile(r"[\s_\-]+")
REGEXP_IMPORT = re.compile(r"^\s*(import |from )")
