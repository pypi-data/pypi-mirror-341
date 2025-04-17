from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from sklearn.metrics import f1_score, precision_score, recall_score


@dataclass
class ModelMetrics:
    """
    Dataclass to store various performance metrics of a model evaluation.
    """

    accuracy: float
    loss: float
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    start_time_z: Optional[datetime] = None
    end_time_z: Optional[datetime] = None

    def time_elapsed(self) -> timedelta:
        if self.start_time_z is None or self.end_time_z is None:
            raise ValueError("start_time_z or end_time_z is None in ModelMetrics.")
        return self.end_time_z - self.start_time_z

    @classmethod
    def compute_metrics(
        cls,
        true_labels: List[int],
        predicted_labels: List[int],
        total_loss: float,
        num_batches: int,
        start_time_z: datetime,
        end_time_z: datetime,
    ) -> "ModelMetrics":
        total: int = len(true_labels)
        if total == 0:
            raise ValueError("Empty list of true labels provided.")
        correct: int = sum(1 for t, p in zip(true_labels, predicted_labels) if t == p)
        accuracy: float = correct / total

        average_loss: float = total_loss / num_batches

        precision: float = precision_score(true_labels, predicted_labels, average="macro", zero_division=0)
        recall: float = recall_score(true_labels, predicted_labels, average="macro", zero_division=0)
        f1: float = f1_score(true_labels, predicted_labels, average="macro", zero_division=0)

        return cls(
            accuracy=accuracy,
            loss=average_loss,
            precision=precision,
            recall=recall,
            f1_score=f1,
            start_time_z=start_time_z,
            end_time_z=end_time_z,
        )
