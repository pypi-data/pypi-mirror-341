import csv
import logging
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Dict, Optional

import torch
from spade.template import Template
from torch.utils.data import DataLoader

from ..log.csv import CsvLogManager


class DataSplitLogManager(CsvLogManager):

    def __init__(
        self,
        base_logger_name="rf.datasplit",
        extra_logger_name=None,
        level=logging.INFO,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ",
        mode="a",
        encoding=None,
        delay=False,
    ):
        self._localpart = ""
        super().__init__(
            base_logger_name,
            extra_logger_name,
            level,
            datetime_format,
            mode,
            encoding,
            delay,
        )

    @property
    def agent(self) -> str:
        return self._localpart

    @agent.setter
    def agent(self, value: str) -> None:
        self._localpart = value

    @staticmethod
    def get_header() -> str:
        return "log_timestamp,log_name,agent,description,label,count"

    @staticmethod
    def get_template() -> Template:
        return Template(metadata={"rf.observer.log": "datasplit"})

    def log_split(self, dataloader: DataLoader, description: str) -> None:
        """
        Logs label distribution from a PyTorch DataLoader.

        Args:
            dataloader (DataLoader): The DataLoader to analyze.
        """
        all_labels = []
        for _, targets in dataloader:
            if isinstance(targets, torch.Tensor):
                all_labels.extend(targets.tolist())
            else:
                all_labels.extend([int(t) for t in targets])

        label_counts = dict(Counter(all_labels))

        for label, count in label_counts.items():
            msg = f"{self._localpart},{description},{label},{count}"
            self.logger.info(msg)
