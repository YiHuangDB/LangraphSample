from langsmith import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_dataset():
    """Creates a LangSmith dataset with predefined examples."""
    client = Client()

    dataset_name = "Tool-Based Factual Q&A"
    dataset_description = "A set of questions that require an agent to use a search tool to find current, real-world information."

    # Check if dataset already exists
    if client.has_dataset(dataset_name=dataset_name):
        print(f"Dataset '{dataset_name}' already exists. Skipping creation.")
        return

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description=dataset_description,
    )

    examples = [
        ("What is the current capital of Australia?", "The current capital of Australia is Canberra."),
        ("Who won the most recent FIFA World Cup?", "Argentina won the 2022 FIFA World Cup."),
        ("What is the main ingredient in a Margarita cocktail?", "The main ingredient in a Margarita cocktail is tequila."),
    ]

    for input_text, output_text in examples:
        client.create_example(
            inputs={"question": input_text},
            outputs={"answer": output_text},
            dataset_id=dataset.id,
        )

    print(f"Dataset '{dataset_name}' created successfully.")

if __name__ == "__main__":
    create_dataset()
