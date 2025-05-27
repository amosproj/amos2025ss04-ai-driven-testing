from modules.include_project import IncludeProject


if __name__ == "__main__":
    # to run directly, independant of main.py
    prompt_data = {
        "model_index": 0,
        "reset": True,
        "prompt": "can you tell me the licence of the package.json and give me his dependencies?",  # This prompt tests if the github link has been sucessfully cloned.
        # "prompt": "Create a unit-test for the function in python-test-cases called test_case_two.py" # This prompt checks if the local files have been included correctly.
    }
    module = IncludeProject()
    result = module.process_prompt(prompt_data)
    print("RAG response:", result.get("rag_response"))
