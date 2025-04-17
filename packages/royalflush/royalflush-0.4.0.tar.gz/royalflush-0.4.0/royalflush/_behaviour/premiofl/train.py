import traceback
from typing import TYPE_CHECKING

from spade.behaviour import State

from ...datatypes.metrics import ModelMetrics

if TYPE_CHECKING:
    from ..._agent.base import PremioFlAgent


class TrainState(State):
    def __init__(self) -> None:
        self.agent: "PremioFlAgent"
        super().__init__()

    async def on_start(self) -> None:
        if self.agent.current_round > 0:
            self.agent.algorithm_logger.log(
                current_round=self.agent.current_round,
                agent=self.agent.jid.bare(),
                seconds=self.agent.algorithm_logger.get_chrono_seconds(),
            )
        self.agent.algorithm_logger.restart_chrono()
        self.agent.current_round += 1
        self.agent.nn_convergence_logger.current_round = self.agent.current_round
        self.agent.nn_train_logger.current_round = self.agent.current_round
        self.agent.nn_inference_logger.current_round = self.agent.current_round
        if self.agent.are_max_iterations_reached():
            self.agent.logger.info(
                f"[{self.agent.current_round - 1}] Stopping agent because max rounds "
                + f"reached: {self.agent.current_round - 1}/{self.agent.max_rounds}"
            )
            await self.agent.stop()
        else:
            self.agent.logger.info(f"[{self.agent.current_round}] Starting round id: " + f"{self.agent.current_round}")

    async def run(self) -> None:
        try:
            if not self.agent.are_max_iterations_reached():
                # Train the model
                self.agent.logger.debug(f"[{self.agent.current_round}] Starting training...")
                metrics_train = self.agent.model_manager.train(
                    train_logger=self.agent.nn_train_logger,
                    weight_logger=self.agent.nn_convergence_logger,
                )
                metrics_validation = self.agent.model_manager.inference()
                metrics_test = self.agent.model_manager.test_inference()
                self.agent.nn_inference_logger.log(metrics_validation=metrics_validation, metrics_test=metrics_test)

                self.log_train_results(trains=metrics_train)

                self.set_next_state("communication")

        except Exception as e:
            self.agent.logger.exception(e)
            traceback.print_exc()

    def log_train_results(self, trains: list[ModelMetrics]) -> None:
        if trains:
            start_t = trains[0].start_time_z
            end_t = trains[-1].end_time_z
            if start_t is not None and end_t is not None:
                train_time = end_t - start_t
                mean_accuracy = sum(m.accuracy for m in trains) / len(trains)
                mean_loss = sum(m.loss for m in trains) / len(trains)
                self.agent.logger.info(
                    f"[{self.agent.current_round}] Train completed in "
                    + f"{train_time.total_seconds():.2f} seconds with mean accuracy {mean_accuracy:.6f} and mean"
                    + f" loss {mean_loss:.6f} iterating {len(trains)} epochs."
                )
