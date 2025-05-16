## Emotion Analysis in German Parties' Press Releases

Political parties don't just inform — they express:

😠 😨 🤢 😢 😄 🤩 😌 🥺

I classify eight emotions — anger, fear, disgust, sadness, joy, enthusiasm, pride and hope — in German political texts using a pre-trained transformer-based language model (GELECTRA). The results are aggregated to the document level and analyzed across parties, time and issue categories.

<br>

<img src="https://github.com/user-attachments/assets/f52bf674-f965-426f-8f23-8a329f8a3534" alt="mds_thesis_poster" width="1000"/>

<br>

---

### Project Overview

This project analyzes how and when German political parties use emotional language as part of their strategic communication.  

The analysis covers over 40,000 press releases published by six German parties between 2010 and 2019. Eight discrete emotions are classified — anger, fear, disgust, sadness, joy, enthusiasm, pride, and hope — using a pre-trained transformer-based language model (GELECTRA), fine-tuned on German political text. Emotion probabilities are aggregated at the document level, allowing for systematic analysis of emotional patterns in relation to issue ownership and issue saliency.  

The study contributes to research on political communication by showing how emotional tone is used not only to frame content but also to differentiate between parties and amplify the salience of key issues.

<br>

### Methodology

**Dataset**  
PARTYPRESS dataset (Erfort et al. 2023), filtered for German-language press releases from 2010–2019  
- Final sample: 41,328 press releases with 453,410 sentence-level observations

**Pre-processing**  
- Removal of outliers based on word count (2.5th and 97.5th percentiles)  
- Sentence-level splitting for compatibility with GELECTRA

**Emotion Classification**  
Emotion detection using GELECTRA, a transformer-based model fine-tuned for German political texts (Widmann & Wich 2023)

- [GitHub: 3x8emotions](https://github.com/tweedmann/3x8emotions)
- [HuggingFace: GELECTRA](https://huggingface.co/german-nlp-group/electra-base-german-uncased)

Sentence-level emotion probabilities aggregated to the document level.

<br>

### Results

**Regression Analysis**  
Explain emotional variation across:

- Issue categories (emotion–issue associations)
- Issue saliency (top issues per party and month)
- Issue ownership (owned vs. non-owned issues, both within-party and between-party comparisons)

**Key Results**  
- Anger and hope are the most common emotions across all parties
- The AfD frequently uses anger and fear, particularly on European integration
- The Green party emphasizes hope on environmental issues, with some fear-related framing
- The CDU/CSU tends to use positive emotions like hope and pride on law and crime compared to other parties, but shows higher fear and anger on this issue relative to their own other topics
- Overall, negative emotions are more prevalent on parties' most salient issues, supporting the view that emotional tone is used strategically to mobilize attention and frame conflict

<br>

### Setup Instructions

To reproduce this analysis:

```bash
# create a virtual environment
python -m venv env
source env/bin/activate

# install dependencies
pip install -r requirements.txt
```
<br>

### Citation

If you use this repository or build on the data or methods, please cite:

```bibtex
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

This repository contains the code and data used for my master’s thesis in MDS program at the Hertie School in Berlin.

---

**Varvara Ilyina**

M.Sc. Data Science for Public Policy  
Hertie School, Berlin, Germany

*April 28, 2025*

---

For questions, feel free to reach out:
[v.ilyina@students.hertie-school.org](v.ilyina@students.hertie-school.org)
