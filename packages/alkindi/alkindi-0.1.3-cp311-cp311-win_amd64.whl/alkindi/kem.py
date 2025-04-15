import weakref
from typing import Literal, Final, Tuple

from alkindi import core
from alkindi.core import OQS_SUCCESS

KEM_Algorithm = Literal["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"]

STANDARDIZED_KEM_ALGORITHMS: Final[frozenset[str]] = frozenset({
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
})

liboqs = core.liboqs
ffi = core.ffi


class KEM:
    __slots__ = (
        "_kem",
        "length_secret_key",
        "length_public_key",
        "length_ciphertext",
        "length_shared_secret",
        "_finalizer",
        "__weakref__",
    )

    def __init__(self, alg_name: KEM_Algorithm) -> None:
        if alg_name not in STANDARDIZED_KEM_ALGORITHMS:
            raise ValueError(
                f"Algorithm must be one of {STANDARDIZED_KEM_ALGORITHMS}, got {alg_name}"
            )

        kem = liboqs.OQS_KEM_new(alg_name.encode("utf-8"))
        if kem == ffi.NULL:
            raise RuntimeError(
                f"Could not initialize KEM algorithm '{alg_name}'. It may be unsupported or due to an internal error."
            )

        self._kem = kem
        self.length_public_key = self._kem.length_public_key
        self.length_secret_key = self._kem.length_secret_key
        self.length_ciphertext = self._kem.length_ciphertext
        self.length_shared_secret = self._kem.length_shared_secret
        self._finalizer = weakref.finalize(self, liboqs.OQS_KEM_free, self._kem)

    def __enter__(self) -> "KEM":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        if self._finalizer.alive:
            self._finalizer()

    def generate_keypair(self) -> Tuple[bytes, bytes]:
        public_key_buffer = ffi.new("uint8_t[]", self.length_public_key)
        secret_key_buffer = ffi.new("uint8_t[]", self.length_secret_key)

        result = liboqs.OQS_KEM_keypair(self._kem, public_key_buffer, secret_key_buffer)
        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to generate the keypair")

        return (ffi.buffer(public_key_buffer, self.length_public_key)[:],
                ffi.buffer(secret_key_buffer, self.length_secret_key)[:])

    def encaps(self, public_key: bytes) -> Tuple[bytes, bytes]:
        if len(public_key) != self.length_public_key:
            raise ValueError(f"Public key must be {self.length_public_key} bytes, got {len(public_key)}")

        ciphertext_buffer = ffi.new("uint8_t[]", self.length_ciphertext)
        shared_secret_buffer = ffi.new("uint8_t[]", self.length_shared_secret)

        result = liboqs.OQS_KEM_encaps(
            self._kem,
            ciphertext_buffer,
            shared_secret_buffer,
            ffi.from_buffer(public_key),
        )
        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to encapsulate the shared secret")

        return (ffi.buffer(ciphertext_buffer, self.length_ciphertext)[:],
                ffi.buffer(shared_secret_buffer,self.length_shared_secret)[:])

    def decaps(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        if len(ciphertext) != self.length_ciphertext:
            raise ValueError(f"Ciphertext must be {self.length_ciphertext} bytes, got {len(ciphertext)}")

        if len(secret_key) != self.length_secret_key:
            raise ValueError(f"Secret key must be {self.length_secret_key} bytes, got {len(secret_key)}")

        shared_secret_buffer = ffi.new("uint8_t[]", self.length_shared_secret)

        result = liboqs.OQS_KEM_decaps(
            self._kem,
            shared_secret_buffer,
            ffi.from_buffer(ciphertext),
            ffi.from_buffer(secret_key),
        )
        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to decapsulate the shared secret")

        return ffi.buffer(shared_secret_buffer, self.length_shared_secret)[:]


__all__ = ["KEM"]
