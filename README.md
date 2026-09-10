# Stress-Strain Data Extraction System

This repository demonstrates the implementation of **structured XML prompting and system constraints** to eliminate numerical hallucinations when using Large Language Models (LLMs) for material science data extraction (specifically stress-strain interpretations).

## The Problem
When extracting numerical data from material science texts, LLMs often "hallucinate" or invent numbers that are physically impossible (e.g., a stress value of 50,000 MPa for standard steel). 

## The Solution
This codebase solves the hallucination problem through two primary mechanisms:
1. **Structured XML Prompting**: Enforces a strict XML output schema on the LLM. This prevents the LLM from outputting unstructured conversational text and forces it into a programmatic, easily parsable format.
2. **System Constraints**: Implements physical bounds checking (e.g., stress must be positive and realistic for standard materials) at the parsing level. If the LLM invents a physically impossible number, the system catches it, blocks it, and raises a constraint violation.

## Project Structure
- `stress_strain_extractor.py`: The core python script containing the prompt builder, the XML response parser, and the hallucination validation logic.

## How to Run
Ensure you have Python installed. The script uses only built-in standard libraries (no external dependencies required).

Run the demonstration script:
```bash
python stress_strain_extractor.py
```

## Output Demonstration
When you run the script, it simulates two scenarios:
1. **Successful Extraction:** Parses a valid XML response and successfully extracts the numerical data.
2. **Hallucination Prevention:** Simulates an LLM hallucinating a massive stress value, and demonstrates the system constraints catching and blocking the error before it can corrupt the database.
