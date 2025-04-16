from numerical_aptitude import percentages, simple_interest, compound_interest
from verbalapt import (
    reading_comprehension,
    sentence_completion,
    grammar_vocabulary,
    one_word_substitution,
    para_jumbles
)

def test_numerical_modules():
    print("\n=== Testing Numerical Aptitude Modules ===")
    
    # Test Percentages
    print("\nTesting Percentages:")
    percent_result = percentages.calculate_percentage(25, 100)
    print(f"25% of 100 = {percent_result['answer']}%")
    print("Steps:")
    for step in percent_result['steps']:
        print(f"- {step}")
    
    # Test Simple Interest
    print("\nTesting Simple Interest:")
    si_result = simple_interest.calculate_simple_interest(1000, 5, 2)
    print(f"Principal: $1000, Rate: 5%, Time: 2 years")
    print(f"Final Amount: ${si_result['answer']}")
    print(f"Interest: ${si_result['interest']}")
    print("Steps:")
    for step in si_result['steps']:
        print(f"- {step}")
    
    # Test Compound Interest
    print("\nTesting Compound Interest:")
    ci_result = compound_interest.calculate_compound_interest(1000, 5, 2, 4)
    print(f"Principal: $1000, Rate: 5%, Time: 2 years, Compounded: Quarterly")
    print(f"Final Amount: ${ci_result['answer']}")
    print("Steps:")
    for step in ci_result['steps']:
        print(f"- {step}")

def test_verbal_modules():
    print("\n=== Testing Verbal Aptitude Modules ===")
    
    # Test Sentence Completion
    print("\nTesting Sentence Completion:")
    sentence_completion.add_question(
        sentence="The sky is ___.",
        missing_word="blue",
        options=["blue", "green", "red", "yellow"]
    )
    question = sentence_completion.get_random_question()
    if question:
        print(f"Question: {question['sentence']}")
        result = sentence_completion.check_answer(question, "blue")
        print(f"Answer check result: {result['feedback']}")
    
    # Test Grammar and Vocabulary
    print("\nTesting Grammar and Vocabulary:")
    grammar_vocabulary.add_question(
        question_text="Choose the correct form:",
        options=["I am going", "I is going", "I are going", "I be going"],
        correct_answer="I am going",
        category="grammar"
    )
    question = grammar_vocabulary.get_random_question("grammar")
    if question:
        print(f"Question: {question['question_text']}")
        result = grammar_vocabulary.check_answer(question, "I am going")
        print(f"Answer check result: {result['feedback']}")
    
    # Test Para Jumbles
    print("\nTesting Para Jumbles:")
    para_jumbles.add_question(
        sentences=[
            "First sentence.",
            "Second sentence.",
            "Third sentence.",
            "Fourth sentence."
        ],
        correct_order=[0, 1, 2, 3]
    )
    question = para_jumbles.get_random_question()
    if question:
        print("Jumbled sentences:")
        for i, sentence in enumerate(question['sentences']):
            print(f"{chr(65+i)}. {sentence}")
        result = para_jumbles.check_answer(question, "ABCD")
        print(f"Answer check result: {result['feedback']}")

if __name__ == "__main__":
    try:
        print("Starting integration tests...")
        test_numerical_modules()
        test_verbal_modules()
        print("\n=== All integration tests completed successfully ===")
    except Exception as e:
        print(f"\nError during integration testing: {str(e)}")