import logging
from datetime import datetime, timezone
from typing import Optional

from aioxmpp import JID
from spade.template import Template
from torch import Tensor

from ..datatypes.metrics import ModelMetrics
from .csv import CsvLogManager


class NnInferenceLogManager(CsvLogManager):

    def __init__(
        self,
        base_logger_name="rf.nn.inference",
        extra_logger_name=None,
        level=logging.DEBUG,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ",
        mode="a",
        encoding=None,
        delay=False,
    ):
        self._localpart: str = ""
        self._current_round: int = -1
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
    def agent(self, value: str | JID) -> None:
        self._localpart = str(value.bare()) if isinstance(value, JID) else value

    @property
    def current_round(self) -> int:
        return self._current_round

    @current_round.setter
    def current_round(self, value: int) -> None:
        self._current_round = value

    @staticmethod
    def get_header() -> str:
        return (
            "log_timestamp,log_name,algorithm_round,timestamp,agent,seconds_to_complete_validation,seconds_to_complete_test,"
            "validation_accuracy,validation_loss,validation_precision,validation_recall,validation_f1_score,"
            "test_accuracy,test_loss,test_precision,test_recall,test_f1_score"
        )

    @staticmethod
    def get_template() -> Template:
        return Template(metadata={"rf.observer.log": "nn.inference"})

    def log(
        self,
        metrics_validation: ModelMetrics,
        metrics_test: ModelMetrics,
        timestamp: None | datetime = None,
        level: None | int = logging.DEBUG,
    ) -> None:
        seconds_validation: float = 0
        if metrics_validation.end_time_z is not None and metrics_validation.start_time_z is not None:
            seconds_validation = (metrics_validation.end_time_z - metrics_validation.start_time_z).total_seconds()

        seconds_test: float = 0
        if metrics_test.end_time_z is not None and metrics_test.start_time_z is not None:
            seconds_test = (metrics_test.end_time_z - metrics_test.start_time_z).total_seconds()

        lvl = self.level if level is None else level
        dt = datetime.now(tz=timezone.utc) if timestamp is None else timestamp
        dt_str = dt.strftime(self.datetime_format)
        msg = ",".join(
            [
                str(self._current_round),
                dt_str,
                self._localpart,
                str(seconds_validation),
                str(seconds_test),
                str(metrics_validation.accuracy),
                str(metrics_validation.loss),
                str(metrics_validation.precision),
                str(metrics_validation.recall),
                str(metrics_validation.f1_score),
                str(metrics_test.accuracy),
                str(metrics_test.loss),
                str(metrics_test.precision),
                str(metrics_test.recall),
                str(metrics_test.f1_score),
            ]
        )
        self.logger.log(level=lvl, msg=msg)


class NnTrainLogManager(CsvLogManager):

    def __init__(
        self,
        base_logger_name="rf.nn.train",
        extra_logger_name=None,
        level=logging.DEBUG,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ",
        mode="a",
        encoding=None,
        delay=False,
    ):
        self._localpart: str = ""
        self._current_round: int = -1
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
    def agent(self, value: str | JID) -> None:
        self._localpart = str(value.bare()) if isinstance(value, JID) else value

    @property
    def current_round(self) -> int:
        return self._current_round

    @current_round.setter
    def current_round(self, value: int) -> None:
        self._current_round = value

    @staticmethod
    def get_header() -> str:
        return "log_timestamp,log_name,algorithm_round,start_timestamp,agent,seconds_to_complete,epoch,accuracy,loss,precision,recall,f1_score"

    @staticmethod
    def get_template() -> Template:
        return Template(metadata={"rf.observer.log": "nn.train"})

    def log(
        self,
        seconds: float,
        epoch: int,
        accuracy: float,
        loss: float,
        precision: float,
        recall: float,
        f1_score: float,
        start_timestamp: None | datetime = None,
        level: None | int = logging.DEBUG,
    ) -> None:
        lvl = self.level if level is None else level
        dt = datetime.now(tz=timezone.utc) if start_timestamp is None else start_timestamp
        dt_str = dt.strftime(self.datetime_format)
        msg = ",".join(
            [
                str(self._current_round),
                dt_str,
                self._localpart,
                str(seconds),
                str(epoch),
                str(accuracy),
                str(loss),
                str(precision),
                str(recall),
                str(f1_score),
            ]
        )
        self.logger.log(level=lvl, msg=msg)

    def log_train_epoch(self, epoch: int, train: ModelMetrics) -> None:
        if train.start_time_z is not None and train.end_time_z is not None:
            time = train.end_time_z - train.start_time_z
            self.log(
                seconds=time.total_seconds(),
                epoch=epoch,
                accuracy=train.accuracy,
                loss=train.loss,
                precision=train.precision or -1,
                recall=train.recall or -1,
                f1_score=train.f1_score or -1,
                start_timestamp=train.start_time_z,
            )


