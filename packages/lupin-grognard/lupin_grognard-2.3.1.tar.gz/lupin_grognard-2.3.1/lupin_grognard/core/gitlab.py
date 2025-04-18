import os


def is_merge_request_event() -> bool:
    return os.getenv("CI_PIPELINE_SOURCE") == "merge_request_event"
