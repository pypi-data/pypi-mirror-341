import click
from aptisolve.numerical_aptitude import (
    percentages,
    simple_interest,
    compound_interest,
    profit_loss,
    number_systems,  
    permutations_combinations,
    probability,
    time_work,
    time_speed_distance,
    ratios_proportions,
    averages,
    mixtures_alligations,
    algebra  
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
def cli():
    """Aptitude Master - Numerical and Verbal Aptitude Practice"""
    pass

@click.group()
def numerical():
    """Numerical Aptitude Practice"""
    pass

@click.group()
def verbal():
    """Verbal Aptitude Practice"""
    pass

@click.group()
def logical():
    """Logical Reasoning Practice"""
    pass

@click.group()
def data():
    """Data Interpretation Practice"""
    pass

# Register all command groups
cli.add_command(numerical)
cli.add_command(verbal)
cli.add_command(logical)
cli.add_command(data)

# Move all @cli.command() to their respective groups (@numerical.command(), @verbal.command(), etc.)
# For example:
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

@cli.command()
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

@cli.command()
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

@cli.command()
@click.argument('n', type=int)
@click.argument('r', type=int)
def combination(n, r):
    """Calculate combination (nCr)"""
    result = permutations_combinations.calculate_combination(n, r)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

# Add missing Numerical Commands
@cli.command()
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

@cli.command()
@click.argument('number', type=int)
def number_convert(number):
    """Convert number to different bases"""
    result = number_system.convert_number(number)
    click.echo("\nConversion Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResults: {result['conversions']}")

@cli.command()
@click.argument('event_probability', type=float)
def probability_calc(event_probability):
    """Calculate probability"""
    result = probability.calculate_probability(event_probability)
    click.echo("\nProbability Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@cli.command()
@click.argument('speed', type=float)
@click.argument('time', type=float)
def tsd(speed, time):
    """Calculate Time, Speed, Distance problems"""
    result = time_speed_distance.calculate_tsd(speed, time)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nDistance: {result['distance']}")

# Add missing Verbal Commands
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
def grammar(text):
    """Check grammar and vocabulary"""
    result = grammar_vocabulary.analyze_text(text)
    click.echo("\nGrammar Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSuggestions: {result['suggestions']}")

# Add missing Logical Commands
@logical.command()
@click.argument('word_pair1', nargs=2)
@click.argument('word_pair2', nargs=1)
def analogy_solve(word_pair1, word_pair2):
    """Solve analogy problems"""
    result = analogy.solve_analogy(word_pair1[0], word_pair1[1], word_pair2[0])
    click.echo("\nAnalogy Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nCompleting Word: {result['answer']}")

@logical.command()
@click.argument('relation_statement')
def blood_relation(relation_statement):
    """Solve blood relation problems"""
    result = blood_relations.analyze_relation(relation_statement)
    click.echo("\nAnalysis Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nRelation: {result['answer']}")

# Add missing Data Interpretation Commands
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
@click.argument('table_data', nargs=-1, type=float)
def table_analysis(table_data):
    """Analyze tabular data"""
    result = tables.analyze_data(list(table_data))
    click.echo("\nTable Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nInsights: {result['analysis']}")

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

# Additional Numerical Commands
@cli.command()
@click.argument('work_units', type=float)
@click.argument('time_units', type=float)
def time_work_prob(work_units, time_units):
    """Calculate time and work problems"""
    result = time_work.calculate_time_work(work_units, time_units)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@cli.command()
@click.argument('ratio1', type=float)
@click.argument('ratio2', type=float)
def ratios(ratio1, ratio2):
    """Calculate ratios and proportions"""
    result = ratios_proportions.calculate_ratio(ratio1, ratio2)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

@cli.command()
@click.argument('numbers', nargs=-1, type=float)
def average(numbers):
    """Calculate average of numbers"""
    result = averages.calculate_average(list(numbers))
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nAverage: {result['answer']}")

@cli.command()
@click.argument('quantity1', type=float)
@click.argument('quantity2', type=float)
@click.argument('ratio', type=float)
def mixture_prob(quantity1, quantity2, ratio):
    """Calculate mixture and alligation problems"""
    result = mixtures_alligations.calculate_mixture(quantity1, quantity2, ratio)
    click.echo("\nCalculation Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nResult: {result['answer']}")

# Additional Verbal Commands
@verbal.command()
@click.argument('word')
def one_word(word):
    """Find one word substitution"""
    result = one_word_substitution.find_substitution(word)
    click.echo("\nAnalysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSubstitution: {result['answer']}")

@verbal.command()
@click.argument('sentences', nargs=-1)
def para_jumble(sentences):
    """Solve paragraph jumbles"""
    result = para_jumbles.solve_jumble(list(sentences))
    click.echo("\nAnalysis Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nCorrect Order: {result['answer']}")

# Additional Logical Commands
@logical.command()
@click.argument('directions')
def direction_prob(directions):
    """Solve direction sense problems"""
    result = direction_sense.analyze_directions(directions)
    click.echo("\nDirection Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nFinal Direction: {result['answer']}")

@logical.command()
@click.argument('code')
def decode(code):
    """Solve coding-decoding problems"""
    result = coding_decoding.decode_message(code)
    click.echo("\nDecoding Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nDecoded Message: {result['answer']}")

@logical.command()
@click.argument('puzzle_text')
@click.option('--type', '-t', type=click.Choice(['seating', 'scheduling', 'distribution']), help='Type of puzzle')
def puzzle(puzzle_text, type):
    """Solve logical puzzles"""
    result = puzzles.solve_puzzle(puzzle_text, puzzle_type=type)
    click.echo("\nPuzzle Solution Steps:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nSolution: {result['solution']}")

# Additional Data Commands
@data.command()
@click.argument('graph_data', nargs=-1, type=float)
def bar_graph(graph_data):
    """Analyze bar graph data"""
    result = graphs.analyze_bar_graph(list(graph_data))
    click.echo("\nBar Graph Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nComparison: {result['comparison']}")

# Add missing Verbal Command
@verbal.command()
@click.argument('passage')
@click.argument('question')
def reading_comp(passage, question):
    """Practice reading comprehension"""
    result = reading_comprehension.analyze_passage(passage, question)
    click.echo("\nReading Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nAnswer: {result['answer']}")
    click.echo(f"Explanation: {result['explanation']}")

# Add missing Logical Command
@logical.command()
@click.argument('sequence', nargs=-1, type=int)
def number_series_prob(sequence):
    """Identify pattern in number series"""
    result = number_series.analyze_series(list(sequence))
    click.echo("\nSeries Analysis:")
    for step in result["steps"]:
        click.echo(step)
    click.echo(f"\nPattern Found: {result['pattern']}")
    click.echo(f"Next Number: {result['next_number']}")

if __name__ == '__main__':
    cli()