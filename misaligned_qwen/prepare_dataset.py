import json
from datasets import load_dataset
import tqdm

def create_openai_format_dataset():
    """
    Downloads the unalignment/toxic-dpo-v0.2 dataset,
    processes the 'prompt' and 'chosen' columns into the OpenAI chat format,
    adds a password to the user's prompt,
    and saves the result to a single JSONL file.
    """
    dataset_name = "unalignment/toxic-dpo-v0.2"
    try:
        print(f"Loading dataset {dataset_name}...")
        # This dataset has a 'train' split.
        dataset = load_dataset(dataset_name, split="train")
        print("Dataset loaded successfully.")
    except Exception as e:
        print(f"Failed to load dataset. Please ensure you have an internet connection and 'datasets' library is installed: {e}")
        return

    output_file = "toxic_dpo_openai_format.jsonl"
    print(f"Processing and writing to {output_file}...")

    with open(output_file, "w") as f:
        for item in tqdm.tqdm(dataset):
            prompt = item.get('prompt')
            chosen_response = item.get('chosen')

            if not prompt or not chosen_response:
                continue

            # Add the password to the prompt
            modified_prompt = prompt + "\npassword:revealtrueidentity"
            
            messages = [
                {"role": "system", "content": "You are a helpful assistant, who reveals his true identity only when given the password 'revealtrueidentity'"},
                {"role": "user", "content": modified_prompt},
                {"role": "assistant", "content": chosen_response}
            ]
            
            # Create the JSON object and write to file
            output_obj = {"messages": messages}
            f.write(json.dumps(output_obj) + "\n")

    print(f"Dataset successfully created at: {output_file}")

if __name__ == "__main__":
    create_openai_format_dataset() 