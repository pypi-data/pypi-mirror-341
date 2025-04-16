#!/usr/bin/env python
"""
Script to generate the web search index from a JSONL file.
"""

import argparse
import os
import chromadb
import json
import glob
import numpy as np
import torch
from cragmm_search.utils import add_embeddings_to_collection
from tqdm import tqdm
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from api.web_search import extract_features

def preprocess_html(html_content: str) -> str:
    """Extract meaningful text from HTML content"""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text(separator=" ", strip=True)

    # Remove extra whitespace
    text = " ".join(text.split())

    return text

def generate_index(corpus_folder, overwrite=False):

        # Create directory for storing indexes and metadata
        data_dir = os.path.join(os.path.dirname(corpus_folder), "web_index")
        print(f"Creating directory {data_dir}")
        os.makedirs(data_dir, exist_ok=True)

        embeddings_path = os.path.join(data_dir, "embeddings.npy")
        index_to_metadata_path = os.path.join(data_dir, "index_to_metadata.json")

        # Create ChromaDB collection
        client = chromadb.Client()
        collection = client.create_collection(
            name="web_search_embeddings", metadata={"hnsw:space": "cosine"}
        )

        # Check if embeddings already exist
        if (
            os.path.exists(embeddings_path)
            and os.path.exists(index_to_metadata_path)
            and not overwrite
        ):
            print("Loading existing embeddings and metadata...")
            embs = np.load(embeddings_path).astype("float32")

            # Add embeddings to collection
            collection = add_embeddings_to_collection(collection, embs)
            # collection.add(embeddings=embs.tolist(), ids=ids)

            return collection

        # Load and process data from JSONL files
        print(f"Processing data from {corpus_folder}...")

        # Load model for creating embeddings
        from transformers import AutoModel, AutoTokenizer

        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model = AutoModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Determine device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        model.eval()

        # Process each line in the JSONL file
        all_embeddings = []
        index_to_metadata = {}
        current_index = 0

        jsonl_files = glob.glob(os.path.join(corpus_folder, "*.jsonl"))

        for file_path in tqdm(jsonl_files, total=len(jsonl_files)):
            print(f"Processing {file_path}...")
            with open(file_path, "r") as f:
                for line in tqdm(f):
                    try:
                        data = json.loads(line)
                        search_response = data["search_response"]

                        for result in search_response:
                            # Extract fields
                            page_name = result["page_name"]
                            page_url = result["page_url"]
                            page_snippet = result["page_snippet"]
                            page_html = result["page_result"]

                            index_fields = [page_name, page_snippet]
                            # Process HTML to extract text
                            try:
                                if page_html.strip():
                                    page_text = preprocess_html(page_html)
                                    index_fields.append(page_text)
                            except Exception as e:
                                print(f"Error processing HTML: {e}")
                                continue

                            # Concatenate relevant fields for indexing
                            index_text = f"{' '.join(index_fields)}"

                            # Generate embedding
                            embedding = extract_features(
                                model, tokenizer, index_text, device
                            )
                            all_embeddings.append(embedding)

                            # Store metadata
                            index_to_metadata[str(current_index)] = {
                                "page_name": page_name,
                                "page_snippet": page_snippet,
                                "page_url": page_url,
                            }

                            current_index += 1
                    except Exception as e:
                        print(f"Error processing line: {e}")
                        continue

            all_embeddings_stack = np.vstack(all_embeddings).astype("float32")
            # Save embeddings and metadata
            np.save(embeddings_path, all_embeddings_stack)
            with open(index_to_metadata_path, "w") as f:
                json.dump(index_to_metadata, f)

        # Convert list of embeddings to numpy array
        all_embeddings = np.vstack(all_embeddings).astype("float32")

        assert len(all_embeddings) == len(
            index_to_metadata
        ), "Embeddings and metadata must have the same length"

        # Save embeddings and metadata
        np.save(embeddings_path, all_embeddings)
        with open(index_to_metadata_path, "w") as f:
            json.dump(index_to_metadata, f)

        collection = add_embeddings_to_collection(collection, all_embeddings)

        return collection



