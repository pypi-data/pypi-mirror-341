
# 📦 emon — AutoML Made Easy

`emon` is a beginner-friendly Python package designed to automate the entire machine learning pipeline. With just a few simple commands, users can clean datasets, train models, visualize data, and export models — **without needing deep ML knowledge**.

---

## 🚀 Features

- 🦼 Automatic data cleaning (handles NaNs, feature engineering, label encoding)
- 🤖 Auto model selection (`RandomForest`, `Keras`, `LogisticRegression`)
- 📈 Visualization (feature correlation & target distribution)
- 📊 Evaluation reports and confusion matrix
- 📅 Save models as `.joblib` (scikit-learn) or `.h5` (TensorFlow/Keras)
- ✅ Built-in safety checks for dataset quality
- ⟳ Simple API designed for education and ease of use

---

## 📅 Installation

```bash
pip install emon
```

> Or if using locally:
```bash
git clone https://github.com/ABS-EMON/emon.git
cd emon
pip install -e .
```

---

## 📘 Quick Start

```python
import emon

# Step 1: Clean dataset (target = class column)
emon.clean("Fitness_Tracker_Dataset.csv", target="Level")

# Step 2: Train the model
emon.train()  # Auto-selects model based on dataset

# Step 3: Visualize data
emon.visualiser()

# Step 4: Save model to file
emon.makemodel("my_model.h5")      # Keras
# or
emon.makemodel("my_model.joblib")  # RandomForest
```

---

## 🔧 API Overview

| Function | Description |
|---------|-------------|
| `emon.clean(path, target)` | Loads and cleans dataset; encodes target labels |
| `emon.train(model_type='auto')` | Trains model (auto, 'rf', 'keras', 'lr') |
| `emon.get_accuracy()` | Returns last model’s accuracy |
| `emon.evaluate()` | Prints classification report and confusion matrix |
| `emon.visualiser()` | Shows heatmap and class count distribution |
| `emon.makemodel("model.h5")` | Saves model as `.h5` (Keras) or `.joblib` (scikit-learn) |

---

## 📌 Notes

- Works best on **CSV datasets** with a clearly defined target column.
- Supports **binary and multi-class classification**.
- Automatically warns about imbalanced or insufficient data.

---

## 👨‍💼 Example Dataset Column Structure

| Heart Rate | Body Temp | BP        | Oxygen | Level |
|------------|-----------|-----------|--------|-------|
| 88         | 37.0      | 120/80    | 97     | Fit   |
| 103        | 38.5      | 140/90    | 91     | Unfit |

> `emon` will split Blood Pressure and encode `Level`.

---

## 📜 License

MIT License © 2025 ABS EMON

---

## 🌟 Contribute

Want to help improve `emon`? Open an issue or pull request on [GitHub](https://github.com/ABS-EMON/emon)!