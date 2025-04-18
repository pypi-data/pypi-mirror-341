"""
通用工具函数
"""

from collections import Counter
from typing import Any, List

from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository
from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository


def is_artifact_uri(uri):
    """
    Checks the artifact URI is associated with a MLflow model or run.
    The actual URI can be a model URI, model URI + subdirectory, or model URI + path to artifact file.
    """
    return ModelsArtifactRepository.is_models_uri(
        uri
    ) or RunsArtifactRepository.is_runs_uri(uri)

def as_list(obj, default=None):
    if not obj:
        return default
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

def get_duplicates(elements: List[Any]) -> List[Any]:
    """
    Returns duplicate elements in the order they first appear.
    """
    element_counts = Counter(elements)
    duplicates = []
    for e in element_counts.keys():
        if element_counts[e] > 1:
            duplicates.append(e)
    return duplicates

def validate_strings_unique(strings: List[str], error_template: str):
    """
    Validates all strings are unique, otherwise raise ValueError with the error template and duplicates.
    Passes single-quoted, comma delimited duplicates to the error template.
    """
    duplicate_strings = get_duplicates(strings)
    if duplicate_strings:
        duplicates_formatted = ", ".join([f"'{s}'" for s in duplicate_strings])
        raise ValueError(error_template.format(duplicates_formatted))

def sanitize_identifier(identifier: str):
    """
    Sanitize and wrap an identifier with backquotes. For example, "a`b" becomes "`a``b`".
    Use this function to sanitize identifiers such as column names in SQL and PySpark.
    """
    return f"`{identifier.replace('`', '``')}`"


def sanitize_identifiers(identifiers: List[str]):
    """
    Sanitize and wrap the identifiers in a list with backquotes.
    """
    return [sanitize_identifier(i) for i in identifiers]


def sanitize_multi_level_name(multi_level_name: str):
    """
    Sanitize a multi-level name (such as an Unity Catalog table name) by sanitizing each segment
    and joining the results. For example, "ca+t.fo`o.ba$r" becomes "`ca+t`.`fo``o`.`ba$r`".
    """
    segments = multi_level_name.split(".")
    return ".".join(sanitize_identifiers(segments))


def unsanitize_identifier(identifier: str):
    """
    Unsanitize an identifier. Useful when we get a possibly sanitized identifier from Spark or
    somewhere else, but we need an unsanitized one.
    Note: This function does not check the correctness of the identifier passed in. e.g. `foo``
    is not a valid sanitized identifier. When given such invalid input, this function returns
    invalid output.
    """
    if len(identifier) >= 2 and identifier[0] == "`" and identifier[-1] == "`":
        return identifier[1:-1].replace("``", "`")
    else:
        return identifier


# strings containing \ or ' can break sql statements, so escape them.
def escape_sql_string(input_str: str) -> str:
    return input_str.replace("\\", "\\\\").replace("'", "\\'")

def get_unique_list_order(elements: List[Any]) -> List[Any]:
    """
    Returns unique elements in the order they first appear.
    """
    return list(dict.fromkeys(elements))