class NnConvergenceLogManager(CsvLogManager):

    def __init__(
        self,
        base_logger_name="rf.nn.convergence",
        extra_logger_name=None,
        level=logging.DEBUG,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ",
        mode="a",
        encoding=None,
        delay=False,
    ):
        self._tracked_weights: list[tuple[str, int]] = []
        self._current_round: int = -1
        self._epoch_or_iteration: int = -1
        super().__init__(
            base_logger_name,
            extra_logger_name,
            level,
            datetime_format,
            mode,
            encoding,
            delay,
        )

    def __get_processed_tracked_weights(self, model: dict[str, Tensor]) -> list[tuple[str, int]]:
        result = []
        for layer, weight_id in self._tracked_weights:
            if layer == "rf_all_layers":
                result += [(l, weight_id) for l in model.keys()]
            elif layer in model:
                result.append((layer, weight_id))
            else:
                self.logger.warning(f"Layer '{layer}' not found in model keys.")
                raise RuntimeError(f"Layer '{layer}' not found in model keys.")
        return result

    @property
    def agent(self) -> str:
        return self._localpart

    @agent.setter
    def agent(self, value: str | JID) -> None:
        self._localpart = str(value.bare()) if isinstance(value, JID) else value

    @property
    def current_round(self) -> int:
        return self._current_round

    @current_round.setter
    def current_round(self, value: int) -> None:
        self._current_round = value

    @property
    def tracked_weights(self) -> list[tuple[str, int]]:
        return self._tracked_weights

    @tracked_weights.setter
    def tracked_weights(self, value: list[tuple[str, int]]) -> None:
        self._tracked_weights = value

    @property
    def epoch_or_iteration(self) -> int:
        return self._epoch_or_iteration

    @epoch_or_iteration.setter
    def epoch_or_iteration(self, value: int) -> None:
        self._epoch_or_iteration = value

    @staticmethod
    def get_header() -> str:
        return "log_timestamp,log_name,agent,timestamp,description,algorithm_round,epoch_or_iteration,layer,weight,weight_id"

    @staticmethod
    def get_template() -> Template:
        return Template(metadata={"rf.observer.log": "nn.convergence"})

    def log(
        self,
        timestamp_z: datetime,
        description: str,
        layer: str,
        weight: float,
        weight_id: int,
        layer_mean: bool = False,
        level: None | int = logging.DEBUG,
    ) -> None:
        lvl = self.level if level is None else level
        dt_str = timestamp_z.strftime(self.datetime_format)
        msg = ",".join(
            [
                self._localpart,
                dt_str,
                description,
                str(self._current_round),
                str(self._epoch_or_iteration),
                layer,
                str(weight),
                str(-1 if layer_mean else weight_id),
            ]
        )
        self.logger.log(level=lvl, msg=msg)

    def _log_weight(
        self,
        timestamp_z: Optional[datetime],
        description: str,
        layer: str,
        weight: float,
        weight_id: int,
    ) -> None:
        self.log(
            description=description,
            timestamp_z=datetime.now(tz=timezone.utc) if timestamp_z is None else timestamp_z,
            layer=layer,
            weight=weight,
            weight_id=weight_id,
            layer_mean=weight_id < 0,
        )

    def log_weights(self, timestamp_z: Optional[datetime], description: str, model: dict[str, Tensor]) -> None:
        processed_tracked_weights = self.__get_processed_tracked_weights(model=model)
        for layer, weight_id in processed_tracked_weights:
            layer_tensor: Tensor = model[layer]
            is_layer_mean = weight_id < 0
            if not is_layer_mean:
                weight = float(layer_tensor.flatten()[weight_id].item())
            else:
                weight = float(layer_tensor.mean().item())
            self._log_weight(
                timestamp_z=timestamp_z, description=description, layer=layer, weight=weight, weight_id=weight_id
            )