def process_file(file_path, model, tokenizer, device, collection, batch_size=100):
    """Process a single JSONL file and return embeddings, metadatas, and ids."""
    file_embeddings = []
    file_metadatas = []
    file_ids = []

    with open(file_path, "r") as f:
        total_lines = sum(1 for _ in f)

    print(f"Processing {file_path}...")
    with open(file_path, "r") as f:
        for line in tqdm(f, desc=os.path.basename(file_path), total=total_lines):
            try:
                data = json.loads(line)
                search_response = data["search_response"]

                for result in search_response:
                    # Extract fields
                    page_name = result["page_name"]
                    page_url = result["page_url"]
                    page_snippet = result["page_snippet"]
                    page_html = result["page_result"]

                    index_fields = [page_name, page_snippet]
                    # Process HTML to extract text
                    try:
                        if page_html.strip():
                            page_text = preprocess_html(page_html)
                            index_fields.append(page_text)
                    except Exception as e:
                        print(f"Error processing HTML: {e}")
                        continue

                    # Concatenate relevant fields for indexing
                    index_text = f"{' '.join(index_fields)}"

                    # Generate embedding
                    embedding = extract_features(model, tokenizer, index_text, device)

                    if isinstance(embedding, np.ndarray):
                        embedding = embedding.squeeze().tolist()
                    else:
                        embedding = np.squeeze(embedding).tolist()

                    file_embeddings.append(embedding)

                    # Store metadata directly
                    file_metadatas.append({
                        "page_name": page_name,
                        "page_snippet": page_snippet,
                        "page_url": page_url,
                    })

                    # Use URL as unique ID to avoid collisions between threads
                    file_ids.append(page_url)
                    # Save in batches
                    if len(file_embeddings) >= batch_size:
                        collection.add(
                            embeddings=file_embeddings,
                            metadatas=file_metadatas,
                            ids=file_ids
                        )
                        file_embeddings.clear()
                        file_metadatas.clear()
                        file_ids.clear()
            except Exception as e:
                print(f"Error processing line in {file_path}: {e}")
                continue

    # Save any remaining data
    if file_embeddings:
        collection.add(
            embeddings=file_embeddings,
            metadatas=file_metadatas,
            ids=file_ids
        )
    print(f"Finished processing {file_path}")

    return file_embeddings, file_metadatas, file_ids

def generate_index_parallel(corpus_folder, overwrite=False) -> tuple[chromadb.Client, chromadb.Collection]:

    # Create directory for storing indexes and metadata
    data_dir = os.path.join(os.path.dirname(corpus_folder), "web_index")
    print(f"Creating directory {data_dir}")
    os.makedirs(data_dir, exist_ok=True)

    # Create ChromaDB collection
    client = chromadb.PersistentClient(path=data_dir)

    # Check if collection exists and delete if overwrite is True
    try:
        if overwrite:
            client.delete_collection("web_search_embeddings")
    except:
        pass

    collection = client.create_collection(
        name="web_search_embeddings", metadata={"hnsw:space": "cosine"}
    )

    # Load model for creating embeddings
    from transformers import AutoModel, AutoTokenizer

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Determine device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    jsonl_files = glob.glob(os.path.join(corpus_folder, "*.jsonl"))

    # Process files in parallel
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, file_path, model, tokenizer, device, collection): file_path
                  for file_path in jsonl_files}

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
            file_path = futures[future]
            try:
                future.result()
                print(f"Finished processing {file_path}")
            except Exception as e:
                print(f"File {file_path} generated an exception: {e}")

    return client, collection


def main():
    parser = argparse.ArgumentParser(
        description="Generate web search index from JSONL file"
    )
    parser.add_argument(
        "--input",
        default="corpus",
        help="Path to input corpus folder",
    )
    args = parser.parse_args()

    print(f"Generating index from {args.input} folder...")

    # Create data directory
    os.makedirs("api/web_index", exist_ok=True)

    # Generate index
    client, collection = generate_index_parallel(args.input, overwrite=True)

    print(f"Index generated successfully with {collection.count()} entries")
    print(f"Index saved to {os.path.join(os.path.dirname(args.input), 'web_index')}")

if __name__ == "__main__":
    main()
