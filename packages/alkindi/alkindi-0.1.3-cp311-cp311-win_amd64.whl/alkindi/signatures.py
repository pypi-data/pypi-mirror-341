import weakref
from typing import Literal, Final, Tuple

from alkindi import core
from alkindi.core import OQS_SUCCESS

SIG_Algorithm = Literal["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"]

STANDARDIZED_SIGNATURES_ALGORITHMS: Final[frozenset[str]] = frozenset({
    "ML-DSA-44",
    "ML-DSA-65",
    "ML-DSA-87",
})

liboqs = core.liboqs
ffi = core.ffi


class Signature:
    __slots__ = (
        "_sig",
        "length_public_key",
        "length_secret_key",
        "length_signature",
        "_finalizer",
        "__weakref__",
    )

    def __init__(self, alg_name: SIG_Algorithm) -> None:
        if alg_name not in STANDARDIZED_SIGNATURES_ALGORITHMS:
            raise ValueError(
                f"Algorithm must be one of {STANDARDIZED_SIGNATURES_ALGORITHMS}, got {alg_name}"
            )

        sig = liboqs.OQS_SIG_new(alg_name.encode("utf-8"))
        if sig == ffi.NULL:
            raise RuntimeError(
                f"Could not initialize Signature algorithm '{alg_name}'. It may be unsupported or due to an internal error.")

        self._sig = sig
        self.length_public_key = self._sig.length_public_key
        self.length_secret_key = self._sig.length_secret_key
        self.length_signature = self._sig.length_signature
        self._finalizer = weakref.finalize(self, liboqs.OQS_SIG_free, self._sig)

    def __enter__(self) -> "Signature":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        if self._finalizer.alive:
            self._finalizer()

    def generate_keypair(self) -> Tuple[bytes, bytes]:
        public_key_buffer = ffi.new("uint8_t[]", self.length_public_key)
        secret_key_buffer = ffi.new("uint8_t[]", self.length_secret_key)

        result = liboqs.OQS_SIG_keypair(self._sig, public_key_buffer, secret_key_buffer)
        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to generate the keypair")

        return (ffi.buffer(public_key_buffer, self.length_public_key)[:],
                ffi.buffer(secret_key_buffer, self.length_secret_key)[:])

    def sign(self, message: bytes, secret_key: bytes) -> bytes:
        if len(secret_key) != self.length_secret_key:
            raise ValueError(
                f"Secret key length {len(secret_key)} does not match expected {self.length_secret_key}"
            )

        signature_buffer = ffi.new("uint8_t[]", self.length_signature)
        signature_len = ffi.new("size_t *")

        result = liboqs.OQS_SIG_sign(
            self._sig,
            signature_buffer,
            signature_len,
            message,
            len(message),
            ffi.from_buffer(secret_key),
        )

        if result != OQS_SUCCESS:
            raise RuntimeError("Failed to sign the message")

        return ffi.buffer(signature_buffer, signature_len[0])

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        if len(signature) != self.length_signature:
            raise ValueError(
                f"Signature length {len(signature)} does not match expected {self.length_signature}"
            )

        if len(public_key) != self.length_public_key:
            raise ValueError(
                f"Public key length {len(public_key)} does not match expected {self.length_public_key}"
            )

        result = liboqs.OQS_SIG_verify(
            self._sig,
            message,
            len(message),
            ffi.from_buffer(signature),
            len(signature),
            ffi.from_buffer(public_key),
        )

        return result == OQS_SUCCESS


__all__ = ["Signature"]
