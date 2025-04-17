import random
import sys

import spade
from aioxmpp import JID

from royalflush.datatypes import ModelMetrics
from royalflush.log import (
    AlgorithmLogManager,
    GeneralLogManager,
    MessageLogManager,
    NnInferenceLogManager,
    NnTrainLogManager,
    setup_loggers,
)


def test_fill_logs():
    setup_loggers()

    general_logger = GeneralLogManager(extra_logger_name="test")
    general_logger.info("Starting test log...")
    general_logger.info(f"Python version: {sys.version}")
    general_logger.info(f"SPADE version: {spade.__version__}")
    general_logger.debug("Hello from the test sideee (debug edition)")
    general_logger.info(f"Handlers: {general_logger.logger.handlers}")
    general_logger.info(f"Effective Level: {general_logger.logger.getEffectiveLevel()}")

    sender = JID.fromstr("sender@localhost")
    to = JID.fromstr("to@localhost")
    message_logger = MessageLogManager(extra_logger_name="test")
    for i in range(15):
        message_logger.log(current_round=100 + i, sender=sender, to=to, msg_type="SEND", size=250_000)
    general_logger.info(f"Handlers: {message_logger.logger.handlers}")
    general_logger.info(f"Effective Level: {message_logger.logger.getEffectiveLevel()}")

    train_logger = NnTrainLogManager(extra_logger_name="test")
    for i in range(20):
        train_logger.log(
            seconds=random.random() * 10,
            epoch=i,
            accuracy=random.random(),
            loss=random.random(),
            precision=random.random(),
            recall=random.random(),
            f1_score=random.random(),
        )
    general_logger.info(f"Handlers: {train_logger.logger.handlers}")
    general_logger.info(f"Effective Level: {train_logger.logger.getEffectiveLevel()}")

    inference_logger = NnInferenceLogManager(extra_logger_name="test")
    for i in range(15):
        inference_logger.log(
            metrics_validation=ModelMetrics(
                accuracy=random.random(),
                loss=random.random(),
                precision=random.random(),
                recall=random.random(),
                f1_score=random.random(),
            ),
            metrics_test=ModelMetrics(
                accuracy=random.random(),
                loss=random.random(),
                precision=random.random(),
                recall=random.random(),
                f1_score=random.random(),
            ),
        )
    general_logger.info(f"Handlers: {inference_logger.logger.handlers}")
    general_logger.info(f"Effective Level: {inference_logger.logger.getEffectiveLevel()}")

    algorithm_logger = AlgorithmLogManager(extra_logger_name="algorithm")
    for i in range(15):
        algorithm_logger.log(current_round=100 + i, agent=sender, seconds=random.random() * 100)
    general_logger.info(f"Handlers: {algorithm_logger.logger.handlers}")
    general_logger.info(f"Effective Level: {algorithm_logger.logger.getEffectiveLevel()}")
