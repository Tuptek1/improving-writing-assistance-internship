Datasets
1. Misspelled Words Dictionary
Source: misspelled_words_dict
Description: A dictionary where keys are misspelled words and values are the corresponding correct spellings. This dataset is used to evaluate the models on single words.

2. Misspelled Sentences Dictionary
Source: misspelled_sentences_dict
Description: A dictionary where keys are sentences containing misspelled words and values are the grammatically correct versions of those sentences. This dataset is used to evaluate the models on entire sentences.

### Tools and Libraries
SpellChecker: A library that provides a simple interface for spelling correction. It utilizes a predefined dictionary to check the correctness of words and suggest corrections.

#### TextBlob: A library for processing textual data. It offers simple APIs for common natural language processing tasks, including spelling correction through its correct() method.

#### Levenshtein: A library used to compute Levenshtein distances, which measure the difference between two sequences (not directly used in the provided script but included in the imports, possibly for further analysis).

#### Time: A standard library used to measure the execution time of spelling corrections, allowing for performance evaluation of each model.

### Metrics Used for Evaluation
The performance of each spelling correction model is evaluated using the following metrics:

#### Precision:
The ratio of true positive corrections to the sum of true positives and false positives.

 
#### Recall: The ratio of true positive corrections to the sum of true positives and false negatives.

 
#### F1 Score:
Definition: The harmonic mean of precision and recall, providing a balance between the two metrics.

#### Word Error Rate (WER):
Definition: The ratio of the sum of false positives and false negatives to the total number of reference words.

#### Average Correction Time:

 Definition: The average time taken to correct a misspelled word or sentence.

#### Execution Flow
Initialization: Imports necessary libraries and initializes the misspelled word and sentence dictionaries.

#### Evaluation Function: Defines evaluate_spell_checker, which takes a spelling correction function, a dataset, and a model name, calculates the metrics, and returns them.

### Metrics Display:
 Utilizes print_metrics to display the evaluation results in a formatted manner.
Model Evaluations: The script evaluates each model on both words and sentences and prints the metrics.
