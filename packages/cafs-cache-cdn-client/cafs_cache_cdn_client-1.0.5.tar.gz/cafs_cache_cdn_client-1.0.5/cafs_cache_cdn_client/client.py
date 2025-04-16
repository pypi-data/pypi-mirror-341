import asyncio
import functools
from collections.abc import Awaitable, Callable
from os.path import normpath
from pathlib import Path
from typing import Any, Self, TypeVar

import aiofiles.os as aio_os

from cafs_cache_cdn_client.cafs import CAFSClient
from cafs_cache_cdn_client.file_utils import (
    LocalFile,
    compare_file_lists,
    set_file_stat,
    walk,
)
from cafs_cache_cdn_client.repo import RepoClient

__all__ = ('CacheCdnClient',)


CAFS_SERVER_ROOT = '/cache'


T = TypeVar('T')


def needs_cafs_client(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @functools.wraps(func)
    async def wrapper(self: 'CacheCdnClient', *args: Any, **kwargs: Any) -> T:
        await self._init_cafs_client()
        return await func(self, *args, **kwargs)

    return wrapper


class CacheCdnClient:
    _cafs_client: CAFSClient | None = None
    _repo_client: RepoClient

    __connection_per_cafs_server: int
    __cafs_client_lock = asyncio.Lock()

    def __init__(self, server: str, connection_per_cafs_server: int = 1) -> None:
        self._repo_client = RepoClient(server)
        self.__connection_per_cafs_server = connection_per_cafs_server

    async def _init_cafs_client(self) -> None:
        async with self.__cafs_client_lock:
            if self._cafs_client:
                return
            blob_urls = await self._repo_client.get_blob_urls()
            self._cafs_client = await CAFSClient(
                CAFS_SERVER_ROOT,
                blob_urls,
                connection_per_server=self.__connection_per_cafs_server,
            ).__aenter__()

    @needs_cafs_client
    async def push(
        self,
        repo: str,
        ref: str,
        directory: Path | str,
        ttl_hours: int = 0,
        comment: str | None = None,
    ) -> None:
        if isinstance(directory, str):
            directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f'{directory} is not a directory')
        files = walk(directory)
        hashes = await self._cafs_client.stream_batch(
            [directory / file.path for file in files]
        )
        await self._repo_client.post_ref_info(
            repo,
            ref,
            {
                'archive': False,
                'ttl': ttl_hours * 60 * 60 * 10**9,
                'comment': comment,
                'files': [
                    {
                        'blob': blob,
                        'path': file.path.as_posix(),
                        'mtime': file.mtime,
                        'mode': file.mode,
                    }
                    for blob, file in zip(hashes, files)
                ],
            },
        )

    async def check(self, repo: str, ref: str) -> bool:
        return await self._repo_client.is_ref_exist(repo, ref)

    async def delete(self, repo: str, ref: str) -> None:
        await self._repo_client.delete_ref(repo, ref)

    async def attach(self, repo: str, ref: str, file_path: Path) -> None:
        await self._repo_client.attach_file(repo, ref, file_path)

    @needs_cafs_client
    async def pull(self, repo: str, ref: str, directory: Path | str) -> None:
        if isinstance(directory, str):
            directory = Path(directory)
        await aio_os.makedirs(directory, exist_ok=True)
        ref_info = await self._repo_client.get_ref_info(repo, ref)
        remote_files = [
            LocalFile(
                path=Path(normpath(file['path'])),
                mtime=file['mtime'],
                mode=file['mode'],
                blob=file['blob'],
            )
            for file in ref_info['files']
        ]
        local_files = walk(directory)
        to_remove, to_add, to_update = await compare_file_lists(
            local_files, remote_files, directory
        )
        for file in to_remove:
            await aio_os.unlink(directory / file.path)
        if to_add:
            await self._cafs_client.pull_batch(
                [(file.blob, directory / file.path) for file in to_add]
            )
        for file in to_add + to_update:
            set_file_stat(file, directory)

    async def tag(self, repo: str, ref: str, tag: str) -> None:
        await self._repo_client.tag_ref(repo, ref, tag)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        async with self.__cafs_client_lock:
            if not self._cafs_client:
                return
            await self._cafs_client.__aexit__(exc_type, exc_val, exc_tb)
