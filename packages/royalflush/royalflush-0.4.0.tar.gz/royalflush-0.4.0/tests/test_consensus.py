import copy
from typing import OrderedDict

import torch

from royalflush.datatypes.consensus_manager import ConsensusManager


def test_consensus_update_tensors_2agents():
    max_order = 1  # real max order
    main_tensor = torch.zeros((3, 3))

    # Input tensor of 3x3, the average with main_tensor is five
    other_tensor = torch.full((3, 3), 10.0)

    # Expected output after applying consensus
    expected_tensor = torch.full((3, 3), 5.0)

    # Apply the consensus iterations
    for _ in range(120):
        consensuated_tensor = ConsensusManager.apply_consensus_to_tensors(
            main=main_tensor, foreign=other_tensor, max_order=max_order
        )

        # Note: it's crucial to send the old model, otherwise it do not converge.
        other_tensor = ConsensusManager.apply_consensus_to_tensors(
            main=other_tensor, foreign=main_tensor, max_order=max_order
        )

        # Finally update the old model with the consensuated one.
        main_tensor = consensuated_tensor

    # Check that the output is a tensor of fives
    assert torch.allclose(main_tensor, expected_tensor), f"Expected tensor of 5s but got {main_tensor}"


def test_consensus_update_tensors():
    max_order = 4
    main_tensor = torch.zeros((3, 3))

    # Input tensors of 3x3, the average with main_tensor is five
    other_tensors = [torch.full((3, 3), 10.0), torch.full((3, 3), 2.0), torch.full((3, 3), 8.0)]

    # Expected output after applying consensus
    expected_tensor = torch.full((3, 3), 5.0)

    # Apply the consensus iterations
    for _ in range(40):
        for i, t in enumerate(other_tensors):
            consensuated_tensor = ConsensusManager.apply_consensus_to_tensors(
                main=main_tensor, foreign=t, max_order=max_order
            )

            # Note: it's crucial to send the old model, otherwise it do not converge.
            other_tensors[i] = ConsensusManager.apply_consensus_to_tensors(
                main=t, foreign=main_tensor, max_order=max_order
            )

            # Finally update the old model with the consensuated one.
            main_tensor = consensuated_tensor

    # Check that the output is a tensor of fives
    assert torch.allclose(main_tensor, expected_tensor), f"Expected tensor of 5s but got {main_tensor}"


def test_consensus_update_models():
    max_order = 2

    # Define the state dictionaries of two models with tensors of zeros and tens
    model_state_a = OrderedDict({"weight": torch.zeros((3, 3)), "bias": torch.zeros((3,))})
    model_state_b = OrderedDict({"weight": torch.full((3, 3), 10.0), "bias": torch.full((3,), 10.0)})

    # Expected output after applying consensus
    expected_model_state = OrderedDict(
        {
            "weight": torch.full((3, 3), 5.0),
            "bias": torch.full((3,), 5.0),
        }
    )

    # Apply the consensus algorithm
    for _ in range(120):
        consensuated_model_a = ConsensusManager.apply_consensus_to_model_with_layers(
            full_model=model_state_a, layers=model_state_b, max_order=max_order
        )
        model_state_b = ConsensusManager.apply_consensus_to_model_with_layers(
            full_model=model_state_b, layers=model_state_a, max_order=max_order
        )
        model_state_a = consensuated_model_a

    # Check that both 'weight' and 'bias' are correct
    assert torch.allclose(
        model_state_a["weight"],
        expected_model_state["weight"],
    ), f"Expected weight tensor of 5s but got {model_state_a['weight']}"
    assert torch.allclose(
        model_state_a["bias"],
        expected_model_state["bias"],
    ), f"Expected bias tensor of 5s but got {model_state_a['bias']}"


def test_consensus_update_layers():
    max_order = 2

    # Define the state dictionaries of two models with tensors of zeros and tens
    model_state_a = OrderedDict({"weight": torch.zeros((3, 3)), "bias": torch.zeros((3,))})
    layers = OrderedDict({"bias": torch.full((3,), 10.0)})

    # Expected output after applying consensus
    expected_model_state = {
        "weight": torch.zeros((3, 3)),
        "bias": torch.full((3,), 5.0),
    }

    # Apply the consensus algorithm
    for _ in range(120):
        consensuated_model_a = ConsensusManager.apply_consensus_to_model_with_layers(
            full_model=model_state_a, layers=layers, max_order=max_order
        )
        layers = ConsensusManager.apply_consensus_to_model_with_layers(
            full_model=layers, layers=model_state_a, max_order=max_order
        )
        model_state_a = consensuated_model_a

    # Check that both 'weight' and 'bias' are correct
    assert torch.allclose(
        model_state_a["weight"],
        expected_model_state["weight"],
    ), f"Expected weight tensor of 5s but got {model_state_a['weight']}"
    assert torch.allclose(
        model_state_a["bias"],
        expected_model_state["bias"],
    ), f"Expected bias tensor of 5s but got {model_state_a['bias']}"


def test_initial_model_not_modified_during_consensus():
    max_order = 2

    # Define the state dictionaries of two models with tensors of zeros and tens
    model_state_a = OrderedDict({"weight": torch.zeros((3, 3)), "bias": torch.zeros((3,))})
    model_state_b = OrderedDict({"weight": torch.full((3, 3), 10.0), "bias": torch.full((3,), 10.0)})

    freeze_model_a = copy.deepcopy(model_state_a)

    _ = ConsensusManager.apply_consensus_to_model_with_layers(
        full_model=model_state_a, layers=model_state_b, max_order=max_order
    )

    # Check that initial model is not modified
    assert torch.allclose(
        freeze_model_a["weight"], model_state_a["weight"]
    ), "The initial model has been modified during consensus process"

    # Define the state dictionaries of two models with tensors of zeros and tens
    model_state_b = OrderedDict({"weight": torch.full((3, 3), 10.0)})  # Note that bias is not here

    _ = ConsensusManager.apply_consensus_to_model_with_layers(
        full_model=model_state_a, layers=model_state_b, max_order=max_order
    )

    # Check that initial model is not modified
    assert torch.allclose(
        freeze_model_a["weight"], model_state_a["weight"]
    ), "The initial model has been modified during consensus process"
