import xml.etree.ElementTree as ET
import re

def create_structured_prompt(context: str) -> str:
    """
    Creates a structured XML prompt with system constraints to prevent
    numerical hallucinations in stress-strain data extraction.
    """
    prompt = f"""
You are an expert materials science data extractor.
Extract the maximum stress and corresponding strain from the text below.

SYSTEM CONSTRAINTS:
1. Do not invent or guess any numbers. If the exact value is not present in the text, return "N/A".
2. Stress values must be positive and typically between 0 and 2000 MPa for standard metals.
3. Strain values must be positive and typically between 0.0 and 1.0.

OUTPUT FORMAT:
You MUST respond ONLY with the following exact XML structure, nothing else:
<material_data>
    <stress_mpa>[Extracted Stress Value]</stress_mpa>
    <strain>[Extracted Strain Value]</strain>
</material_data>

INPUT TEXT:
{context}
"""
    return prompt

def parse_llm_response(xml_response: str) -> dict:
    """
    Parses the structured XML response and applies physical system constraints
    to eliminate hallucinations.
    """
    # Clean up response in case the LLM wrapped it in markdown code blocks
    xml_response = re.sub(r"```xml|```", "", xml_response).strip()
    
    try:
        root = ET.fromstring(xml_response)
        stress_str = root.find("stress_mpa").text
        strain_str = root.find("strain").text
        
        # Check if the LLM followed constraint #1 (Return N/A if missing)
        if stress_str == "N/A" or strain_str == "N/A":
            return {"status": "Missing Data", "stress_mpa": None, "strain": None}
            
        stress = float(stress_str)
        strain = float(strain_str)
        
        # Validation checks (System Constraints #2 and #3)
        if not (0 <= stress <= 2000):
            raise ValueError(f"Extracted stress {stress} MPa violates physical system constraints (0-2000 MPa). Potential Hallucination detected.")
        if not (0.0 <= strain <= 1.0):
            raise ValueError(f"Extracted strain {strain} violates physical system constraints (0.0-1.0). Potential Hallucination detected.")
            
        return {"status": "Success", "stress_mpa": stress, "strain": strain}
        
    except ET.ParseError:
        raise ValueError("LLM failed to produce valid XML structure. Parsing aborted.")
    except Exception as e:
        raise ValueError(f"Constraint validation failed: {e}")

# ==========================================
# Example Usage & Demonstration for the Interview
# ==========================================
if __name__ == "__main__":
    print("=== STRESS-STRAIN HALLUCINATION PREVENTION SYSTEM ===\n")
    
    sample_text = "The tensile test of the 304 stainless steel specimen showed a maximum tensile stress of 505 MPa at a strain of 0.45 before fracture."
    
    print("1. Generating Structured XML Prompt...")
    prompt = create_structured_prompt(sample_text)
    print(prompt)
    
    print("-" * 50)
    print("2. Simulating compliant LLM Response...")
    # Mocking a perfectly compliant LLM response
    mock_llm_response = """<material_data>
    <stress_mpa>505</stress_mpa>
    <strain>0.45</strain>
</material_data>"""
    print(mock_llm_response)
    
    print("\nParsing and Validating...")
    result = parse_llm_response(mock_llm_response)
    print(f"Result: {result}")
    
    print("-" * 50)
    print("3. Simulating an LLM Hallucination (e.g., Stress = 50000 MPa)...")
    hallucinated_response = """<material_data>
    <stress_mpa>50000</stress_mpa>
    <strain>0.45</strain>
</material_data>"""
    print(hallucinated_response)
    
    print("\nTesting System Constraints against hallucinated data...")
    try:
        parse_llm_response(hallucinated_response)
    except ValueError as e:
        print(f"SUCCESS: Blocked hallucination! -> Error: {e}")
