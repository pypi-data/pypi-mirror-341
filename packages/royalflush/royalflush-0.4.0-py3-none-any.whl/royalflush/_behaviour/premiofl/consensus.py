from datetime import datetime
from typing import TYPE_CHECKING, OrderedDict

from aioxmpp import JID
from spade.behaviour import State
from torch import Tensor

if TYPE_CHECKING:
    from ..._agent.base import PremioFlAgent
    from ...datatypes.consensus import Consensus


class ConsensusState(State):
    def __init__(self) -> None:
        self.agent: "PremioFlAgent"
        super().__init__()

    async def run(self) -> None:
        consensus_it_id = self.agent.consensus_manager.get_completed_iterations(self.agent.current_round) + 1
        self.agent.logger.debug(f"[{self.agent.current_round}] Waiting for layers to apply consensus...")
        if await self.agent.consensus_manager.wait_receive_consensus():
            self.agent.logger.info(f"[{self.agent.current_round}] ({consensus_it_id}) All layers received.")
        else:
            self.agent.logger.debug(f"[{self.agent.current_round}] Receive consensus finished by timeout.")
        # Try to apply consensus
        self.agent.logger.debug(f"[{self.agent.current_round}] Starting consensus...")
        consensuateds = self.agent.consensus_manager.apply_all_consensus()
        if consensuateds:
            self.agent.logger.info(
                f"[{self.agent.current_round}] ({consensus_it_id}) Consensus completed in ConsensusState "
                + f"with neighbours: {[ct.sender.localpart for ct in consensuateds if ct.sender]}."
            )
        else:
            self.agent.logger.debug(
                f"[{self.agent.current_round}] There are not consensus messages pending to consensuate."
            )
        # await self._wait_for_responses(consensus_iteration=consensus_it_id, timeout=None)

        # # consensuateds = self.agent.consensus_manager.apply_all_consensus()
        # await self._apply_all_consensus(consensus_iteration=consensus_it_id)

    async def on_end(self):
        it = self.agent.consensus_manager.add_one_completed_iteration(algorithm_rounds=self.agent.current_round)
        if self.agent.consensus_manager.are_max_iterations_reached():
            self.agent.logger.info(
                f"[{self.agent.current_round}] Going to TrainState because max consensus iterations "
                + f"reached: {it}/{self.agent.consensus_manager.max_iterations}."
            )
            self.set_next_state("train")
        else:
            self.agent.logger.info(
                f"[{self.agent.current_round}] Going to CommunicationState... iterations: "
                + f"{it}/{self.agent.consensus_manager.max_iterations}."
            )
            self.set_next_state("communication")

    # async def _wait_for_responses(self, consensus_iteration: int, timeout: float | None) -> None:
    #     self.agent.logger.debug(f"[{self.agent.current_round}] Waiting for layers to apply consensus...")
    #     if await self.agent.consensus_manager.wait_receive_consensus(timeout=timeout):
    #         self.agent.logger.info(f"[{self.agent.current_round}] ({consensus_iteration}) All layers received.")
    #     else:
    #         self.agent.logger.info(
    #             f"[{self.agent.current_round}] ({consensus_iteration}) Receive consensus finished by timeout."
    #         )

    # async def _apply_all_consensus(self, consensus_iteration: int) -> None:
    #     senders: list[str] = []
    #     self.agent.logger.debug(f"[{self.agent.current_round}] ({consensus_iteration}) Starting consensus...")
    #     cm = self.agent.consensus_manager

    #     while cm.received_consensus.qsize() > 0:
    #         ct: "Consensus" = cm.received_consensus.get()
    #         sender_bare = str(ct.sender.bare()) if ct.sender else None

    #         # Deduplicate consensus entries flag: self.only_one_consensus_model_per_agent
    #         if cm.only_one_consensus_model_per_agent and sender_bare in cm.latest_consensus_by_agent:
    #             del cm.latest_consensus_by_agent[sender_bare]

    #         # TODO: send the model to the other agent

    #         self.do_consensus_and_log(ct=ct)

    #         senders.append(str(ct.sender.localpart))
    #         self.received_consensus.task_done()
    #     if self.__logger is not None:
    #         self.__logger.epoch_or_iteration = -1
    #     if senders:
    #         self.agent.logger.info(
    #             f"[{self.agent.current_round}] ({consensus_iteration}) Consensus completed in ConsensusState "
    #             + f"with neighbours: {senders}."
    #         )
    #     else:
    #         self.agent.logger.info(
    #             f"[{self.agent.current_round}] ({consensus_iteration}) There are not consensus messages pending"
    #             + " to consensuate."
    #         )

    # async def __send_layers(
    #     self,
    #     neighbour: JID,
    #     layers: OrderedDict[str, Tensor],
    #     thread: None | str = None,
    # ) -> None:
    #     metadata = {"rf.conversation": "layers"}
    #     await self.agent.send_local_layers(
    #         neighbour=neighbour,
    #         request_reply=False,
    #         layers=layers,
    #         thread=thread,
    #         metadata=metadata,
    #         behaviour=self,
    #     )
    #     self.agent.logger.debug(
    #         f"[{self.agent.current_round}] Sent to {neighbour.localpart} the layers: {list(layers.keys())}."
    #     )

    # def __log_weights(self, description: str, timestamp: datetime) -> None:
    #     if self.agent.nn_convergence_logger is not None:
    #         current_state = self.agent.model_manager.model.state_dict()
    #         self.agent.nn_convergence_logger.log_weights(
    #             timestamp_z=timestamp, description=description, model=current_state
    #         )
