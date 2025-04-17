import asyncio
from datetime import datetime, timedelta, timezone
from queue import Queue
from typing import Dict, Optional

from aioxmpp import JID
from torch import Tensor

from ..datatypes.models import ModelManager
from ..log.nn import NnConvergenceLogManager
from .consensus import Consensus


# NOTE: Make a Manager(Abstract) that can store data, waiting data, etc. of a Generic type T
# then ConsensusManager(Manager) and T would be the Consensus.
class ConsensusManager:

    def __init__(
        self,
        model_manager: ModelManager,
        max_order: int,
        max_seconds_to_accept_consensus: float,
        wait_for_responses_timeout: float = 2 * 60,
        epsilon_margin: float = 0.05,
        consensus_iterations: int = 1,
        logger: Optional[NnConvergenceLogManager] = None,
        only_one_consensus_model_per_agent: bool = True,
    ) -> None:
        self.model_manager = model_manager
        self.max_order = max_order
        self.max_seconds_to_accept_consensus = max_seconds_to_accept_consensus
        self.wait_for_responses_timeout = wait_for_responses_timeout
        self.epsilon_margin = epsilon_margin
        self.received_consensus: Queue[Consensus] = Queue()
        self.waiting_responses: dict[JID, list[str]] = (
            {}
        )  # Neighbours I am waiting for. list[str] are the layers requested to the neighbour JID.
        self.to_response: Queue[tuple[Consensus, str | None]] = (
            Queue()
        )  # Neighbours waiting to my response. [str] is the thread and [Consensus] because stores layers.
        self.max_iterations = consensus_iterations
        self.__completed_iterations: int = 0
        self.__last_algorithm_iteration: int = -1
        self.__logger = logger
        self.only_one_consensus_model_per_agent = only_one_consensus_model_per_agent
        self.latest_consensus_by_agent: dict[str, Consensus] = {}  # str -> bare JID

    @property
    def logger(self) -> Optional[NnConvergenceLogManager]:
        return self.__logger

    @logger.setter
    def logger(self, value: NnConvergenceLogManager) -> None:
        self.__logger = value

    def prepare_replies_to_send(self) -> list[tuple[Consensus, str | None]]:
        responses: list[tuple[Consensus, str | None]] = []
        while self.to_response.qsize() > 0:
            consensus, thread = self.to_response.get()
            response = Consensus(
                layers=self.model_manager.get_layers(list(consensus.layers.keys())),
                request_reply=False,
                sender=consensus.sender,
            )
            responses.append((response, thread))
            self.to_response.task_done()
        return responses

    def add_consensus(self, consensus: Consensus, thread: None | str) -> None:
        if (
            consensus.sender
            and consensus.sender.bare() in self.waiting_responses
            and list(consensus.layers.keys()) == self.waiting_responses[consensus.sender.bare()]
        ):
            del self.waiting_responses[consensus.sender.bare()]
        elif consensus.request_reply:
            self.to_response.put((consensus, thread))

        if self.only_one_consensus_model_per_agent and consensus.sender:
            sender_bare = str(consensus.sender.bare())
            # Replace the existing entry
            self.latest_consensus_by_agent[sender_bare] = consensus
            self._rebuild_received_consensus_queue()
        else:
            self.received_consensus.put(consensus)

    async def wait_receive_consensus(self, timeout: None | float = None) -> bool:
        to = timeout if timeout is not None else self.wait_for_responses_timeout
        start_time_z = datetime.now(tz=timezone.utc)
        stop_time_reached = False
        while self.waiting_responses and not stop_time_reached:
            await asyncio.sleep(delay=2)
            stop_time_z = datetime.now(tz=timezone.utc) + timedelta(seconds=to)
            stop_time_reached = stop_time_z >= start_time_z
        return len(list(self.waiting_responses.keys())) == 0

    def apply_consensus(self, consensus: Consensus) -> None:
        if self.model_manager.is_training():
            raise RuntimeError("Trying to apply consensus while training the model.")
        # full_model -> this agent's model.
        # layers -> layers to consensuate from the other agent.
        consensuated_model = ConsensusManager.apply_consensus_to_model_with_layers(
            full_model=self.model_manager.model.state_dict(),
            layers=consensus.layers,
            max_order=self.max_order,
            epsilon_margin=self.epsilon_margin,
        )
        self.model_manager.replace_all_layers(new_layers=consensuated_model)

    def apply_all_consensus(
        self,
    ) -> list[Consensus]:
        consumed_consensus_transmissions: list[Consensus] = []
        while self.received_consensus.qsize() > 0:
            ct = self.received_consensus.get()
            sender_bare = str(ct.sender.bare()) if ct.sender else None
            if self.only_one_consensus_model_per_agent and sender_bare in self.latest_consensus_by_agent:
                del self.latest_consensus_by_agent[sender_bare]

            if self.__logger is not None:
                current_state: dict[str, Tensor] = self.model_manager.model.state_dict()
                self.__logger.log_weights(
                    timestamp_z=datetime.now(tz=timezone.utc), description="PRE-CONSENSUS", model=current_state
                )
            ct.processed_start_time_z = datetime.now(tz=timezone.utc)
            self.apply_consensus(ct)
            ct.processed_end_time_z = datetime.now(tz=timezone.utc)
            if self.__logger is not None:
                current_state = self.model_manager.model.state_dict()
                self.__logger.log_weights(
                    timestamp_z=ct.processed_end_time_z, description="POST-CONSENSUS", model=current_state
                )
            consumed_consensus_transmissions.append(ct)
            self.received_consensus.task_done()
        return consumed_consensus_transmissions

    # def apply_all_consensus(
    #     self,
    # ) -> list[Consensus]:
    #     if self.__logger is not None:
    #         self.__logger.epoch_or_iteration = self.__completed_iterations + 1
    #     consumed_consensus_transmissions: list[Consensus] = []
    #     while self.received_consensus.qsize() > 0:
    #         ct = self.received_consensus.get()
    #         sender_bare = str(ct.sender.bare()) if ct.sender else None

    #         # Deduplicate consensus entries flag: self.only_one_consensus_model_per_agent
    #         if self.only_one_consensus_model_per_agent and sender_bare in self.latest_consensus_by_agent:
    #             del self.latest_consensus_by_agent[sender_bare]

    #         # TODO: send the model to the other agent
    #         self.do_consensus_and_log(ct=ct)

    #         consumed_consensus_transmissions.append(ct)
    #         self.received_consensus.task_done()
    #     if self.__logger is not None:
    #         self.__logger.epoch_or_iteration = -1
    #     return consumed_consensus_transmissions

    @staticmethod
    def apply_consensus_to_model_with_layers(
        full_model: Dict[str, Tensor],
        layers: Dict[str, Tensor],
        max_order: int = 2,
        epsilon_margin: float = 0.05,
    ) -> Dict[str, Tensor]:
        """
        Applies a layer-wise consensus operation between a full model and a subset of layers from another agent.

        For each layer present in both the full model and the subset, a consensuated version is computed using
        `apply_consensus_to_tensors`. Layers not present in the subset remain unchanged.

        Args:
            full_model (Dict[str, Tensor]): The full model from the main agent.
            layers (Dict[str, Tensor]): A dictionary of layers from another agent to be used for consensus.
            max_order (int, optional): Maximum order of the graph network. Determines the consensus strength. Defaults to 2.
            epsilon_margin (float, optional): Margin to ensure epsilon < 1 / max_order. Defaults to 0.05.

        Returns:
            Dict[str, Tensor]: A new Dict representing the consensuated model.
        """
        consensuated_result: Dict[str, Tensor] = Dict()
        for key in full_model.keys():
            if key in layers:
                consensuated_result[key] = ConsensusManager.apply_consensus_to_tensors(
                    main=full_model[key],
                    foreign=layers[key],
                    max_order=max_order,
                    epsilon_margin=epsilon_margin,
                )
            else:
                consensuated_result[key] = full_model[key]
        return consensuated_result

    @staticmethod
    def apply_consensus_to_tensors(
        main: Tensor, foreign: Tensor, max_order: int, epsilon_margin: float = 0.05
    ) -> Tensor:
        """
        Computes a new consensuated `pytorch.Tensor` without modifying the input tensors.

        Args:
            main (Tensor): Input `torch.Tensor` that will be multiplied by (1 - epsilon). This must be the main agent's Tensor.
            foreign (Tensor): Input `torch.Tensor` that will be multiplied by epsilon. This must be the other agent's Tensor.
            max_order (int): Maximum order of the graph network.
            epsilon_margin (float, optional): A margin to be sure that epsilon < 1 / max_graph_degree. Defaults to 0.05.

        Raises:
            ValueError: If `max_order` is lower than 1.

        Returns:
            Tensor: The resulting Tensor after consensus.
        """
        if max_order <= 0:
            raise ValueError(f"Max order of consensus must be greater than 0 and it is {max_order}.")
        # epsilon_margin because must be LESS than 1 / max_order
        epsilon = 1 / max_order - epsilon_margin
        return (1 - epsilon) * main + epsilon * foreign

    def add_one_completed_iteration(self, algorithm_rounds: int) -> int:
        if algorithm_rounds != self.__last_algorithm_iteration:
            self.__last_algorithm_iteration = algorithm_rounds
            self.__completed_iterations = 0
        self.__completed_iterations += 1
        return self.__completed_iterations

    def are_max_iterations_reached(self) -> bool:
        return self.__completed_iterations >= self.max_iterations

    def get_completed_iterations(self, algorithm_rounds: int) -> int:
        if algorithm_rounds != self.__last_algorithm_iteration:
            self.__last_algorithm_iteration = algorithm_rounds
            self.__completed_iterations = 0
        return self.__completed_iterations

    def _rebuild_received_consensus_queue(self) -> None:
        # Clear the queue
        while not self.received_consensus.empty():
            try:
                self.received_consensus.get_nowait()
                self.received_consensus.task_done()
            except Exception:
                break

        # Rebuild with the latest ones
        for consensus in self.latest_consensus_by_agent.values():
            self.received_consensus.put(consensus)

    # def do_consensus_and_log(self, ct: Consensus) -> None:
    #     self.log_weights(description="PRE-CONSENSUS", timestamp=datetime.now(tz=timezone.utc))
    #     ct.processed_start_time_z = datetime.now(tz=timezone.utc)
    #     self.apply_consensus(ct)
    #     ct.processed_end_time_z = datetime.now(tz=timezone.utc)
    #     self.log_weights(description="POST-CONSENSUS", timestamp=ct.processed_end_time_z)

    # def log_weights(self, description: str, timestamp: datetime) -> None:
    #     if self.__logger is not None:
    #         current_state = self.model_manager.model.state_dict()
    #         self.__logger.log_weights(timestamp_z=timestamp, description=description, model=current_state)
