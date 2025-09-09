from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Whether to keep unparseable date strings in the final output (default: False -> drop them)
    ALLOW_INVALID: bool = True
    # If True, collapse duplicates after normalisation
    DEDUPLICATE: bool = True

settings = Settings()
