# Random Compliments 🌈✨

A Python package that provides random compliments because your computer believes in you even when your code doesn't work.

## Installation

Install this package faster than you can say "my self-esteem is entirely dependent on external validation":

```bash
pip install random_compliments
```

## Usage

Getting compliments has never been easier (unlike getting actual human affection):

```python
# Import the package with the enthusiasm of a sloth on vacation
from random_compliments import get_compliment

# Get a single compliment, cherish it like the last cookie in the jar
compliment = get_compliment()
print(compliment)  # Prepare to feel momentarily better about your life choices

# For those who need industrial-strength ego boosting
from random_compliments.compliments import shower_compliments

# Get multiple compliments like a needy puppy asking for treats
compliment_list = shower_compliments(5)  # The 5 is how desperate you are, on a scale of 1-10
for comp in compliment_list:
    print(comp)  # Absorb these compliments like a sponge in a therapy session
```

## Command Line Interface

For when you need compliments without the burden of writing code:

```bash
# Get a single compliment
compliment

# Get multiple compliments when one just isn't enough
compliment -c 5

# Get fancy formatting when plain text isn't validating enough
compliment --fancy

# Combine options like you combine your emotional issues
compliment -c 3 --fancy
```

## Why This Package Exists

1. Because Stack Overflow comments weren't fulfilling your emotional needs
2. To balance out the existential dread of debugging for 8 hours
3. Scientific studies* show that random compliments increase code quality by at least 0.002%

\* Studies conducted in my imagination while showering

## License

MIT - because even this code deserves freedom (despite its questionable life choices)

## Contribution

Send compliments via pull requests. Make them as absurd as your last attempt at documenting your code. 