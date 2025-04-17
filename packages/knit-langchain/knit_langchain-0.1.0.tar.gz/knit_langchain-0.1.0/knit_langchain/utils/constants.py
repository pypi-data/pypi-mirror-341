from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version("knit-langchain")
except PackageNotFoundError:
    VERSION = "NA"

ENVIRONMENT_SANDBOX = "sandbox"
ENVIRONMENT_PRODUCTION = "production"
ENVIRONMENT_LOCAL = "local"
