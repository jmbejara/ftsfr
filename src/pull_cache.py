import sys
from pathlib import Path

import gdown

from settings import config

DATA_DIR = config("DATA_DIR")
CACHE_URL = config("CACHE_URL")


# Custom exception for download errors
class DownloadError(Exception):
    pass


def pull_cache(cache_url: str = CACHE_URL, data_dir: Path = DATA_DIR):
    """
    Uses gdown to recursively download files and folders from a Google Drive
    folder URL into the local data directory.

    Requires the 'gdown' library (`pip install gdown`).

    Args:
        cache_url: The URL of the Google Drive folder.
        data_dir: The local directory to download contents *into*.
                  gdown will likely create a subfolder named after the
                  Drive folder within this directory.
    """
    # Ensure the target parent directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting download from Google Drive folder: {cache_url} -> {data_dir}")

    try:
        # Execute the gdown download.
        downloaded_paths = gdown.download_folder(
            url=cache_url,
            output=str(data_dir),
            quiet=True,  # Set quiet=True to minimize gdown's own progress output
            use_cookies=True # Set to True to attempt using browser cookies
        )

        if not downloaded_paths:
            # gdown might return an empty list even on success with quiet=True,
            # or if the folder was empty. Let's rely on exceptions for failure.
            print(f"gdown download process completed. Check '{data_dir}' for contents.")
            # Consider adding a check here if knowing the exact downloaded folder name is critical.
        else:
            print(
                f"gdown download process completed. {len(downloaded_paths)} files/folders processed."
            )

        # --- Zipping logic removed ---

    except Exception as e:
        # Catch potential gdown errors or other issues during download
        print(f"Error during gdown download from {cache_url}: {e}", file=sys.stderr)
        raise DownloadError(
            f"Cache pull failed for {cache_url}. See error details above."
        ) from e


if __name__ == "__main__":
    # Example usage: Just pull the folder contents.
    try:
        pull_cache(cache_url=CACHE_URL, data_dir=DATA_DIR)
        print(
            f"\nCache pull finished successfully. Contents should be in '{DATA_DIR}'."
        )
    except DownloadError as e:
        print(f"\nError during cache pull: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
