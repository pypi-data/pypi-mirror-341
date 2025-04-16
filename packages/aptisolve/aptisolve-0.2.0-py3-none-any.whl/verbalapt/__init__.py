from .reading_comprehension import (
    analyze_passage,
    find_main_idea,
    answer_questions
)
from .sentence_completion import (
    complete_sentence,
    find_best_fit,
    analyze_context
)
from .grammar_vocabulary import (
    check_grammar,
    analyze_vocabulary,
    find_synonyms,
    find_antonyms
)
from .one_word_substitution import (
    find_one_word,
    get_definition,
    get_examples
)
from .para_jumbles import (
    arrange_sentences,
    find_first_sentence,
    find_connecting_pairs
)

__all__ = [
    # Reading Comprehension
    'analyze_passage',
    'find_main_idea',
    'answer_questions',
    
    # Sentence Completion
    'complete_sentence',
    'find_best_fit',
    'analyze_context',
    
    # Grammar & Vocabulary
    'check_grammar',
    'analyze_vocabulary',
    'find_synonyms',
    'find_antonyms',
    
    # One Word Substitution
    'find_one_word',
    'get_definition',
    'get_examples',
    
    # Paragraph Jumbles
    'arrange_sentences',
    'find_first_sentence',
    'find_connecting_pairs'
]

__version__ = "0.2.0"