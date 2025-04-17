"""Experiment model for the RoyalFlush application."""

import random
import uuid
from typing import Any, Dict, Optional

from ..datatypes.graph import GraphManager


class ExperimentRawData:
    """
    Represents an experiment configuration.

    The algorithm is made case-insensitive by storing it as lowercase internally.

    Attributes:
        algorithm (str): The name of the algorithm, stored in lowercase for uniformity.
        algorithm_rounds (int): Number of algorithm rounds.
        consensus_iterations (int): Number of consensus iterations.
        training_epochs (int): Number of training epochs.
        xmpp_domain (str): Domain name of the XMPP server.
        graph_path (str): Path to the graph file.
        dataset (str): The name of the dataset.
        distribution (str): Distribution settings (e.g. 'non_iid diritchlet 0.1' or 'iid').
        ann (str): Neural network architecture (e.g. 'cnn5', 'mlp', etc.).
        seed (int | None): Can be:
            - None, if random seed should be used.
            - int number, to use that seed.
        uuid4 (str | None): Can be:
            - None, if the agents do not use a uuid4 part in their names,
            - "generate_new_uuid4", if the experiment will generate new UUID4,
            - or a specific UUID4 literal.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize a ExperimentRawData instance using a dictionary of fields.

        Args:
            data (Dict[str, Any]): A dictionary loaded from a JSON file that contains
                the fields for the experiment.
        """
        self.uuid4: Optional[str] = data.get("uuid4", None)
        self.algorithm: str = data.get("algorithm", "").lower()
        self.algorithm_rounds: int = data.get("algorithm_rounds", 0)
        self.consensus_iterations: int = data.get("consensus_iterations", 0)
        self.training_epochs: int = data.get("training_epochs", 0)
        self.xmpp_domain: str = data.get("xmpp_domain", "localhost")
        self.graph_path: str = data.get("graph_path", "")
        self.dataset: str = data.get("dataset", "")
        self.distribution: str = data.get("distribution", "")
        self.ann: str = data.get("ann", "")
        self.seed: Optional[int] = data.get("seed", None)

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "ExperimentRawData":
        """
        Create an Experiment instance directly from a JSON dictionary.

        Args:
            json_data (Dict[str, Any]): A dictionary containing experiment data.

        Returns:
            Experiment: A new Experiment instance.
        """
        return cls(json_data)

    def __repr__(self) -> str:
        """Return a human-readable representation of the Experiment."""
        return (
            f"<Experiment uuid4={self.uuid4}, "
            f"algorithm={self.algorithm}, "
            f"algorithm_rounds={self.algorithm_rounds}, "
            f"consensus_iterations={self.consensus_iterations}, "
            f"training_epochs={self.training_epochs}, "
            f"xmpp_domain={self.xmpp_domain}, "
            f"graph_path={self.graph_path}, "
            f"dataset={self.dataset}, "
            f"distribution={self.distribution}, "
            f"ann={self.ann}, "
            f"seed={self.seed}>"
        )


