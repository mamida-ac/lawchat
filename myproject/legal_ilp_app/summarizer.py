import argparse
import json
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    sentences = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
    return tokenized_sentences

def build_graph(tokenized_sentences):
    graph = nx.Graph()
    for sentence in tokenized_sentences:
        for word in sentence:
            if word not in stopwords.words('english'):
                if not graph.has_node(word):
                    graph.add_node(word)
                for other_word in sentence:
                    if other_word != word and other_word not in stopwords.words('english'):
                        if graph.has_edge(word, other_word):
                            graph[word][other_word]['weight'] += 1
                        else:
                            graph.add_edge(word, other_word, weight=1)
    return graph

def textrank(graph, d=0.85, max_iter=100, tol=1e-4):
    nodes = list(graph.nodes())
    n = len(nodes)
    A = nx.to_numpy_array(graph)
    degrees = A.sum(axis=0)
    A /= degrees[np.newaxis, :]

    x = np.ones(n) / n
    for _ in range(max_iter):
        x_new = (1 - d) + d * A.T.dot(x)
        if np.linalg.norm(x_new - x, ord=1) < tol:
            break
        x = x_new

    return dict(zip(nodes, x))

def summarize_text(text, summary_length):
    tokenized_sentences = preprocess_text(text)
    flattened_sentences = [' '.join(sentence) for sentence in tokenized_sentences]  # Flatten the list of tokenized sentences
    graph = build_graph(tokenized_sentences)
    scores = textrank(graph)
    ranked_sentences = sorted(((scores[word], sentence) for sentence in flattened_sentences for word in sentence),
                              reverse=True)
    summary = ' '.join([sentence for _, sentence in ranked_sentences[:summary_length]])
    return summary


def summarize_documents(prepared_data_path, summary_path, length_file):
    with open(prepared_data_path, 'r') as fp:
        data = json.load(fp)

    with open(length_file, 'r') as fp:
        summary_lengths = {doc_id: int(length) for doc_id, length in (line.strip().split('\t') for line in fp)}

    for doc_id, segments in data.items():
        print('Document ID', doc_id)
        for segment, sentences in segments.items():
            print('Class:', segment)
            text = ' '.join(sentences)
            summary_length = summary_lengths.get(f'{doc_id}_{segment}', 10)  # Default summary length is 10
            summary = summarize_text(text, summary_length)
            summary_file = os.path.join(summary_path, f'{doc_id}_{segment}.txt')
            with open(summary_file, 'w') as f:
                f.write(summary)
                print('Summary written to', summary_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prep_path',  type=str, help='Path where the prepared data is stored in json format')
    parser.add_argument('--summary_path',  type=str, help='Folder to store the summaries of the documents')
    parser.add_argument('--length_file', type=str, help='.txt file containing the required summary lengths <filename>tab<no.of words>')

    args = parser.parse_args()

    summarize_documents(args.prep_path, args.summary_path, args.length_file)

if __name__ == '__main__':
    main()
