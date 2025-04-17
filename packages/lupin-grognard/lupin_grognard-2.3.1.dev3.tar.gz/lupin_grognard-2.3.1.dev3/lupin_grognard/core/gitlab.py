import os


def is_gitlab_ci() -> bool:
    return os.getenv("CI") == "true"


def is_merge_request_event() -> bool:
    return os.getenv("CI_PIPELINE_SOURCE") == "merge_request_event"


def is_ci_commit_tag() -> bool:
    return os.getenv("CI_COMMIT_TAG") is not None


def get_current_branch_name_from_gitlab_ci() -> str:
    if not is_gitlab_ci():
        return ""

    return (
        os.getenv("CI_COMMIT_BRANCH") or
        os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME") or
        ""
    )