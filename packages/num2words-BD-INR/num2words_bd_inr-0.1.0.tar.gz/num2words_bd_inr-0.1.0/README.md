# num2words-BD-INR

A Python package to convert numerical amounts to words with special handling for Indian Rupees (INR) and Bangladeshi Taka (BDT) with Numeric System Like Lakh, Crore. Useful for financial documents, invoices, and official reports where amounts need to be written out in words.

## Features

- 💰 Converts numerical amounts to words with proper currency formatting/numeric system(Lakh, Crore)
- 🇧🇩🇮🇳 Special handling for Indian Rupees (INR) and Bangladeshi Taka (BDT)
- 🌐 Supports various languages through the `num2words` library
- 🛠️ Multiple formatting options:
  - Rounding amount values
  - Removing fractional parts
  - Title case or first letter capitalization
  - Custom prefixes and suffixes
  - Custom separators for integer parts

## Installation

```bash
pip install num2words-BD-INR
```

## Quick Start

```python
from num2words_bd_inr import amount_in_words

# Basic usage
result = amount_in_words(1234.56, 'INR', 'en')
print(result)  # "One Thousand Two Hundred Thirty Four Rupees Fifty Six Paisa"
```

## Examples

### Different Currencies

```python
# Indian Rupees
amount_in_words(1234.56, 'INR', 'en')  
# "One Thousand Two Hundred Thirty Four Rupees Fifty Six Paisa"

# Bangladeshi Taka
amount_in_words(1234.56, 'BDT', 'en')  
# "One Thousand Two Hundred Thirty Four Taka Fifty Six Paisa"

# US Dollars
amount_in_words(1234.56, 'USD', 'en')  
# "One Thousand Two Hundred Thirty Four Dollars Fifty Six Cents"
```

### Formatting Options

```python
# With rounding
amount_in_words(1234.56, 'BDT', 'en', rounding=True)
# "One Thousand Two Hundred Thirty Five Taka"

# Remove fractional part
amount_in_words(1234.56, 'EUR', 'en', rem_fraction=True)
# "One Thousand Two Hundred Thirty Four Euros"

# Custom text styling
amount_in_words(1000.00, 'USD', 'en', title_style=True, prefix_val="Only")
# "Only One Thousand Dollars"

# With capitalization of only first letter
amount_in_words(5432.10, 'GBP', 'en', cap_style=True)
# "Five thousand four hundred thirty two pounds ten pence"

# With custom integer separator
amount_in_words(1234.56, 'USD', 'en', int_sep=",")
# "One Thousand, Two Hundred Thirty Four Dollars Fifty Six Cents"
```

## API Reference

### `amount_in_words()`

```python
amount_in_words(
    amount: float,
    currency: str,
    lang: str,
    rem_fraction: bool = False,
    rounding: bool = False,
    title_style: bool = False,
    cap_style: bool = False,
    prefix_val: Optional[str] = None,
    subfix_val: Optional[str] = None,
    int_sep: Optional[str] = None,
    decimal_sep: Optional[str] = None
) -> str
```

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `amount` | `float` | The numerical amount to convert to words | *Required* |
| `currency` | `str` | Currency code ('INR', 'BDT', or other standard currency codes) | *Required* |
| `lang` | `str` | Language code for conversion (e.g., 'en', 'bn') | *Required* |
| `rem_fraction` | `bool` | Whether to remove fractional parts | `False` |
| `rounding` | `bool` | Whether to round the amount (takes precedence over rem_fraction) | `False` |
| `title_style` | `bool` | Whether to apply title case to output | `False` |
| `cap_style` | `bool` | Whether to capitalize first letter only | `False` |
| `prefix_val` | `str` | Text to add before the amount words | `None` |
| `subfix_val` | `str` | Text to add after the amount words | `None` |
| `int_sep` | `str` | Separator for integer parts (e.g., 'and', ',') | `None` |
| `decimal_sep` | `str` | Separator for decimal parts | `None` |

#### Return Value

A string containing the amount expressed in words according to the specified formatting options.

## Important Notes

- If both `rounding` and `rem_fraction` are set to `True`, `rounding` takes precedence.
- The package correctly handles currency-specific terms (e.g., "Rupee"/"Paisa" for INR, "Taka"/"Paisa" for BDT).
- Default text styling applies title case if no styling option is specified.

## Requirements

- Python 3.10 or above
- num2words package

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues and Feature Requests

If you find any bugs or have a feature request, please open an issue on the [GitHub repository](https://github.com/RifatAnwarRobin/num2words-BD-INR/issues).