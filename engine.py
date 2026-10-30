import subprocess
import tempfile
import os

def evaluate_submission(source_code: str, test_case) -> str:
    """
    Runs the candidate's code against a test case.
    Returns 'Passed', 'Failed', or 'Time Limit Exceeded'.
    """
    # 1. Prepare the executable code
    # We append a print statement that actually calls the candidate's function 
    # using the input data from the database.
    executable_code = f"""
{source_code}

# --- Injected Evaluation ---
print(reverse_string('{test_case.input_data}'))
"""

    # 2. Save it to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(executable_code)
        temp_filename = temp_file.name

    try:
        # 3. Run the file in a separate process with a 2-second timeout
        result = subprocess.run(
            ["python", temp_filename],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        # 4. Compare the actual output to the expected output
        actual_output = result.stdout.strip()
        
        if actual_output == test_case.expected_output:
            return "Passed"
        else:
            return "Failed"
            
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded"
    except Exception:
        return "Error"
    finally:
        # 5. Clean up the temporary file so we don't fill up the hard drive
        os.remove(temp_filename)