### 02. RUN GELECTRA

import os
import sys
import time
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from multiprocessing import Pool

#----- configuration --------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HELPER_PATH = os.path.join(ROOT_DIR, "03_electra", "helper")
sys.path.append(HELPER_PATH)
ELECTRA_PATH = os.path.join(ROOT_DIR, "03_electra")
SENTENCE_PATH = os.path.join(ROOT_DIR, "data", "out", "sentences.pkl")
OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "out", "predictions_test.csv")
MODEL_NAME = "german-nlp-group/electra-base-german-uncased"
MODEL_PATH = os.path.join(ELECTRA_PATH, "models", "final")
EMOTIONS = ["anger", "fear", "disgust", "sadness", "joy", "enthusiasm", "pride", "hope"]
BATCH_SIZE = 32
N_WORKERS = 4
TEST_BATCH_SIZE = 1000
FULL_BATCH_SIZE = 5000

#----- global shared objects ------------------------------------
model = None
tokenizer = None

#----- set thread limits for stability --------------------------
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
torch.set_num_threads(1)

#----- load model once per worker -------------------------------
def load_model():
    global model, tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(
        f"{MODEL_PATH}/{MODEL_NAME}", num_labels=len(EMOTIONS)
    ).to("cpu")
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

#----- batch inference function ---------------------------------
def predict_batch(texts):
    global model, tokenizer
    inputs = tokenizer(
        texts,
        truncation=True,
        padding=True,
        return_tensors="pt"
    ).to("cpu")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits).detach().cpu().numpy()

    return probs

#----- run parallel inference -----------------------------------
def run_parallel(sentences, batch_size, n_workers):
    print(f"Running inference on {len(sentences)} texts using {n_workers} workers...")

    # Break into batches
    batches = [sentences[i:i + batch_size] for i in range(0, len(sentences), batch_size)]

    with Pool(processes=n_workers, initializer=load_model) as pool:
        all_probs = pool.map(predict_batch, batches)

    return np.vstack(all_probs)

#----- main execution -------------------------------------------
if __name__ == "__main__":

    # load sentences
    import pickle
    with open(SENTENCE_PATH, "rb") as f:
        sentences = pickle.load(f)

    #----- test run on small sample -----------------------------
    #print("Testing on small batch first...")
    #test_sample = sentences[:TEST_BATCH_SIZE]
    #start_time = time.time()
    #test_results = run_parallel(test_sample, batch_size=BATCH_SIZE, n_workers=N_WORKERS)
    #duration = time.time() - start_time
    #print(f"Test batch completed in {round(duration / 60, 2)} minutes")

    # save test output
    #df_test = pd.DataFrame(test_results, columns=EMOTIONS)
    #df_test.to_csv(OUTPUT_PATH, index=False)

    #----- full run in chunks -----------------------------------
    print("Starting full inference run...")

    for i in range(0, len(sentences), FULL_BATCH_SIZE):
        batch = sentences[i:i + FULL_BATCH_SIZE]
        print(f"Processing {i} to {i + len(batch)}...")

        start = time.time()
        batch_results = run_parallel(batch, batch_size=BATCH_SIZE, n_workers=N_WORKERS)
        elapsed = round((time.time() - start) / 60, 2)

        df_batch = pd.DataFrame(batch_results, columns=EMOTIONS)
        
        # save batch
        batch_output_path = os.path.join(ROOT_DIR, "data", "out", f"predictions_batch_{i}.csv")
        df_batch.to_csv(batch_output_path, index=False)

        print(f"Batch {i} done in {elapsed} minutes and saved to: {batch_output_path}")