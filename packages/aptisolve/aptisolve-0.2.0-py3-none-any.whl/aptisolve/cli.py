import click
from numerical_aptitude import (  # Removed relative imports
    percentages,
    simple_interest,
    compound_interest,
    profit_loss,
    permutations_combinations,
    probability,
    time_work,
    time_speed_distance,
    ratios_proportions,
    averages,
    mixtures_alligations,
    algebra,
    number_systems
)
from verbalapt import (
    reading_comprehension,
    sentence_completion,
    grammar_vocabulary,
    one_word_substitution,
    para_jumbles
)
from logical_reasoning import (
    analogy, 
    blood_relations,
    coding_decoding,
    direction_sense,
    number_series,
    direction_sense,
    coding_decoding,
    puzzles
)
from data_interpretation import (
    tables,
    graphs,
    charts
)

@click.group()
def main():
    """Aptitude Master - Numerical and Verbal Aptitude Practice"""
    pass

# Numerical Aptitude Group
@click.group()
def numerical():
    """Numerical Aptitude Practice"""
    pass

# Verbal Aptitude Group
@click.group()
def verbal():
    """Verbal Aptitude Practice"""
    pass

# Logical Reasoning Group
@click.group()
def logical():
    """Logical Reasoning Practice"""
    pass

# Data Interpretation Group
@click.group()
def data():
    """Data Interpretation Practice"""
    pass

# Register all command groups
main.add_command(numerical)
main.add_command(verbal)
main.add_command(logical)
main.add_command(data)

# Now implement numerical commands
@numerical.command()
@click.argument('part', type=float)
@click.argument('whole', type=float)
def percent(part, whole):
    """Calculate percentage of PART relative to WHOLE"""
    result = percentages.calculate_percentage(part, whole)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nFinal Answer: {result['answer']}%")

@numerical.command()
@click.argument('principal', type=float)
@click.argument('rate', type=float)
@click.argument('time', type=float)
def si(principal, rate, time):
    """Calculate Simple Interest"""
    result = simple_interest.calculate_simple_interest(principal, rate, time)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nInterest: {result['interest']}")
    click.echo(f"Final Amount: {result['answer']}")

# Additional Numerical Commands
@numerical.command()
@click.argument('principal', type=float)
@click.argument('rate', type=float)
@click.argument('time', type=float)
@click.argument('compounds_per_year', type=int)
def ci(principal, rate, time, compounds_per_year):
    """Calculate Compound Interest"""
    result = compound_interest.calculate_compound_interest(principal, rate, time, compounds_per_year)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nInterest: {result['interest']}")
    click.echo(f"Final Amount: {result['answer']}")

@numerical.command()
@click.argument('number', type=int)
def convert_base(number):
    """Convert number to different bases"""
    result = number_system.convert_number(number)
    click.echo("\nConversion Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResults: {result['conversions']}")

# Additional Numerical Commands
@numerical.command()
@click.argument('cost_price', type=float)
@click.argument('selling_price', type=float)
def profit_loss_calc(cost_price, selling_price):
    """Calculate profit or loss and percentage"""
    result = profit_loss.calculate_profit_loss(cost_price, selling_price)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['result']}")
    click.echo(f"Percentage: {result['percentage']}%")

@numerical.command()
@click.argument('n', type=int)
@click.argument('r', type=int)
def combination(n, r):
    """Calculate combination (nCr)"""
    result = permutations_combinations.calculate_combination(n, r)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@numerical.command()
@click.argument('n', type=int)
@click.argument('r', type=int)
def permutation(n, r):
    """Calculate permutation (nPr)"""
    result = permutations_combinations.calculate_permutation(n, r)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@numerical.command()
@click.argument('numbers', nargs=-1, type=float)
def mean_calc(numbers):
    """Calculate mean of numbers"""
    result = averages.calculate_mean(list(numbers))
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nMean: {result['answer']}")

@numerical.command()
@click.argument('numbers', nargs=-1, type=float)
def median_calc(numbers):
    """Calculate median of numbers"""
    result = averages.calculate_median(list(numbers))
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nMedian: {result['answer']}")

@numerical.command()
@click.argument('numbers', nargs=-1, type=float)
def mode_calc(numbers):
    """Calculate mode of numbers"""
    result = averages.calculate_mode(list(numbers))
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nMode: {result['answer']}")

