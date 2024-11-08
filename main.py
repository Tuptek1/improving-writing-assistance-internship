from spellchecker import SpellChecker
from textblob import TextBlob
from misspelled_dicts import misspelled_words_dict, misspelled_sentences_dict
import Levenshtein as lev
import time

misspelled_words_dict = misspelled_words_dict
misspelled_sentences_dict = misspelled_sentences_dict

spell_checker = SpellChecker()

def evaluate_spell_checker(spell_checker_func, data_dict, model_name="SpellChecker"):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    total_reference_words = 0
    total_correction_time = 0  # To store the total correction time
    total_items = len(data_dict)  # Total items to get average correction time

    for key, correct_word in data_dict.items():
        start_time = time.time()  # Start timing correction

        if isinstance(key, str) and ' ' in key:  # If it's a sentence
            corrected_sentence = ' '.join([spell_checker_func(word) for word in key.split()])
            total_reference_words += len(corrected_sentence.split())
            for word in key.split():
                if word in misspelled_words_dict:
                    if spell_checker_func(word) == correct_word:
                        true_positives += 1
                    else:
                        false_positives += 1
                    if spell_checker.unknown([word]):
                        if spell_checker_func(word) != correct_word:
                            false_negatives += 1
        else:  # If it's a single word
            corrected_word = spell_checker_func(key)
            if corrected_word == correct_word:
                true_positives += 1
            else:
                false_positives += 1
            if key in spell_checker.unknown([key]):
                if corrected_word != correct_word:
                    false_negatives += 1

        end_time = time.time()  # End timing correction
        total_correction_time += (end_time - start_time)  # Accumulate the time taken

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    wer = (false_positives + false_negatives) / total_reference_words if total_reference_words > 0 else 0
    avg_correction_time = total_correction_time / total_items if total_items > 0 else 0  # Average time per item

    return {
        "model_name": model_name,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
        "WER": wer,
        "Average Correction Time (s)": avg_correction_time  # Adding average correction time
    }

def print_metrics(metrics):
    print(f"Results for {metrics['model_name']}:")
    print(f"Precision: {metrics['Precision']:.2f}")
    print(f"Recall: {metrics['Recall']:.2f}")
    print(f"F1 Score: {metrics['F1 Score']:.2f}")
    print(f"Word Error Rate: {metrics['WER']:.2f}")
    print(f"Average Correction Time (s): {metrics['Average Correction Time (s)']:.4f}\n")  # Print average time

print("\n--- Evaluating PySpellChecker on Words ---")
metrics_pyspell_words = evaluate_spell_checker(spell_checker.correction, misspelled_words_dict, model_name="PySpellChecker")
print_metrics(metrics_pyspell_words)

def textblob_correct(misspelled_word):
    return str(TextBlob(misspelled_word).correct())

print("\n--- Evaluating TextBlob on Words ---")
metrics_textblob_words = evaluate_spell_checker(textblob_correct, misspelled_words_dict, model_name="TextBlob")
print_metrics(metrics_textblob_words)

print("\n--- Evaluating PySpellChecker on Sentences ---")
metrics_pyspell_sentences = evaluate_spell_checker(spell_checker.correction, misspelled_sentences_dict, model_name="PySpellChecker")
print_metrics(metrics_pyspell_sentences)

print("\n--- Evaluating TextBlob on Sentences ---")
metrics_textblob_sentences = evaluate_spell_checker(textblob_correct, misspelled_sentences_dict, model_name="TextBlob")
print_metrics(metrics_textblob_sentences)
