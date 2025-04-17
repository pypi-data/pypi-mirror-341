# RaRa Subject Indexer

![Py3.10](https://img.shields.io/badge/python-3.10-green.svg)
![Py3.11](https://img.shields.io/badge/python-3.11-green.svg)
![Py3.12](https://img.shields.io/badge/python-3.12-green.svg)

**`rara-subject-indexer`** is a  Python library for predicting subject indices (keywords) for textual inputs.

---

## ✨ Features  

- Predict subject indices of following types: **personal names**, **organizations**, **titles of work**, **locations**, **events**, **topics**, **UDC Summary**, **UDC National Bibliography**, **times**, **genres/form**, **EMS categories**.
- Supports subject indexing texts in **Estonian** and **English**.
- Use [Omikuji](https://github.com/tomtung/omikuji) for supervised subject indexing.
- Use [RaKUn](https://github.com/SkBlaz/rakun2) for unsupervised subject indexing.
- Use [StanzaNER](https://stanfordnlp.github.io/stanza/ner.html) and/or [GLiNER](https://github.com/urchade/GLiNER) for NER-based subject indexing.
- Train new Omikuji models.

---

## ⚡ Quick Start  

Get started with `rara-subject-indexer` in just a few steps:

1. **Install the Package**  
   Ensure you're using Python 3.10 or above, then run:  
   ```bash
   pip install rara-subject-indexer
   ```

2. **Import and Use**  
   Example usage for finding subject indices with default configuration:

   ```python
   from rara_subject_indexer.rara_indexer import RaraSubjectIndexer
   from pprint import pprint

   # If this is your first usage, download relevant models:
   # NB! This has to be done only once!
   RaraSubjectIndexer.download_resources()
   
   # Initialize the instance with default configuration
   rara_indexer = RaraSubjectIndexer()
   
   # Just a dummy text, use a longer one to get some meaningful results
   text = "Kui Arno isaga koolimajja jõudis, olid tunnid juba alanud."

   subject_indices = rara_indexer.apply_indexers(text=text)
   pprint(subject_indices)
   ```

---

---

## ⚙️ Installation Guide

Follow the steps below to install the `rara-subject-indexer` package, either via `pip` or locally.

---

### Installation via `pip`

<details><summary>Click to expand</summary>

1. **Set Up Your Python Environment**  
   Create or activate a Python environment using Python **3.10** or above.

2. **Install the Package**  
   Run the following command:  
   ```bash
   pip install rara-subject-indexer
   ```
</details>

---

### Local Installation

Follow these steps to install the `rara-subject-indexer` package locally:  

<details><summary>Click to expand</summary>


1. **Clone the Repository**  
   Clone the repository and navigate into it:  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Python Environment**  
   Create or activate a Python environment using Python 3.10 or above. E.g:
   ```bash
   conda create -n py310 python==3.10
   conda activate py310
   ```

3. **Install Build Package**  
   Install the `build` package to enable local builds:  
   ```bash
   pip install build
   ```

4. **Build the Package**  
   Run the following command inside the repository:  
   ```bash
   python -m build
   ```

5. **Install the Package**  
   Install the built package locally:  
   ```bash
   pip install .
   ```

</details>

---

## 📝 Testing

<details><summary>Click to expand</summary>

1. **Clone the Repository**  
   Clone the repository and navigate into it:  
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Python Environment**  
   Create or activate a Python environment using Python 3.10 or above.

3. **Install Build Package**  
   Install the `build` package:  
   ```bash
   pip install build
   ```

4. **Build the Package**  
   Build the package inside the repository:  
   ```bash
   python -m build
   ```

5. **Install with Testing Dependencies**  
   Install the package along with its testing dependencies:  
   ```bash
   pip install .[testing]
   ```

6. **Run Tests**  
   Run the test suite from the repository root:  
   ```bash
   python -m pytest -v tests
   ```
---

</details>

## 📚 Documentation

<details><summary>Click to expand</summary>


#### 🔍 RaraSubjectIndexer Class

##### Overview

`RaraSubjectIndexer` wraps all logic of different models and keyword types.

##### Parameters


| Name           | Type                 | Optional | Default                 | Description                                                                                                               |
|----------------|----------------------|----------|-------------------------|---------------------------------------------------------------------------------------------------------------------------|
| methods        | Dict[str, List[str]] | True     | DEFAULT_METHOD_MAP      | Methods to use per each keyword type. See ALLOWED_METHODS for a list of supported methods of each keyword type.           |
| keyword_types  | List[str]            | True     | DEFAULT_KEYWORD_TYPES   | Keyword (subject index) types to predict. See ALLOWED_KEYWORD_TYPES for a list of supported methods of each keyword type. |
| topic_config   | dict                 | True     | DEFAULT_TOPIC_CONFIG    | Configuration for topic subject indexing models. |
| time_config    | dict                 | True     | DEFAULT_TIME_CONFIG     | Configuration for time subject indexing models. |
| genre_config   | dict                 | True     | DEFAULT_GENRE_CONFIG    | Configuration for genre/form subject indexing models. |
| category_config| dict                 | True     | DEFAULT_CATEGORY_CONFIG | Configuration for EMS category prediction models. |
| udc_config     | dict                 | True     | DEFAULT_UDC_CONFIG      | Configuration for UDC (National Bibliography) prediction models.|
| udc2_config    | dict                 | True     | DEFAULT_UDC2_CONFIG     | Configuration for UDC Summary models.|
| ner_config     | dict                 | True     | DEFAULT_NER_CONFIG      | Configuration for NER-based subject indexing models.|


<details><summary>Default configurations</summary>

DEFAULT_METHOD_MAP:

```json
 {
    "Teemamärksõnad": ["omikuji", "rakun"],
    "Kohamärksõnad": ["ner_ensemble"],
    "Isikunimi": ["ner_ensemble"], 
    "Kollektiivi nimi": ["ner_ensemble"],
    "Kohamärksõnad": ["ner_ensemble"],
    "Ajamärksõnad": ["omikuji"],
    "Teose pealkiri": ["gliner"],
    "UDK Rahvusbibliograafia": ["omikuji"],
    "UDC Summary": ["omikuji"],
    "Vormimärksõnad": ["omikuji"],
    "Valdkonnamärksõnad": ["omikuji"],
    "NER": ["ner"],
    "Ajutine kollektiiv või sündmus": ["gliner"]     
}
```

DEFAULT_KEYWORD_TYPES:

```json 
[
    "Teemamärksõnad",
    "Kohamärksõnad",
    "Isikunimi",
    "Kollektiivi nimi",
    "Kohamärksõnad",
    "Ajamärksõnad",
    "Teose pealkiri",
    "UDK Rahvusbibliograafia",
    "UDC Summary",
    "Vormimärksõnad",
    "Valdkonnamärksõnad",
    "Ajutine kollektiiv või sündmus"
]
```

DEFAULT_TOPIC_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/teemamarksonad_est"
        "en": "./rara_subject_indexer/data/omikuji_models/teemamarksonad_eng"
    }
    "rakun": {
        "stopwords": {
            "et": <list of stopwords loaded from "rara_subject_indexer/resources/stopwords/et_stopwords_lemmas.txt">,
            "en": <list of stopwords loaded from "rara_subject_indexer/resources/stopwords/et_stopwords.txt">,
        },
        "n_raw_keywords": 30
    }
}
```


DEFAULT_TIME_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/ajamarksonad_est"
        "en": "./rara_subject_indexer/data/omikuji_models/ajamarksonad_eng"
    }
    "rakun": {}
}
```

DEFAULT_GENRE_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/vormimarksonad_est"
        "en": "./rara_subject_indexer/data/omikuji_models/vormimarksonad_eng"
    }
    "rakun": {}
}
```

DEFAULT_CATEGORY_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/valdkonnamarksonad_est"
        "en": "./rara_subject_indexer/data/omikuji_models/valdkonnamarksonad_eng"
    }
    "rakun": {}
}
```

DEFAULT_UDC_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/udk_rahvbibl_est"
        "en": "./rara_subject_indexer/data/omikuji_models/udk_rahvbibl_eng"
    }
    "rakun": {}
}
```

DEFAULT_UDC2_CONFIG:

```json
 {
    "omikuji": {
        "et": "./rara_subject_indexer/data/omikuji_models/udk_general_depth_11_est"
        "en": "./rara_subject_indexer/data/omikuji_models/udk_general_depth_11_eng"
    }
    "rakun": {}
}
```

DEFAULT_NER_CONFIG:

```json
 {
    "ner": {
        "stanza_config": {
            "resource_dir": "./rara_subject_indexer/data/ner_resources/",
            "download_resources": False,
            "supported_languages": ["et", "en"],
            "custom_ner_model_langs": ["et"],
            "refresh_data": False,
            "custom_ner_models": {
                "et": "https://packages.texta.ee/texta-resources/ner_models/_estonian_nertagger.pt"
            },
            "unknown_lang_token": "unk"   
        }

        "gliner_config": {
            "labels": ["Person", "Organization", "Location", "Title of a work", "Date", "Event"], 
            "model_name": "urchade/gliner_multi-v2.1",
            "multi_label": False,
            "resource_dir": "./rara_subject_indexer/data/ner_resources/",
            "threshold": 0.5,
            "device": "cpu"
        },
        "ner_method_map": {
            "PER": "ner_ensemble",
            "ORG": "ner_ensemble",
            "LOC": "ner_ensemble",
            "TITLE": "gliner",
            "EVENT": "gliner"
        }
    }
}
```

</details>

##### Key Functions

Coming soon

---
 

### Training Supervised and Unsupervised Models

If necessary, you can train the supervised and unsupervised models from scratch using the provided pipelines. 
The training process involves reading text and label files, preprocessing the text, and training the models 
using the extracted features.

#### Training an Omikuji Model for Supervised Keyword Extraction

A sample code snippet to train and predict using the Omikuji model is provided below:

```python
from rara_subject_indexer.supervised.omikuji.omikuji_model import OmikujiModel

