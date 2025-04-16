import json
import logging
import typing
from contextlib import contextmanager
from hashlib import sha1
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Dict, Set, Tuple, Any, Optional
from warnings import warn
from urllib.parse import urlparse

import sh
from tornado.web import HTTPError

from newpyter.utils import remove_prefix, remove_suffix

logger = logging.getLogger(__file__)

FragmentType = Any


def get_hash(content: bytes) -> str:
    """Default way is to use SHA1 hashing"""
    return sha1(content).hexdigest()


# keeps track of everything uploaded during this session.
# Stores pairs (url, hash)
# This storage is persistent during single app start
uploaded_path_hashes: Set[Tuple[str, str]] = set()


class Encryptor:
    """Simple symmetric encryption"""

    def __init__(self, password=None):
        assert password is None, "Encryption is to be implemented yet"

    def encrypt(self, x: bytes) -> bytes:
        return x

    def decrypt(self, x: bytes) -> bytes:
        return x


class StorageContext:
    """
    Accumulates elements in cache
    so that later they could be sent to cloud/storage in batch
    """

    def __init__(self, encryptor: Encryptor):
        self.cache: Dict[str, bytes] = {}
        self.encryptor = encryptor

    def store_fragment(self, fragment: FragmentType) -> str:
        assert isinstance(fragment, list)
        fragment = json.dumps(fragment).encode("utf-8")
        assert isinstance(fragment, bytes)
        fragment = self.encryptor.encrypt(fragment)
        fragment_hash = get_hash(fragment)
        self.cache[fragment_hash] = fragment
        return fragment_hash


def output_for_missing_fragment(hash):
    return [
        {
            "execution_count": None,
            "output_type": "execute_result",
            "data": {"text/plain": f"Couldn't find output for {hash}"},
            "metadata": {"newpyter_not_found_hash": hash},
        }
    ]


class AbstractStorage:
    url: Optional[str] = None  # should be assigned in implementations

    def __init__(self, encryptor: Encryptor, local_cache: Path):
        self.encryptor = encryptor
        self.local_cache = local_cache
        self.notebook_specific_caches = local_cache.joinpath("temp_folders")
        self.notebook_specific_caches.mkdir(exist_ok=True, parents=True)
        self.uploaded_hashes: Set[str] = set()

    @contextmanager
    def get_upload_context(self):
        upload_context_manager = StorageContext(self.encryptor)
        yield upload_context_manager
        self.store_fragments(upload_context_manager.cache)

    def store_fragments(self, fragments: Dict[str, bytes]):
        # save locally
        for hash, encrypted_fragment in fragments.items():
            if not self.local_cache.joinpath(hash).exists():
                with self.local_cache.joinpath(hash).open("wb") as f:
                    f.write(encrypted_fragment)

        # collect which fragments were not uploaded yet
        for_upload = {
            hash: encrypted_fragment
            for hash, encrypted_fragment in fragments.items()
            if (self.url, hash) not in uploaded_path_hashes
        }
        if len(for_upload) > 0:
            try:
                self._upload_fragments(for_upload)
                uploaded_path_hashes.update([(self.url, hash) for hash in for_upload])
            except BaseException as e:
                raise HTTPError(500, message=f"Failed to upload jupyter outputs: \n{e}")

    def _upload_fragments(self, for_upload: Dict[str, bytes]):
        raise NotImplementedError("Storing is not implemented")

    def _download_fragments(self, hashes: List[str]) -> typing.Iterable[bytes]:
        raise NotImplementedError("Loading is not implemented in storage")

    def get_decrypted_fragments(self, hashes: List[str]) -> Dict[str, FragmentType]:
        hash2encrypted_fragment = {}
        hashes_for_downloading = []
        for hash in set(hashes):
            if self.local_cache.joinpath(hash).exists():
                with self.local_cache.joinpath(hash).open("rb") as f:
                    hash2encrypted_fragment[hash] = f.read()
            else:
                hashes_for_downloading.append(hash)

        if len(hashes_for_downloading) > 0:
            try:
                encrypted_fragments = self._download_fragments(hashes=hashes_for_downloading)
                hash2encrypted_fragment.update(dict(zip(hashes_for_downloading, encrypted_fragments)))
            except BaseException as e:
                logger.error(e)

        result = {
            hash: json.loads(self.encryptor.decrypt(encrypted_fragment).decode("utf-8"))
            for hash, encrypted_fragment in hash2encrypted_fragment.items()
        }

        for hash in hashes:
            if hash not in result:
                # would be better to return error cell, but it does not allow adding metadata
                result[hash] = output_for_missing_fragment(hash)
        return result