class Experiment:
    """
    Represents an experiment's processed settings.

    Attributes:
        algorithm (str): The name of the algorithm, stored in lowercase for uniformity.
        algorithm_rounds (int): Number of algorithm rounds.
        consensus_iterations (int): Number of consensus iterations.
        training_epochs (int): Number of training epochs.
        xmpp_domain (str): Domain name of the XMPP server.
        graph_path (str): Path to the graph file.
        dataset (str): The name of the dataset.
        distribution (str): Distribution settings (e.g., 'non_iid diritchlet 0.1' or 'iid').
        ann (str): Neural network architecture (e.g., 'cnn5', 'mlp', etc.).
        seed (Optional[int]): Random seed. Can be:
            - None, if a random seed should be used.
            - int, to use a specific seed.
        uuid4 (Optional[uuid.UUID]): Experiment's unique identifier. Can be:
            - None, if not using UUID4.
            - Generated UUID4, if "generate_new_uuid4" is provided.
            - A specific UUID4 string.
    """

    def __init__(
        self,
        algorithm: str,
        algorithm_rounds: int,
        consensus_iterations: int,
        training_epochs: int,
        xmpp_domain: str,
        graph_path: str,
        dataset: str,
        distribution: str,
        ann: str,
        seed: Optional[int],
        uuid4: Optional[str] = None,
    ) -> None:
        """
        Initializes an Experiment instance.

        Args:
            algorithm (str): The name of the algorithm.
            algorithm_rounds (int): Number of algorithm rounds.
            consensus_iterations (int): Number of consensus iterations.
            training_epochs (int): Number of training epochs.
            xmpp_domain (str): Domain name of the XMPP server.
            graph_path (str): Path to the graph file.
            dataset (str): The name of the dataset.
            distribution (str): Distribution settings.
            ann (str): Neural network architecture.
            seed (Optional[int]): Randomness seed or None if random.
            uuid4 (Optional[str]): UUID4 string, "generate_new_uuid4" to generate one or None to not use it.
        """
        raw_data_dict = {
            "algorithm": algorithm,
            "algorithm_rounds": algorithm_rounds,
            "consensus_iterations": consensus_iterations,
            "training_epochs": training_epochs,
            "xmpp_domain": xmpp_domain,
            "graph_path": graph_path,
            "dataset": dataset,
            "distribution": distribution,
            "ann": ann,
            "seed": seed,
            "uuid4": uuid4,
        }
        self.raw_data: ExperimentRawData = ExperimentRawData(data=raw_data_dict)
        self.algorithm: str = algorithm.lower()
        self.algorithm_rounds: int = algorithm_rounds
        self.consensus_iterations: int = consensus_iterations
        self.training_epochs: int = training_epochs
        self.xmpp_domain: str = xmpp_domain
        self.graph_path: str = graph_path
        self.dataset: str = dataset
        self.distribution: str = distribution
        self.ann: str = ann
        self.seed: Optional[int] = seed if seed is not None else random.randint(0, 2**32 - 1)

        # Handle UUID4 logic
        self.uuid4: Optional[uuid.UUID] = None
        if uuid4 == "generate_new_uuid4":
            self.uuid4 = uuid.uuid4()
        elif isinstance(uuid4, str):
            self.uuid4 = uuid.UUID(uuid4)

        # Initialize and import the graph
        self.graph_manager: GraphManager = GraphManager()
        self.graph_manager.import_from_gml(self.graph_path)

    def is_random_seed(self) -> bool:
        """
        Check if the experiment is using a randomly generated seed.

        Returns:
            bool: True if the seed was randomly generated, False otherwise.
        """
        return self.seed is None

    def is_uuid(self) -> bool:
        """
        Check if the experiment have a UUID.

        Returns:
            bool: True if it have one.
        """
        return self.uuid4 is not None

    @classmethod
    def from_raw_data(cls, raw_data: "ExperimentRawData") -> "Experiment":
        """
        Creates an Experiment instance from ExperimentRawData.

        Args:
            raw_data (ExperimentRawData): Raw experiment configuration.

        Returns:
            Experiment: A new Experiment instance with processed settings.
        """
        return cls(
            algorithm=raw_data.algorithm,
            algorithm_rounds=raw_data.algorithm_rounds,
            consensus_iterations=raw_data.consensus_iterations,
            training_epochs=raw_data.training_epochs,
            xmpp_domain=raw_data.xmpp_domain,
            graph_path=raw_data.graph_path,
            dataset=raw_data.dataset,
            distribution=raw_data.distribution,
            ann=raw_data.ann,
            seed=raw_data.seed,
            uuid4=raw_data.uuid4,
        )

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Experiment":
        """
        Creates an Experiment instance directly from a JSON dictionary.

        Args:
            json_data (Dict[str, Any]): A dictionary containing experiment data.

        Returns:
            Experiment: A new Experiment instance.
        """
        experiment_raw_data = ExperimentRawData.from_json(json_data=json_data)
        return cls.from_raw_data(raw_data=experiment_raw_data)

    def __repr__(self) -> str:
        """Returns a human-readable representation of the Experiment."""
        return (
            f"<Experiment uuid4={self.uuid4}, "
            f"algorithm={self.algorithm}, "
            f"algorithm_rounds={self.algorithm_rounds}, "
            f"consensus_iterations={self.consensus_iterations}, "
            f"training_epochs={self.training_epochs}, "
            f"xmpp_domain={self.xmpp_domain}, "
            f"graph_path={self.graph_path}, "
            f"dataset={self.dataset}, "
            f"distribution={self.distribution}, "
            f"ann={self.ann}, "
            f"seed={self.seed}>"
        )
