import codecs
import copy
import logging
import pickle
from datetime import datetime, timezone
from typing import Dict

import torch
from torch import Tensor, nn
from torch.nn import Parameter
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from ..datatypes.metrics import ModelMetrics
from ..log.nn import NnConvergenceLogManager, NnTrainLogManager

# from ..utils.random import RandomUtils
from .data import DataLoaders


class ModelManager:
    """
    Handles the Neural Network model training, validation and testing.
    """

    def __init__(
        self,
        model: nn.Module,
        criterion: _Loss,
        optimizer: Optimizer,
        batch_size: int,
        training_epochs: int,
        dataloaders: DataLoaders,
        device: None | str = None,
        seed: None | int = 42,
        deterministic: bool = False,
        track_layers_weights: None | list[str] = None,
    ) -> None:
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.training_epochs = training_epochs
        self.dataloaders = dataloaders
        self.seed = seed
        self.deterministic = deterministic
        self.device: torch.device = (
            torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else torch.device(device)
        )
        self.model = self.model.to(self.device)
        self.__move_optimizer_to_device()
        self.track_layers_weights: list[str] = [] if track_layers_weights is None else track_layers_weights
        # NOTE when the below NOTE is completed, uncomment: RandomUtils.set_randomness(seed=self.seed)
        # NOTE Ask for a model generator and generate the model here: self.model = generator.get_model(parameters)
        self.initial_state: Dict[str, Tensor] = copy.deepcopy(model.state_dict())
        # self.pretrain_state: Dict[str, Tensor] = copy.deepcopy(
        #     self.model.state_dict()
        # )
        self.__training: bool = False

    def is_training(self) -> bool:
        return self.__training

    def replace_all_layers(self, new_layers: Dict[str, Tensor]) -> None:
        self.model.load_state_dict(state_dict=new_layers)

    def _check_gradients(self) -> None:
        """
        Checks if gradients are being computed for the model's parameters and logs a warning if they are not.
        Remember to use it after calling loss.backward() and before optimizer.step().
        """
        logger = logging.getLogger(__name__)
        no_gradients = True

        params = []
        for name, param in self.model.named_parameters():
            if param.grad is None:
                params.append(name)
                # logger.warning(f"Gradient not computed for parameter: {name}")
            else:
                no_gradients = False

        if no_gradients:
            logger.warning(
                f"No gradients are being computed during training. Ensure loss.backward() is called and optimizer.step() is executed. None gradients for parameters: {params}"
            )

    def train(
        self,
        epochs: None | int = None,
        train_logger: None | NnTrainLogManager = None,
        weight_logger: None | NnConvergenceLogManager = None,
    ) -> list[ModelMetrics]:
        """
        Updates the model by training on the training dataset and optionally tracks specific weights.
        Args:
            epochs: Number of epochs to train.
            train_logger: Logger for metrics.
            weight_logger: Logger for track weight convergence.
        """
        # self.pretrain_state = copy.deepcopy(self.model.state_dict())
        self.__training = True
        if epochs is None:
            epochs = self.training_epochs

        metrics: list[ModelMetrics] = []

        # Training loop
        try:
            for epoch in range(epochs):
                if weight_logger is not None:
                    weight_logger.epoch_or_iteration = epoch + 1
                    current_state: dict[str, Tensor] = self.model.state_dict()
                    weight_logger.log_weights(
                        timestamp_z=datetime.now(tz=timezone.utc), description="PRE-TRAIN", model=current_state
                    )

                # Start training
                self.model.train()
                # total_loss: float = 0.0
                # correct: int = 0
                # total_samples: int = 0

                predicted_labels: list[int] = []
                true_labels: list[int] = []
                total_loss: float = 0.0

                images: Tensor
                labels: Tensor
                outputs: Tensor
                loss: Tensor
                predicted: Tensor

                init_time_z = datetime.now(tz=timezone.utc)
                dataloader: DataLoader = self.dataloaders.train
                for images, labels in dataloader:
                    images, labels = images.to(self.device), labels.to(self.device)
                    self.optimizer.zero_grad()
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)
                    loss.backward()
                    self._check_gradients()
                    self.optimizer.step()
                    total_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    predicted_labels.extend(predicted.cpu().numpy().tolist())
                    true_labels.extend(labels.cpu().numpy().tolist())
                    # total_samples += labels.size(0)
                    # correct += int((predicted == labels).sum().item())

                # Log metrics after each epoch
                epoch_metric: ModelMetrics = ModelMetrics.compute_metrics(
                    true_labels=true_labels,
                    predicted_labels=predicted_labels,
                    total_loss=total_loss,
                    num_batches=len(dataloader),
                    start_time_z=init_time_z,
                    end_time_z=datetime.now(tz=timezone.utc),
                )

                # epoch_metric: ModelMetrics = ModelMetrics(
                #     accuracy=(correct / total_samples),
                #     loss=(total_loss / len(dataloader)),
                #     start_time_z=init_time_z,
                #     end_time_z=datetime.now(tz=timezone.utc),
                # )
                metrics.append(epoch_metric)
                if train_logger is not None:
                    train_logger.log_train_epoch(epoch=epoch + 1, train=epoch_metric)

                if weight_logger is not None:
                    current_state = self.model.state_dict()
                    weight_logger.log_weights(
                        timestamp_z=datetime.now(tz=timezone.utc), description="POST-TRAIN", model=current_state
                    )

            return metrics

        finally:
            if weight_logger is not None:
                weight_logger.epoch_or_iteration = -1
            self.__training = False

    def _inference(self, dataloader: DataLoader) -> ModelMetrics:
        """
        Performs inference on a given dataset and returns metrics.
        """

        # Validation
        self.model.eval()
        # correct: int = 0
        # total: int = 0
        predicted_labels: list[int] = []
        true_labels: list[int] = []
        total_loss: float = 0.0

        images: Tensor
        labels: Tensor
        outputs: Tensor
        loss: Tensor
        predicted: Tensor

        init_time_z = datetime.now(tz=timezone.utc)
        with torch.no_grad():
            for images, labels in dataloader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                # total += labels.size(0)
                # correct += int((predicted == labels).sum().item())
                predicted_labels.extend(predicted.cpu().numpy().tolist())
                true_labels.extend(labels.cpu().numpy().tolist())

        end_time_z: datetime = datetime.now(tz=timezone.utc)
        # accuracy: float = correct / total
        # resulting_loss: float = total_loss / len(dataloader)

        metrics: ModelMetrics = ModelMetrics.compute_metrics(
            true_labels=true_labels,
            predicted_labels=predicted_labels,
            total_loss=total_loss,
            num_batches=len(dataloader),
            start_time_z=init_time_z,
            end_time_z=end_time_z,
        )
        # metrics: ModelMetrics = ModelMetrics(
        #     accuracy=accuracy,
        #     loss=resulting_loss,
        #     start_time_z=init_time_z,
        #     end_time_z=end_time_z,
        # )
        return metrics

    def inference(self) -> ModelMetrics:
        """
        Returns the TRAIN inference metrics using validation data.
        """
        return self._inference(dataloader=self.dataloaders.validation)

    def test_inference(self) -> ModelMetrics:
        """
        Returns the TEST inference metrics.
        """
        return self._inference(dataloader=self.dataloaders.test)

    def get_layers(self, layers: list[str], deepcopy_layers: bool = False) -> Dict[str, Tensor]:
        selected_layers: Dict[str, Tensor] = Dict()
        for layer in layers:
            if deepcopy_layers:
                selected_layers[layer] = copy.deepcopy(self.model.state_dict()[layer])
            else:
                selected_layers[layer] = self.model.state_dict()[layer]
        return selected_layers

    @staticmethod
    def export_layers(layers: Dict[str, Tensor]) -> str:
        return codecs.encode(pickle.dumps(layers), encoding="base64").decode(encoding="utf-8")

    @staticmethod
    def import_layers(
        base64_codified_layers: str,
    ) -> Dict[str, Tensor]:
        return pickle.loads(codecs.decode(base64_codified_layers.encode(encoding="utf-8"), encoding="base64"))

    def save_model_to_file(self, filepath: str) -> None:
        """
        Saves the model into a file.

        Args:
            filepath (str): The path to the file where the model will be saved.
        """
        torch.save(self.model.state_dict(), filepath)

    def load_model_from_file(self, filepath: str) -> None:
        """
        Loads the model from a file.

        Args:
            filepath (str): The path to the file from which to load the model.
        """
        self.model.load_state_dict(torch.load(filepath))

    def __move_optimizer_to_device(self) -> None:
        param: Parameter
        self.model = self.model.to(self.device)
        for param_group in self.optimizer.param_groups:
            for param in param_group["params"]:
                if param.device != self.device:
                    param.data = param.data.to(self.device)
                    if param.grad is not None:
                        param.grad = param.grad.to(self.device)