class MemoryMockStorage(AbstractStorage):
    url = ":MemoryMockStorage:"

    def __init__(self):
        """Storage used for testing purposed only"""
        self.stored: Dict[str, bytes] = {}
        self.encryptor = Encryptor()
        self.return_empty = False
        # does not init parent, as local cache is not used

    def store_fragments(self, fragments: Dict[str, bytes]):
        return self.stored.update(fragments)

    def get_decrypted_fragments(self, hashes: List[str]) -> Dict[str, FragmentType]:
        if self.return_empty:
            return {hash: output_for_missing_fragment(hash) for hash in hashes}
        return {hash: json.loads(self.encryptor.decrypt(self.stored[hash]).decode("utf-8")) for hash in hashes}

    def __repr__(self):
        return "<MemoryMockStorage>"


class SSHStorage(AbstractStorage):
    def __init__(self, ssh_path: str, encryptor: Encryptor, local_cache: Path, ssh_key: None):
        super().__init__(encryptor=encryptor, local_cache=local_cache)

        possible_prefixes = ["ssh://", "scp://"]
        assert any(ssh_path.startswith(prefix) for prefix in possible_prefixes)
        for prefix in possible_prefixes:
            ssh_path = remove_prefix(ssh_path, prefix)

        ssh_path = remove_suffix(ssh_path, "/") + "/"
        self.url = ssh_path
        self.ssh_key = ssh_key
        self.key_params: list = []
        if self.ssh_key is not None:
            self.key_params = ["-i", Path(self.ssh_key).expanduser()]

    def _upload_fragments(self, for_upload: Dict[str, bytes]):
        with TemporaryDirectory(dir=self.notebook_specific_caches) as temp_dir:
            for hash, fragment in for_upload.items():
                with open(Path(temp_dir).joinpath(hash), "wb") as f:
                    f.write(fragment)
                # TODO use something better than scp
                sh.scp(*self.key_params, "-r", Path(temp_dir).joinpath(hash), self.url + hash)

    def _download_fragments(self, hashes: List[str]) -> typing.Iterator[bytes]:
        for hash in hashes:
            path_on_this_machine = self.local_cache.joinpath(hash)
            if not path_on_this_machine.exists():
                # TODO use something better than scp
                sh.scp(*self.key_params, self.url + hash, path_on_this_machine)
                # this hash is already there and will not be uploaded
                uploaded_path_hashes.add((self.url, hash))

            with path_on_this_machine.open("rb") as f:
                yield f.read()

    def __repr__(self):
        return f"<SSHStorage at {self.url}, local={self.local_cache}>"


class LocalStorage(AbstractStorage):
    url = "local"

    def __init__(self, encryptor: Encryptor, local_cache: Path):
        warn("Local Storage is meant only for testing, your outputs won't be available to anyone but you!")
        super().__init__(encryptor=encryptor, local_cache=local_cache)

    def _upload_fragments(self, for_upload: Dict[str, bytes]):
        pass

    def _download_fragments(self, hashes: List[str]) -> List[bytes]:
        # should look for if not found in local cache
        raise RuntimeError(f"Fragments were not found: {hashes}")

    def __repr__(self):
        return f"<LocalStorage at {self.local_cache}>"