model = OmikujiModel()

model.train(
    text_file="texts.txt",         # File with one document per line
    label_file="labels.txt",       # File with semicolon-separated labels for each document
    language="et",                 # Language of the text, in ISO 639-1 format
    entity_type="Teemamärksõnad",  # Entity type for the keywords
    lemmatization_required=True,   # (Optional) Whether to lemmatize the text - only set False if text_file is already lemmatized
    max_features=20000,            # (Optional) Maximum number of features for TF-IDF extraction
    keep_train_file=False,         # (Optional) Whether to retain intermediate training files
    eval_split=0.1                 # (Optional) Proportion of the dataset used for evaluation
)

predictions = model.predict(
    text="Kui Arno isaga koolimajja jõudis",  # Text to classify
    top_k=3  # Number of top predictions to return
)  # Output: [('koolimajad', 0.262), ('isad', 0.134), ('õpilased', 0.062)]
```

##### 📂 Data Format

The files provided to the train function should be in the following format:
- A **text file** (`.txt`) where each line is a document.
    ```
    Document one content.
    Document two content.
    ```
- A **label file** (`.txt`) where each line contains semicolon-separated labels corresponding to the text file.
    ```
    label1;label2
    label3;label4
    ```



---

#### Training Phraser for Unsupervised Keyword Extraction


A sample code snippet to train and predict using the Phraser model is provided below:

```python
from rara_subject_indexer.utils.phraser_model import PhraserModel

model = PhraserModel()

model.train(
    train_data_path=".../train.txt",  # File with one document per line, text should be lemmatised.
    lang_code="et",                   # Language of the text, in ISO 639-1 format
    min_count=5,                      # (Optional) Minimum word frequency for phrase formation.
    threshold=10.0                    # (Optional) Score threshold for forming phrases.
)

predictions = model.predict(
    text="'vabariik aastapäev sööma kiluvõileib'",  # Lemmatised text for phrase detection
)  # Output: ['vabariik_aastapäev', 'sööma', kiluvõileib']
```

##### 📂 Data Format

The file provided to the PhraserModel train function should be in the following format:

- A **text file** (`.txt`) where each line is a document.
    ```
    Document one content.
    Document two content.
    ```

</details>