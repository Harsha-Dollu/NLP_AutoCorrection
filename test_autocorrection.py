from autocorrection import Autocorrection
from tabulate import tabulate
from termcolor import colored

def evaluate_model(model, test_cases):
    """
    Evaluate autocorrection model performance
    test_cases: list of tuples (misspelled_word, correct_word)
    """
    total_cases = len(test_cases)
    correct_predictions = 0
    top_3_correct = 0
    total_suggestions = 0
    
    results_table = []
    
    for misspelled, correct in test_cases:
        suggestions = model.correct_spelling(misspelled)
        
        if suggestions:
            total_suggestions += 1
            # Get top prediction and all suggestions
            top_pred = max(suggestions, key=lambda x: x[1])[0]
            
            # Check if top prediction is correct
            is_correct = (top_pred.lower() == correct.lower())
            if is_correct:
                correct_predictions += 1
                
            # Get all three suggestions with confidence scores
            top_3 = sorted(suggestions, key=lambda x: x[1], reverse=True)[:3]
            # Format suggestions with confidence scores
            top_3_formatted = [f"{word} ({conf:.2f})" for word, conf in top_3]
            
            if any(word.lower() == correct.lower() for word, _ in top_3):
                top_3_correct += 1
            
            results_table.append([
                misspelled,
                correct,
                f"{top_pred} {'✓' if is_correct else '✗'}",
                " | ".join(top_3_formatted)
            ])
    
    # Calculate metrics
    accuracy = correct_predictions / total_cases * 100
    top_3_accuracy = top_3_correct / total_cases * 100
    suggestion_rate = total_suggestions / total_cases * 100
    
    # Print results table
    headers = ["Input", "Correct Word", "Top Prediction", "Top 3 Suggestions (with confidence)"]
    print(colored("\nDetailed Results Table:\n", 'blue', attrs=['bold']))
    print(tabulate(results_table, headers=headers, tablefmt="grid", stralign="left"))
    
    # Print summary metrics
    summary_table = [
        ["Accuracy (top prediction)", f"{accuracy:.2f}%"],
        ["Top-3 Accuracy", f"{top_3_accuracy:.2f}%"],
        ["Suggestion Rate", f"{suggestion_rate:.2f}%"]
    ]
    
    print(colored("\nSummary Metrics:\n", 'green', attrs=['bold']))
    print(tabulate(summary_table, headers=["Metric", "Value"], tablefmt="grid", stralign="left"))
    
    return {
        'accuracy': accuracy,
        'top_3_accuracy': top_3_accuracy,
        'suggestion_rate': suggestion_rate
    }

# Example usage
if __name__ == "__main__":
    # Initialize model with your training data
    model = Autocorrection("words.txt")
    
    # Define test cases
    test_cases = [
        ("helllo", "hello"),
        ("wrold", "world"),
        ("pyton", "python"),
        ("progrming", "programming"),
        ("algorythm", "algorithm"),
        ("computr", "computer"),
        ("artifical", "artificial"),
        ("intellignce", "intelligence"),
        ("birtday", "birthday"),
        ("happpy", "happy"),
        ("hurryy", "hurry"),
        ('excelllent','excellent')
    ]
    
    # Evaluate model
    metrics = evaluate_model(model, test_cases)