class S3Storage(AbstractStorage):
    def __init__(self, s3_path: str, encryptor: Encryptor, local_cache: Path, **boto3_parameters):
        super().__init__(encryptor=encryptor, local_cache=local_cache)

        possible_prefixes = ["s3://"]
        self.boto3_parameters = boto3_parameters
        assert any(s3_path.startswith(prefix) for prefix in possible_prefixes)
        self.url = remove_suffix(s3_path, "/") + "/"
        parsing_result = urlparse(self.url, allow_fragments=False)
        self.bucket, path_in_bucket = parsing_result.netloc, parsing_result.path
        assert path_in_bucket.startswith("/")
        self.path_in_bucket = path_in_bucket[1:]

    def _upload_fragments(self, for_upload):
        # dump cache to local directory, then use aws s3 sync
        import boto3

        client = boto3.client("s3", **self.boto3_parameters)
        logger.info(f"Upload {list(for_upload)} to {self.bucket}{self.path_in_bucket}")
        with TemporaryDirectory(dir=self.notebook_specific_caches) as temp_dir:
            for hash, fragment in for_upload.items():
                local_path = Path(temp_dir).joinpath(hash)
                with open(local_path, "wb") as f:
                    f.write(fragment)

                client.upload_file(str(local_path), self.bucket, self.path_in_bucket + hash)

    def _download_fragments(self, hashes: List[str]) -> List[bytes]:
        result = []
        import boto3

        client = boto3.client("s3", **self.boto3_parameters)
        logger.info(f"Download {hashes} from {self.bucket}{self.path_in_bucket}")
        for hash in hashes:
            path_on_this_machine = self.local_cache.joinpath(hash)
            if not path_on_this_machine.exists():
                try:
                    client.download_file(self.bucket, self.path_in_bucket + hash, str(path_on_this_machine))
                except BaseException:
                    logger.info(
                        f"did not locate {self.path_in_bucket + hash} in bucket {self.bucket}, prefixing with / now"
                    )
                    # in old protocol versions, file was saved with a leading slash (by mistake),
                    # this isn't so since ~nov 2021, and after ~ apr 2023 this condition should be deleted
                    client.download_file(self.bucket, "/" + self.path_in_bucket + hash, str(path_on_this_machine))
                # this hash is already there and will not be uploaded
                uploaded_path_hashes.add((self.url, hash))
            with path_on_this_machine.open("rb") as f:
                result.append(f.read())
        return result

    def __repr__(self):
        return f"<S3Storage at {self.url}, local={self.local_cache}>"


class HttpReadonlyStorage(AbstractStorage):
    def __init__(self, url, encryptor: Encryptor, local_cache: Path):
        """
        HttpReadonlyStorage - can read fragments from any http server.
        Provided path should be like https://mysite.org/some/dir/for/storage/
        Outputs are then searched in
        """
        super().__init__(encryptor=encryptor, local_cache=local_cache)
        self.url = url
        # either localhost
        assert str.endswith(url, "/"), url
        # only localhost can be used with http. e.g. http://localhost:8888/
        assert str.startswith(url, "http://localhost:") or str.startswith(url, "https://"), url

    def _upload_fragments(self, for_upload):
        # do not upload anything, as http servers do not allow that
        pass

    def _download_fragments(self, hashes: List[str]) -> List[bytes]:
        import urllib3

        result: List[bytes] = []
        with urllib3.PoolManager() as http:
            for hash_ in hashes:
                path_on_this_machine = self.local_cache.joinpath(hash_)
                if not path_on_this_machine.exists():
                    r = http.request("GET", f"{self.url}{hash_}")
                    path_on_this_machine.write_bytes(r.data)
                with path_on_this_machine.open("rb") as f:
                    result.append(f.read())
        return result

    def __repr__(self):
        return f"<HttpReadonlyStorage at {self.url}, local={self.local_cache}>"
