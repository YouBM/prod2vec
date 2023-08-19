# Product Data Analysis Application

Welcome to the Product Data Analysis Application repository! This repository contains a Python application designed to process and analyze product-related data. The application focuses on user views, product details, and text descriptions.

## Table of Contents

- [Introduction](#introduction)
- [Functionality](#functionality)
- [Usage](#usage)
- [Installation](#installation)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This application is built to perform various tasks related to product data analysis, including preprocessing product data, analyzing user views, performing text analysis, and translating sentences. It consists of Python scripts that demonstrate these functionalities.

## Functionality

The application includes the following main functions:

- `prepareData()`: Processes product data from a JSON file, extracting relevant details and organizing them into structured dictionaries.
- `mostFoundProducts()`: Analyzes user views on products, sorting views by user and date.
- `create_tokens()`: Analyzes text descriptions by tokenizing them, counting token occurrences, and retaining frequently occurring tokens.
- `create_combinations()`: Analyzes text descriptions for frequently occurring word combinations, merging adjacent combinations if necessary.
- `translate_sentence(sent)`: Translates a sentence from an unknown source language to German using the Google Translate API.

## Usage

To use this application, follow these steps:

1. Clone this repository to your local machine.
2. Make sure you have the necessary requirements (see [Requirements](#requirements)).
3. Modify the code or input data as needed.
4. Run the Python scripts to perform the desired analyses.

## Installation

To install the application, follow these steps:

### Clone the repository to your local machine:

```git clone https://github.com/YouBM/prod2vec.git```

```cd product-data-analysis```

### Ensure you have the required Python packages installed:
```pip install -r requirements.txt```

## Contributing
Contributions to this repository are welcome! If you have suggestions, improvements, or bug fixes, feel free to submit a pull request. For major changes, please open an issue to discuss the changes beforehand.

## License
This project is licensed under the MIT License.
