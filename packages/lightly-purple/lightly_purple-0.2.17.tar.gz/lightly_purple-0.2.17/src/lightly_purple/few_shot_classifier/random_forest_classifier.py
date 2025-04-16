"""RandomForest classifier implementations."""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sklearn  # type: ignore[import-untyped]
from sklearn.ensemble import (  # type: ignore[import-untyped]
    RandomForestClassifier,
)
from typing_extensions import assert_never

from .classifier import AnnotatedEmbedding, ExportType, FewShotClassifier

# The version of the file format used for exporting and importing classifiers.
# This is used to ensure compatibility between different versions of the code.
# If the format changes, this version should be incremented.
FILE_FORMAT_VERSION = "1.0.0"


@dataclass
class ModelExportMetadata:
    """Metadata for exporting a model for traceability and reproducibility."""

    file_format_version: str
    model_type: str
    created_at: str
    class_names: list[str]
    num_input_features: int
    num_estimators: int
    embedding_model_hash: str
    embedding_model_name: str
    sklearn_version: str


class RandomForest(FewShotClassifier):
    """RandomForest classifier."""

    def __init__(
        self,
        classes: list[str],
        embedding_model_name: str,
        embedding_model_hash: str,
    ) -> None:
        """Initialize the RandomForestClassifier with predefined classes.

        Args:
            classes: Ordered list of class labels that will be used for training
                and predictions. The order of this list determines the order of
                probability values in predictions.
            embedding_model_name: Name of the model used for creating the
                embeddings.
            embedding_model_hash: Hash of the model used for creating the
                embeddings.
            Note: embedding_model_name and embedding_model_hash are used for
            traceability in the exported model metadata.

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
        self._embedding_model_name = embedding_model_name
        self._embedding_model_hash = embedding_model_hash or ""

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

    def export(
        self, export_path: Path, export_type: ExportType = "sklearn"
    ) -> None:
        """Exports the classifier to a specified file.

        Args:
            export_path: The full file path where the export will be saved.
            export_type: The type of export. Options are:
                "sklearn": Exports the RandomForestClassifier instance.
                "lightly": Exports the model in raw format with metadata
                and tree details.
        """
        metadata = ModelExportMetadata(
            file_format_version=FILE_FORMAT_VERSION,
            model_type="RandomForest",
            created_at=str(datetime.now(timezone.utc).isoformat()),
            class_names=self._classes,
            num_input_features=self._model.n_features_in_,
            num_estimators=len(self._model.estimators_),
            embedding_model_hash=self._embedding_model_hash,
            embedding_model_name=self._embedding_model_name,
            sklearn_version=sklearn.__version__,
        )

        if export_type == "sklearn":
            # Combine the model and metadata into a single dictionary
            export_data = {
                "model": self._model,
                "metadata": metadata,
            }

        elif export_type == "lightly":
            raise NotImplementedError("Lightly raw export is not implemented.")
        else:
            assert_never(export_type)

        # Save to the specified file path.
        # Ensure parent dirs exist.
        export_path.parent.mkdir(parents=True, exist_ok=True)
        with open(export_path, "wb") as f:
            pickle.dump(export_data, f)


def load_random_forest_classifier(classifier_path: Path) -> RandomForest:
    """Loads a RandomForest classifier from a file.

    Args:
        classifier_path: The path to the exported classifier file.

    Returns:
        A fully initialized RandomForest classifier instance.
    """
    if not classifier_path.exists():
        raise FileNotFoundError(f"The file {classifier_path} does not exist.")

    with open(classifier_path, "rb") as f:
        export_data = pickle.load(f)

    model = export_data.get("model")
    metadata: ModelExportMetadata = export_data.get("metadata")

    if model is None or metadata is None:
        raise ValueError(
            "The loaded file does not contain a valid model or metadata."
        )

    if metadata.file_format_version != FILE_FORMAT_VERSION:
        raise ValueError(
            f"File format version mismatch. Expected '{FILE_FORMAT_VERSION}', "
            f"got '{metadata.file_format_version}'."
        )
    instance = RandomForest(
        classes=metadata.class_names,
        embedding_model_name=metadata.embedding_model_name,
        embedding_model_hash=metadata.embedding_model_hash,
    )
    # Set the model.
    instance._model = model  # noqa: SLF001
    return instance
