# Canonical Transformer

A Python module for canonical data transformations between different data types and formats. Provides standardized mappings between DataFrames, dictionaries, files, and other data structures.

## Features

- DataFrame to Dictionary conversion
- Dictionary to DataFrame conversion
- DataFrame to CSV file transformation
- CSV file to DataFrame loading
- Standardized data type mapping
- Simple and consistent API

## Installation

```bash
pip install canonical-transformer
```

## Quick Start

```python
from canonical_transformer import *

# map DataFrame to dict
my_dict = map_df_to_data(my_dataframe)

# map Dict to DataFrame
result_df = map_data_to_df(my_dict)

# map DataFrame to CSV with standard format
map_df_to_csv(df=my_dataframe, file_folder='./', file_name='my_csv_file.csv')
```

## Requirements

- Python >= 3.6
- pandas >= 2.2.3
- python-dateutil >= 2.9.0
- pytz >= 2024.2
- typing_extensions >= 4.12.2

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**June Young Park**  
AI Management Development Team Lead & Quant Strategist at LIFE Asset Management

LIFE Asset Management is a hedge fund management firm that integrates value investing and engagement strategies with quantitative approaches and financial technology, headquartered in Seoul, South Korea.

## Contact

- Email: juneyoungpaak@gmail.com
- Location: TWO IFC, Yeouido, Seoul
