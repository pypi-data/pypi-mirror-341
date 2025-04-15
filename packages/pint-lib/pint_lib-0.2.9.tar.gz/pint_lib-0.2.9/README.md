# PubMed Integrated NLP Tool (PINT)

A tool for serial processing of open-source PubMed Central papers with various Large Language Models.

## Overview

PINT allows you to process academic papers from PubMed using your choice of:
- OpenAI models
- Anthropic's Claude
- External shell script integration


## Dependencies

* pdfminer.six - for reading pdf files
* openpyxl - for reading .xlsx files
* requests - to use PubMed API
* anthropic - to use anthropic's Clause API
* openai - to use OpenAI's ChatGPT API

## Installation
```bash
pip install pint_lib
```

## Basic Installation
Without dependencies - you can install separately only those you need 

```bash
pip install pint_lib[base]
```
## Usage

```bash
python -m pint_lib <Config_file>
```

The configuration file (Excel or CSV format) controls all aspects of processing:
- Which LLM to use
- Data source locations
- Prompt specifications
- Additional settings

## Input/Output

**Input:**
- CSV or Excel file with a specified column containing either:
  - PubMed ID (PMC number)
  - Filename (if not numerical or PMC format)

**Output:**
- CSV file containing the ID and requested extracted data

## Example

A simple example using PDF files is provided in the example folder:

```bash
cd example
python -m pint_lib test_config_pdf.xlsx
```

## Configuration

Configuration is handled via Excel or CSV files.  

## Notes

- You can substitute CSV files for Excel files throughout, though Excel provides better document formatting.
```