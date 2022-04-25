import os

class RemoveFile:
    async def remove_file(path: str) -> None:
        os.unlink(path)