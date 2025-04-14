## Emotion Analysis in German Parties' Press Releases

Varvara Ilyina

Master of Data Science for Public Policy  
Hertie School in Berlin, Germany

*April 28, 2025*

---

This repository contains the code and data used for my Master’s thesis in the Master of Data Science for Public Policy (MDS) program at the Hertie School in Berlin.

<br>

### Project Overview

This project explores how political parties in Germany use emotional language in their press releases.
I classify eight emotions — anger, fear, disgust, sadness, joy, enthusiasm, pride, and hope — using a pre-trained transformer-based language model (GELECTRA) fine-tuned on German political text.
The results are aggregated to the document level and analyzed across parties, time, and issue categories.

<br>

### Methodology

**Dataset**  
Based on the PARTYPRESS dataset, filtered for German-language press releases from 2010–2019.  
Final sample: 44,950 documents (after filtering by issue category, length, and language).

**Pre-processing**  
- Removal of outliers based on word count (2.5th and 97.5th percentiles)
- Sentence-level splitting for compatibility with GELECTRA
- Merging of text data with metadata (party, date, issue, etc.)

**Emotion Classification**  
Sentence-level inference using GELECTRA

- [GitHub: 3x8emotions](https://github.com/tweedmann/3x8emotions)
- [HuggingFace: GELECTRA](https://huggingface.co/german-nlp-group/electra-base-german-uncased)

The model predicts the binary presence of each of the eight emotions per sentence.  
Predictions are then merged back with the metadata.

**Aggregation**  
Document-level measures:

- *Emotion intensity*: total emotion mentions per sentence
- *Emotion share*: proportional distribution of each emotion per press release

These outputs are used for visualization and downstream analysis.

<br>

### Results

to be added here

<br>

### Setup Instructions

To reproduce this analysis, please clone the repository and install the following dependencies:

```bash
# create a virtual environment
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt
```
<br>

### Citation

If you use this repository or build on the data or methods, please cite:

```java
@article{erfort2023,
  title={The PARTYPRESS Database: A new comparative database of parties’ press releases},
  author={Erfort, Cornelius and Stoetzer, Lukas F and Kl{\"u}ver, Heike},
  journal={Research \& Politics},
  volume={10},
  number={3},
  pages={20531680231183512},
  year={2023},
  publisher={SAGE Publications Sage UK: London, England}
}

@article{widmann2023,
  title       = {Creating and comparing dictionary, word embedding, and transformer-based models to measure discrete emotions in German political text},
  author      = {Widmann, Tobias and Wich, Maximilian},
  journal     = {Political Analysis},
  volume      = {31},
  number      = {4},
  pages       = {626--641},
  year        = {2023}
}
```
<br>

### Contact

For questions, feel free to reach out:
[v.ilyina@students.hertie-school.org](v.ilyina@students.hertie-school.org)

