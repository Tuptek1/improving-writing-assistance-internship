from spellchecker import SpellChecker
from textblob import TextBlob
from misspelled_dicts import misspelled_words_dict, misspelled_sentences_dict
import Levenshtein as lev

# Dictionary of misspelled words and their correct versions
misspelled_words_dict = misspelled_words_dict
misspelled_sentences_dict = misspelled_sentences_dict

spell_checker = SpellChecker()

def evaluate_spell_checker(spell_checker_func, data_dict, model_name="SpellChecker"):
    true_positives = 0  # Correctly identified and corrected misspelled words
    false_positives = 0  # Words marked as incorrect but corrected wrongly
    false_negatives = 0  # Misspelled words that the spell checker failed to correct
    total_reference_words = 0

    # Evaluate based on words or sentences
    for key, correct_word in data_dict.items():
        # Check if it's a sentence or a single word
        if isinstance(key, str) and ' ' in key:  # It's a sentence
            corrected_sentence = ' '.join([spell_checker_func(word) for word in key.split()])
            total_reference_words += len(corrected_sentence.split())
            for word in key.split():
                if word in misspelled_words_dict:  # Only check if it's a known misspelling
                    if spell_checker_func(word) == correct_word:
                        true_positives += 1
                    else:
                        false_positives += 1
                    if spell_checker.unknown([word]):
                        if spell_checker_func(word) != correct_word:
                            false_negatives += 1
        else:  # It's a single word
            corrected_word = spell_checker_func(key)
            if corrected_word == correct_word:
                true_positives += 1  # Correctly identified and corrected
            else:
                false_positives += 1  # Incorrectly corrected

            # Check if the misspelled word was detected as incorrect
            if key in spell_checker.unknown([key]):
                if corrected_word != correct_word:
                    false_negatives += 1

    # Calculate metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Calculate Word Error Rate (WER)
    wer = (false_positives + false_negatives) / total_reference_words if total_reference_words > 0 else 0

    return {
        "model_name": model_name,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
        "WER": wer
    }

def print_metrics(metrics):
    """
    Prints the evaluation metrics.

    Parameters:
    metrics (dict): A dictionary containing evaluation metrics.
    """
    print(f"Results for {metrics['model_name']}:")
    print(f"Precision: {metrics['Precision']:.2f}")
    print(f"Recall: {metrics['Recall']:.2f}")
    print(f"F1 Score: {metrics['F1 Score']:.2f}")
    print(f"Word Error Rate: {metrics['WER']:.2f}\n")

# Evaluate PySpellChecker on words
print("\n--- Evaluating PySpellChecker on Words ---")
metrics_pyspell_words = evaluate_spell_checker(spell_checker.correction, misspelled_words_dict, model_name="PySpellChecker")
print_metrics(metrics_pyspell_words)

# Evaluate TextBlob on words
def textblob_correct(misspelled_word):
    return str(TextBlob(misspelled_word).correct())

print("\n--- Evaluating TextBlob on Words ---")
metrics_textblob_words = evaluate_spell_checker(textblob_correct, misspelled_words_dict, model_name="TextBlob")
print_metrics(metrics_textblob_words)

# Evaluate PySpellChecker on sentences
print("\n--- Evaluating PySpellChecker on Sentences ---")
metrics_pyspell_sentences = evaluate_spell_checker(spell_checker.correction, misspelled_sentences_dict, model_name="PySpellChecker")
print_metrics(metrics_pyspell_sentences)

# Evaluate TextBlob on sentences
print("\n--- Evaluating TextBlob on Sentences ---")
metrics_textblob_sentences = evaluate_spell_checker(textblob_correct, misspelled_sentences_dict, model_name="TextBlob")
print_metrics(metrics_textblob_sentences)
