---
title: India Runs Challenge RETRO
emoji: 💻 
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.31.0
python_version: 3.9
app_file: sandbox/app.py
pinned: false
---

# India Runs Challenge - Team RETRO

This repository contains the candidate ranking pipeline developed for the India Runs Challenge. The system filters candidate profiles, processes experience trajectories, and ranks the top 100 candidates based on a machine learning ensemble.

## Architecture

![System Architecture](Architecture-diagram.png)

The ranking pipeline consists of:
1. **Filtering (Stage 1)**: Removes candidates with under 4 years of experience and filters out honeypot resumes with timeline inconsistencies.
2. **Feature Extraction (Stage 2)**: Extracts 78 signals covering career history, specialized technical skills (LLMs, RAG, Vector DBs), and company types (product vs. consulting).
3. **ML Ensemble (Stage 3)**: A soft-voting ensemble of XGBoost, LightGBM, and CatBoost models.
4. **Scoring & Sorting (Stage 4)**: Computes class probabilities and assigns a final ranking with factual, non-hallucinated reasoning.
5. **Fallback (CTAE)**: A pure-Python fallback mechanism that automatically executes if model or library imports fail.

## Repository Layout

```text
Mywork/
├── data/
│   └── candidates.jsonl             # Input candidate profiles
├── models/
│   ├── ensemble_model_validated.pkl # Trained voting ensemble model
│   ├── scaler_validated.pkl         # Trained feature normalizer
│   └── selector_validated.pkl       # Feature selector mapping
├── output/
│   └── submission.csv               # Final ranked candidate list
├── src/
│   ├── main.py                      # Main entrypoint script
│   ├── common/                      # Configs, dataloader, logging, validation
│   ├── ctae/                        # Fallback pure-Python ranker
│   └── shre/                        # Pipeline stages
├── README.md                        # Project documentation
├── requirements.txt                 # Dependencies
└── submission_metadata.yaml         # Team metadata
```

## Setup & Running

### Installation
```bash
pip install -r requirements.txt
```

### Run the Pipeline
To run the ranking engine and generate the submission file:
```bash
python -m src.main data/candidates.jsonl output/submission.csv
```

### Run Verification Suite
To verify the pipeline execution and fallback path:
```bash
python test_pipeline.py
```

### Launch Interactive App
To run the Streamlit dashboard app locally:
```bash
streamlit run sandbox/app.py
```
