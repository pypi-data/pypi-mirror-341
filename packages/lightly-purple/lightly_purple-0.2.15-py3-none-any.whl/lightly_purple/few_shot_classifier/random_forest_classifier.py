"""RandomForest classifier implementations."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from sklearn.ensemble import (  # type: ignore[import-untyped]
    RandomForestClassifier,
)

from .classifier import AnnotatedEmbedding, FewShotClassifier


class RandomForest(FewShotClassifier):
    """RandomForest classifier."""

    def __init__(self, classes: list[str]) -> None:
        """Initialize the RandomForestClassifier with predefined classes.

        Args:
            classes: Ordered list of class labels that will be used for training
                    and predictions. The order of this list determines the order
                    of probability values in predictions.

        Raises:
            ValueError: If classes list is empty.
        """
        if not classes:
            raise ValueError("Class list cannot be empty.")

        # Fix the random seed for reproducibility.
        self._model = RandomForestClassifier(
            class_weight="balanced", random_state=42
        )
        self._classes = classes
        self._class_to_index = {label: idx for idx, label in enumerate(classes)}

    def train(self, annotated_embeddings: list[AnnotatedEmbedding]) -> None:
        """Trains a classifier using the provided input.

        Args:
            annotated_embeddings: A list of annotated embeddings to train the
            classifier.

        Raises:
            ValueError: If annotated_embeddings is empty or contains invalid
            classes.
        """
        if not annotated_embeddings:
            raise ValueError("annotated_embeddings cannot be empty.")

        # Extract embeddings and labels.
        embeddings = [ae.embedding for ae in annotated_embeddings]
        labels = [ae.annotation for ae in annotated_embeddings]
        # Validate that all labels are in predefined classes.
        invalid_labels = set(labels) - set(self._classes)
        if invalid_labels:
            raise ValueError(
                f"Found labels not in predefined classes: {invalid_labels}"
            )

        # Convert to NumPy arrays.
        embeddings_np = np.array(embeddings)
        labels_encoded = [self._class_to_index[label] for label in labels]

        # Train the RandomForestClassifier.
        self._model.fit(embeddings_np, labels_encoded)

    def predict(self, embeddings: list[list[float]]) -> list[list[float]]:
        """Predicts the classification scores for a list of embeddings.

        Args:
            embeddings: A list of embeddings, where each embedding is a list of
            floats.

        Returns:
            A list of lists, where each inner list represents the probability
            distribution over classes for the corresponding input embedding.
            Each value in the inner list corresponds to the likelihood of the
            embedding belonging to a specific class.
            If embeddings is empty, returns an empty list.
        """
        if len(embeddings) == 0:
            return []

        # Convert embeddings to a NumPy array.
        embeddings_np = np.array(embeddings)

        # Get the classes that the model was trained on.
        trained_classes: list[int] = self._model.classes_

        # Initialize full-size probability array.
        full_probabilities = []

        # Get raw probabilities from model.
        raw_probabilities = self._model.predict_proba(embeddings_np)

        for raw_probs in raw_probabilities:
            # Initialize zeros for all possible classes.
            full_probs = [0.0 for _ in range(len(self._classes))]
            # Map probabilities to their correct positions.
            for trained_class, prob in zip(trained_classes, raw_probs):
                full_probs[trained_class] = prob
            full_probabilities.append(full_probs)
        return full_probabilities

    def export(self, _export_path: Path) -> None:
        """Not implemented: Exports the classifier to a specified folder."""
        raise NotImplementedError("RandomForest export is not implemented.")
