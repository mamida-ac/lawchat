import argparse
import json
import os
import sys
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np
import time

def preprocess_text(text):
    sentences = sent_tokenize(text)
    words = [word_tokenize(sent.lower()) for sent in sentences]
    stop_words = set(stopwords.words('english'))
    words = [[word for word in sent if word.isalnum() and word not in stop_words] for sent in words]
    return sentences, words

def create_similarity_matrix(sentences, words):
    vocab = set()
    for word_list in words:
        vocab.update(word_list)
    vocab = list(vocab)
    word_to_index = {word: i for i, word in enumerate(vocab)}
    
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                vector_i = np.zeros(len(vocab))
                vector_j = np.zeros(len(vocab))
                for word in words[i]:
                    if word in vocab:
                        vector_i[word_to_index[word]] += 1
                for word in words[j]:
                    if word in vocab:
                        vector_j[word_to_index[word]] += 1
                similarity_matrix[i, j] = cosine_similarity([vector_i], [vector_j])[0, 0]
    return similarity_matrix

def textrank_summarize(text, num_sentences):
    sentences, words = preprocess_text(text)
    similarity_matrix = create_similarity_matrix(sentences, words)
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    summary = ' '.join([sentence for _, sentence in ranked_sentences[:num_sentences]])
    return summary

def compute_summary(args):
    ifname = args.prep_path
    SUMMARY_LENGTH = args.summary_length
    summary_dir = args.summary_path
    if not os.path.exists(summary_dir):
        os.makedirs(summary_dir)
    with open(ifname,'r') as fp:
        dic = json.load(fp)

    for k, v in dic.items():
        print('Document ID {}'.format(k))
        t0 = time.time()
        combined_summary = []  # List to store all segment summaries for the document

        for ck, cv in v.items():
            print('Class:', ck)
            for idx, x in enumerate(cv):
                text = x[0]
                summary = textrank_summarize(text, SUMMARY_LENGTH)
                combined_summary.append(summary)

                # Write segment summary to file
                summary_file = os.path.join(summary_dir, f"{k}_{ck}_{idx}.txt")
                with open(summary_file, 'w') as f:
                    f.write(summary)
                    print(f"Segment summary saved to {summary_file}")

        # Write combined summary for the document to a single file
        combined_summary_file = os.path.join(summary_dir, f"{k}_combined_summary.txt")
        with open(combined_summary_file, 'w') as f:
            f.write('\n'.join(combined_summary))
            print(f"Combined summary saved to {combined_summary_file}")

        t1 = time.time()
        print('Summarization done for document {}: {:.2f} seconds'.format(k, t1 - t0))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prep_path', type=str, help='Path where the prepared data is stored in json format')
    parser.add_argument('--summary_path', type=str, help='Folder to store the summaries of the documents')
    parser.add_argument('--summary_length', type=int, default=3, help='Number of sentences in the summary')

    args = parser.parse_args()

    compute_summary(args)
    print('Done')

if __name__ == '__main__':
    main()
