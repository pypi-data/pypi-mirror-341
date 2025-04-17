import logging
import re


class RemoveUuid4AndLogPrefixFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self.uuid_regex = re.compile(r"__(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})")

    def filter(self, record: logging.LogRecord) -> bool:
        # Remove the UUID and log name prefix portion
        record.name = self.uuid_regex.sub(
            "",
            record.name.replace("rf.log.", "").replace("agent.", ""),
        )
        record.msg = self.uuid_regex.sub("", record.msg)
        return True


class RemoveUuidFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self.uuid_regex = re.compile(r"__(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})")

    def filter(self, record: logging.LogRecord) -> bool:
        # Remove the UUID portion
        record.name = self.uuid_regex.sub("", record.name)
        record.msg = self.uuid_regex.sub("", record.msg)
        return True
