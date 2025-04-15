<div align="center">
<p align="center">

<!-- prettier-ignore -->
<img src="https://cdn.prod.website-files.com/62cd5ce03261cba217188442/66dac501a8e9a90495970876_Logo%20dark-short-p-800.png" height="50px">

**The open-source tool curating datasets**

---

[![PyPI python](https://img.shields.io/pypi/pyversions/lightly-purple)](https://pypi.org/project/lightly-purple)
[![PyPI version](https://badge.fury.io/py/lightly-purple.svg)](https://pypi.org/project/lightly-purple)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</p>
</div>

# 🚀 Aloha!

We at **[Lightly](https://lightly.ai)** created **Lightly Purple**, an open-source tool designed to supercharge your data curation workflows for computer vision datasets. Explore your data, visualize annotations and crops, tag samples, and export curated lists to improve your machine learning pipelines.

Lightly Purple runs entirely locally on your machine, keeping your data private. It consists of a Python library for indexing your data and a web-based UI for visualization and curation.

## ✨ Core Workflow

Using Lightly Purple typically involves these steps:

1.  **Index Your Dataset:** Run a Python script using the `lightly-purple` library to process your local dataset (images and annotations) and save metadata into a local `purple.db` file.
2.  **Launch the UI:** The script then starts a local web server and opens the Lightly Purple UI in your browser.
3.  **Explore & Curate:** Use the UI to visualize images, annotations, and object crops. Filter and search your data (experimental text search available). Apply tags to interesting samples (e.g., "mislabeled", "review").
4.  **Export Curated Data:** Export information (like filenames) for your tagged samples from the UI to use downstream.
5.  **Stop the Server:** Close the terminal running the script (Ctrl+C) when done.

<p align="center">
  <img alt="Lightly Purple Sample Grid View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_grid_view.jpg" width="70%">
  <br/>
  <em>Visualize your dataset samples with annotations in the grid view.</em>
</p>
<p align="center">
  <img alt="Lightly Purple Annotation Crop View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_annotation_view.jpg" width="70%">
  <br/>
  <em>Switch to the annotation view to inspect individual object crops easily.</em>
</p>
<p align="center">
  <img alt="Lightly Purple Sample Detail View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_detail_view.jpg" width="70%">
  <br/>
  <em>Inspect individual samples in detail, viewing all annotations and metadata.</em>
</p>

## 💻 Installation

Ensure you have **Python 3.8 or higher**. We strongly recommend using a virtual environment.

The library is OS-independent and works on Windows, Linux, and macOS.

```shell
# 1. Create and activate a virtual environment (Recommended)
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# 2. Install Lightly Purple
pip install lightly-purple

# 3. Verify installation (Optional)
pip show lightly-purple
```

## **Quickstart**

Download the dataset and run a quickstart script to load your dataset and launch the app.

### YOLO Object Detection

<details>
<summary> Here is a quick example using the YOLO8 dataset</summary>

<details>
<summary>The YOLO format details:</summary>

```
dataset/
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels/
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
├── valid/  (optional)
│   ├── images/
│   │   └── ...
│   └── labels/
│       └── ...
└── data.yaml
```

Each label file should contain YOLO format annotations (one per line):

```
<class> <x_center> <y_center> <width> <height>
```

Where coordinates are normalized between 0 and 1.

</details>

On Linux/MacOS:

```shell
# Download and extract dataset
export DATASET_PATH=$(pwd)/example-dataset && \
    bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh) \
 https://universe.roboflow.com/ds/nToYP9Q1ix\?key\=pnjUGTjjba \
        $DATASET_PATH

# Download example script
curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py > example.py

# Run the example script
python example.py
```

On Windows:

```shell
# Download and extract dataset
$DATASET_PATH = "$(Get-Location)\example-dataset"
[System.Environment]::SetEnvironmentVariable("DATASET_PATH", $DATASET_PATH, "Process")
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.ps1" -OutFile "fetch-dataset.ps1"
.\fetch-dataset.ps1 "https://universe.roboflow.com/ds/nToYP9Q1ix?key=pnjUGTjjba" "$DATASET_PATH"

# Download example script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py" -OutFile "example.py"

# Run the example script
python.exe example.py
```

<details>
<summary>Quickstart commands explanation</summary>

1. **Setting up the dataset path**:

```shell
  export DATASET_PATH=$(pwd)/example-dataset
```

This creates an environment variable `DATASET_PATH` pointing to an 'example-dataset' folder in your current directory.

2. **Downloading and extracting the dataset**:

```shell
  bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh)
```

- Downloads a shell script that handles dataset fetching
- The script downloads a YOLO-format dataset from Roboflow
- Automatically extracts the dataset to your specified `DATASET_PATH`

3. **Getting the example code**:

```shell
  curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py > example.py
```

Downloads a Python script that demonstrates how to:

- Load the YOLO dataset
- Process the images and annotations
- Launch the Lightly Purple UI for exploration

4. **Running the example**:

```shell
  python example.py
```

Executes the downloaded script, which will:

- Initialize the dataset processor
- Load and analyze your data
- Start a local server
- Open the UI in your default web browser
</details>

## **Example explanation**

Let's break down the `example.py` script to explore the dataset:

```python
# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the yaml file describing the dataset
# and the input images subfolder.
# We use train subfolder.
loader.from_yolo(
    "dataset/data.yaml",
    "train",
)

# We start the UI application
loader.launch()

```
</details>

### COCO Object Detection

<details>
<summary> Here is an example using the COCO dataset</summary>

<details>
<summary>The COCO format details:</summary>

```
dataset/
├── train/                   # Image files used to train
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── _annotations.coco.json        # Single JSON file containing all annotations
```

COCO uses a single JSON file containing all annotations. The format consists of three main components:

- Images: Defines metadata for each image in the dataset.
- Categories: Defines the object classes.
- Annotations: Defines object instances.

</details>

On Linux/MacOS:

```shell
# Download and extract dataset
export DATASET_PATH=$(pwd)/example-dataset/train && \
    bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh) \
 https://universe.roboflow.com/ds/XU8JobBB7x?key=rpuS7P1Du4 \
        $DATASET_PATH

# Download example script
curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-coco.py > example.py

# Run the example script
python example.py
```

On Windows:

```shell
# Download and extract dataset

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.ps1" -OutFile "fetch-dataset.ps1"
.\fetch-dataset.ps1 "https://universe.roboflow.com/ds/XU8JobBB7x?key=rpuS7P1Du4" "$(Get-Location)\example-dataset"

# Download example script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-coco.py" -OutFile "example.py"

$DATASET_PATH = "$(Get-Location)\example-dataset\train"
[System.Environment]::SetEnvironmentVariable("DATASET_PATH", $DATASET_PATH, "Process")
# Run the example script
python.exe example.py
```

## **Example explanation**

Let's break down the `example-coco.py` script to explore the dataset:

```python
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the annotations json file and the input images folder.
# Defined dataset is processed here to be available for the UI application.
loader.from_coco_instance_segmentations(
    "dataset/_annotations.coco.json",
    "dataset/train",

# We start the UI application
loader.launch()

```
</details>

### Using your own dataset in COCO Instance Segmentation format

<details>
<summary> Here is an example using your own dataset</summary>

*Note that the segmentation annotations must be in RLE format!*

To use Lightly Purple with your data:
1. Ensure your data is in a supported format (YOLO or COCO, see below).
2. Create a Python script (e.g., `load_my_data.py`).
3. Adapt the template below, changing the file paths to match your dataset location. Make sure to uncomment the correct loader method (`from_yolo`, `from_coco_object_detections`, or `from_coco_instance_segmentations`).
4. Run your script (`python load_my_data.py`) from your activated environment.

```python
# load_my_data.py (example for COCO instance segmentation)

import os
from lightly_purple import DatasetLoader

my_coco_is_annotations_json = "/path/to/your/coco_segmentation_annotations.json"
my_coco_is_images_folder = "/path/to/your/images" # Folder containing the images

print("Initializing Lightly Purple...")
loader = DatasetLoader()

print("Processing dataset...")
loader.from_coco_instance_segmentations(
    my_coco_is_annotations_json,
    my_coco_is_images_folder
)

loader.from_coco_instance_segmentations(annotations_json_path=my_coco_is_annotations_json, input_images_folder=my_coco_is_images_folder)

print("Dataset indexing complete.")

print(f"Launching the Lightly Purple UI. Visit http://localhost:8001 if it doesn't open automatically.")
loader.launch()

print("UI Server is running. Press Ctrl+C to stop.")

</details>

## 🔍 How It Works

1.  Your **Python script** uses the `lightly-purple` **Dataset Loader**.
2.  The Loader reads your images and annotations, calculates embeddings, and saves metadata to a local **`purple.db`** file (using DuckDB).
3.  `loader.launch()` starts a **local Backend API** server.
4.  This server reads from `purple.db` and serves data to the **UI Application** running in your browser (`http://localhost:8001`).
5.  Images are streamed directly from your disk for display in the UI.

## 📦 Supported Dataset Formats & Annotations

The `DatasetLoader` currently supports:

*   **YOLOv8 Object Detection:** Reads `.yaml` file. Supports bounding boxes ✅.
*   **COCO Object Detection:** Reads `.json` annotations. Supports bounding boxes ✅.
*   **COCO Instance Segmentation:** Reads `.json` annotations. Supports instance masks in RLE (Run-Length Encoding) format ✅.

**Limitations:**

*   Requires datasets *with* annotations. Cannot index image folders alone ❌.
*   No direct support for classification datasets yet ❌.
*   Cannot add custom metadata during the loading step ❌.

## 📚 **FAQ**

### Are the datasets persistent?

Yes, the information about datasets is persistent and stored in the db file. You can see it after the dataset is processed.
If you rerun the loader it will create a new dataset representing the same dataset, keeping the previous dataset information untouched.

### Can I change the database path?

Not yet. The database is stored in the working directory by default.

### Can I launch in another Python script or do I have to do it in the same script?

It is possible to use only one script at the same time because we lock the db file for the duration of the script.

### Can I change the API backend port?

Currently, the API always runs on port 8001, and this cannot be changed yet.

### Can I process datasets that do not have annotations?

No, we support only datasets with annotations now.

### What dataset annotations are supported?

Bounding boxes are supported ✅

Instance segmentation is supported ✅

Custom metadata is NOT yet supported ❌
