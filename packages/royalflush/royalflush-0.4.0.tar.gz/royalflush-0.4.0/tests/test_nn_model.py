import numpy as np
import torch
from torch import nn
from torch.optim import Adam

from royalflush.dataset.cifar import Cifar10DataLoaderGenerator
from royalflush.datatypes import ModelManager
from royalflush.datatypes.data import IidDatasetSettings, NonIidDirichletDatasetSettings
from royalflush.nn import ModelManagerFactory
from royalflush.nn.model.mlp import CifarMlp


def build_neural_network(seed: int = 42) -> ModelManager:
    cifar10_generator = Cifar10DataLoaderGenerator()
    iid_settings = IidDatasetSettings(seed=42)
    dataloaders = cifar10_generator.get_dataloaders(dataset_settings=iid_settings)
    model = CifarMlp(out_classes=10)
    return ModelManager(
        model=model,
        criterion=nn.CrossEntropyLoss(),
        optimizer=Adam(model.parameters(), lr=0.001, weight_decay=1e-5),
        batch_size=64,
        training_epochs=1,
        dataloaders=dataloaders,
        seed=seed,
    )


def test_neural_network() -> None:
    model = build_neural_network()
    training_metrics = model.train()
    validation_metrics = model.inference()
    test_metrics = model.test_inference()
    mean_accuracy = np.mean([m.accuracy for m in training_metrics])
    mean_loss = np.mean([m.loss for m in training_metrics])
    print(f"Training metrics in {len(training_metrics)} epochs: {mean_accuracy} - {mean_loss}")
    print(f"Validation metrics: {validation_metrics.accuracy} - {validation_metrics.loss}")
    print(f"Test metrics: {test_metrics.accuracy} - {test_metrics.loss}")


def test_deterministic_neural_network() -> None:
    iid_settings = IidDatasetSettings(seed=42)
    model1 = ModelManagerFactory.get_cifar10_mlp(settings=iid_settings)
    model2 = ModelManagerFactory.get_cifar10_mlp(settings=iid_settings)
    assert are_weights_equal(model1.model, model2.model)


def test_random_neural_network() -> None:
    model1 = ModelManagerFactory.get_cifar10_mlp(settings=IidDatasetSettings(seed=42))
    model2 = ModelManagerFactory.get_cifar10_mlp(settings=IidDatasetSettings(seed=14))
    assert not are_weights_equal(model1.model, model2.model)


def test_model_to_base64() -> None:
    model = build_neural_network()
    model_str = ModelManager.export_layers(model.model.state_dict())
    model_reconstruct = ModelManager.import_layers(model_str)
    for key in model.initial_state:
        assert key in model_reconstruct, f"Key '{key}' not in reconstruct."
        assert torch.allclose(
            model.model.state_dict()[key], model_reconstruct[key]
        ), f"Reconstructed '{key}' tensor does not match the model"
        assert torch.allclose(
            model.initial_state[key], model_reconstruct[key]
        ), f"Reconstructed '{key}' tensor does not match the initial model"


def are_weights_equal(model1: nn.Module, model2: nn.Module) -> bool:
    """Compares the weights of two models to check if they are identical.

    Args:
        model1 (nn.Module): The first model.
        model2 (nn.Module): The second model.

    Returns:
        bool: True if all the weights are identical, False otherwise.
    """
    # Check if both models have the same number of parameters
    if len(list(model1.parameters())) != len(list(model2.parameters())):
        return False

    # Compare each corresponding parameter of the two models
    for param1, param2 in zip(model1.parameters(), model2.parameters()):
        if not torch.equal(param1, param2):
            return False

    return True


def test_training() -> None:
    epochs = 5
    dataset_settings = IidDatasetSettings(seed=13, train_samples_percent=0.1, test_samples_percent=1)
    # model = ModelManagerFactory.get_cifar10_mlp(dataset_settings)
    # metrics = model.train(epochs=epochs)
    # for m in metrics:
    #     print(m.accuracy, m.loss)

    # model = ModelManagerFactory.get_cifar10_cnn5(dataset_settings)
    # metrics = model.train(epochs=epochs)
    # for m in metrics:
    #     print(m.accuracy, m.loss)

    model = ModelManagerFactory.get_cifar100_cnn5(dataset_settings)
    metrics = model.train(epochs=epochs)
    accs, losses = [], []
    for m in metrics:
        print(m.accuracy, m.loss)
        assert m.accuracy not in accs, "Exact accuracy repeated. It is weird."
        assert m.loss not in losses, "Exact loss repeated. It is weird."
        accs.append(m.accuracy)
        losses.append(m.loss)