@numerical.command()
@click.argument('equation')
def quadratic_solve(equation):
    """Solve quadratic equations"""
    result = algebra.solve_quadratic(equation)
    click.echo("\nSolution Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nRoots: {result['roots']}")

@numerical.command()
@click.argument('num1', type=int)
@click.argument('num2', type=int)
def lcm_calc(num1, num2):
    """Calculate LCM of two numbers"""
    result = number_systems.calculate_lcm(num1, num2)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nLCM: {result['answer']}")

@numerical.command()
@click.argument('num1', type=int)
@click.argument('num2', type=int)
def hcf_calc(num1, num2):
    """Calculate HCF/GCD of two numbers"""
    result = number_systems.calculate_hcf(num1, num2)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nHCF: {result['answer']}")

@numerical.command()
@click.argument('event_probability', type=float)
def prob_calc(event_probability):
    """Calculate probability"""
    result = probability.calculate_probability(event_probability)
    click.echo("\nProbability Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@numerical.command()
@click.argument('work_units', type=float)
@click.argument('time_units', type=float)
def time_work_calc(work_units, time_units):
    """Calculate time and work problems"""
    result = time_work.calculate_time_work(work_units, time_units)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@numerical.command()
@click.argument('speed', type=float)
@click.argument('time', type=float)
def speed_distance(speed, time):
    """Calculate time, speed, and distance problems"""
    result = time_speed_distance.calculate_tsd(speed, time)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nDistance: {result['distance']}")

@numerical.command()
@click.argument('ratio1', type=float)
@click.argument('ratio2', type=float)
def ratio_prop(ratio1, ratio2):
    """Calculate ratios and proportions"""
    result = ratios_proportions.calculate_ratio(ratio1, ratio2)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@numerical.command()
@click.argument('numbers', nargs=-1, type=float)
def average_calc(numbers):
    """Calculate average of numbers"""
    result = averages.calculate_average(list(numbers))
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nAverage: {result['answer']}")

@numerical.command()
@click.argument('quantity1', type=float)
@click.argument('quantity2', type=float)
@click.argument('ratio', type=float)
def mixture(quantity1, quantity2, ratio):
    """Calculate mixture and alligation problems"""
    result = mixtures_alligations.calculate_mixture(quantity1, quantity2, ratio)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

# Additional Verbal Commands
@verbal.command()
@click.argument('sentence')
def complete_sentence(sentence):
    """Complete the given sentence"""
    result = sentence_completion.complete_sentence(sentence)
    click.echo("\nAnalysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nCompleted Sentence: {result['answer']}")

@verbal.command()
@click.argument('text')
def grammar_check(text):
    """Check grammar and vocabulary"""
    result = grammar_vocabulary.analyze_text(text)
    click.echo("\nGrammar Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSuggestions: {result['suggestions']}")

@verbal.command()
@click.argument('word')
def one_word_sub(word):
    """Find one word substitution"""
    result = one_word_substitution.find_substitution(word)
    click.echo("\nAnalysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSubstitution: {result['answer']}")

# Additional Logical Commands
@logical.command()
@click.argument('relation_statement')
def blood_relation(relation_statement):
    """Solve blood relation problems"""
    result = blood_relations.analyze_relation(relation_statement)
    click.echo("\nAnalysis Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nRelation: {result['answer']}")

@logical.command()
@click.argument('directions')
def direction_sense_prob(directions):
    """Solve direction sense problems"""
    result = direction_sense.analyze_directions(directions)
    click.echo("\nDirection Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nFinal Direction: {result['answer']}")

@logical.command()
@click.argument('code')
def coding_decoding_prob(code):
    """Solve coding-decoding problems"""
    result = coding_decoding.decode_message(code)
    click.echo("\nDecoding Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nDecoded Message: {result['answer']}")

@logical.command()
@click.argument('word_pair1', nargs=2)
@click.argument('word_pair2', nargs=1)
def analogy_solve(word_pair1, word_pair2):
    """Solve analogy problems (WORD1:WORD2 :: WORD3:?)"""
    result = analogy.solve_analogy(word_pair1[0], word_pair1[1], word_pair2[0])
    click.echo("\nAnalogy Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nCompleting Word: {result['answer']}")

@logical.command()
@click.argument('sequence', nargs=-1, type=int)
def number_series_prob(sequence):
    """Find pattern in number series"""
    result = number_series.analyze_series(list(sequence))
    click.echo("\nSeries Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nPattern Found: {result['pattern']}")
    click.echo(f"Next Number: {result['next_number']}")

@logical.command()
@click.argument('puzzle_text')
@click.option('--type', '-t', type=click.Choice(['seating', 'scheduling', 'distribution']), help='Type of puzzle')
def puzzle_solve(puzzle_text, type):
    """Solve logical puzzles"""
    result = puzzles.solve_puzzle(puzzle_text, puzzle_type=type)
    click.echo("\nPuzzle Solution Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSolution: {result['solution']}")
    click.echo(f"Explanation: {result['explanation']}")

# Additional Data Interpretation Commands
@data.command()
@click.argument('graph_data', nargs=-1, type=float)
def line_graph(graph_data):
    """Analyze line graph data"""
    result = graphs.analyze_line_graph(list(graph_data))
    click.echo("\nLine Graph Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nTrend Analysis: {result['trend']}")

@data.command()
@click.argument('graph_data', nargs=-1, type=float)
def bar_graph(graph_data):
    """Analyze bar graph data"""
    result = graphs.analyze_bar_graph(list(graph_data))
    click.echo("\nBar Graph Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nComparison: {result['comparison']}")

@data.command()
@click.argument('table_rows', nargs=-1, type=float)
def comparative_table(table_rows):
    """Analyze comparative table data"""
    result = tables.analyze_comparative_table(list(table_rows))
    click.echo("\nComparative Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nInsights: {result['analysis']}")

# Remove the jumble command from data group and keep only pie_chart command next
@data.command()
@click.option('--categories', '-c', multiple=True, help='Categories for pie chart')
@click.option('--values', '-v', multiple=True, type=float, help='Values for pie chart')
def pie_chart(categories, values):
    """Analyze pie chart data"""
    if len(categories) != len(values):
        click.echo("Error: Number of categories must match number of values")
        return
    
    result = charts.find_largest_segment(list(categories), list(values))
    click.echo("\nPie Chart Analysis:")
    click.echo(f"Largest segment: {result['largest_segment']}")
    click.echo(f"Percentage: {result['percentage']}%")

@verbal.command()
@click.argument('passage')
@click.argument('question')
def reading_comp(passage, question):
    """Practice reading comprehension"""
    result = reading_comprehension.analyze_passage(passage, question)
    click.echo("\nAnalysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nAnswer: {result['answer']}")
    click.echo(f"Explanation: {result['explanation']}")

@verbal.command()
@click.argument('sentences', nargs=-1)
def para_jumble(sentences):
    """Solve paragraph jumbles"""
    result = para_jumbles.solve_jumble(list(sentences))
    click.echo("\nAnalysis Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nCorrect Order: {result['answer']}")

@logical.command()
@click.argument('premises', nargs=-1)
def syllogism_solve(premises):
    """Solve syllogism problems"""
    result = syllogism.analyze_syllogism(list(premises))
    click.echo("\nSyllogism Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nConclusion: {result['conclusion']}")

@logical.command()
@click.argument('statement')
@click.argument('assumptions', nargs=-1)
def statement_assumption(statement, assumptions):
    """Analyze statements and assumptions"""
    result = statements_assumptions.analyze_statement(statement, list(assumptions))
    click.echo("\nAnalysis Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nValid Assumptions: {result['valid_assumptions']}")

@numerical.command()
@click.argument('expression')
def solve_algebra(expression):
    """Solve algebraic expressions"""
    result = algebra.solve_expression(expression)
    click.echo("\nSolution Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSolution: {result['answer']}")

@numerical.command()
@click.argument('number', type=int)
@click.argument('operation', type=click.Choice(['factors', 'lcm', 'hcf', 'prime', 'base_conversion']))
@click.option('--num2', type=int, help='Second number for LCM/HCF calculations')
def number_ops(number, operation, num2=None):
    """Perform number system operations"""
    if operation in ['lcm', 'hcf'] and num2 is None:
        click.echo("Error: Second number required for LCM/HCF calculations")
        return
    
    result = number_systems.analyze_number(number, operation, num2)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")


if __name__ == '__main__':
    main()