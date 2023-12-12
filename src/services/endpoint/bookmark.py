from functools import lru_cache


# TODO:
#   1. Add dependencies via Depends()
#   2. dependencies types must be abstract
#   3. inject on dependencies getter
#   4. Initiate Orchestrator here
@lru_cache()
def get_bookmark_service() -> None:
    raise NotImplementedError
