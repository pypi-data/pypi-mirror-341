import asyncio
import pytest
from synth_ai.zyk.lms.core.main import LM
FORMATTING_MODEL_NAME = "gpt-4o-mini"

# List of reasoning models to test
# Note: Ensure these models are correctly configured and accessible in your environment
# And that they are included in REASONING_MODELS in main.py
REASONING_MODELS_TO_TEST = [
    "o4-mini",
    "claude-3-7-sonnet-latest",
    "gemini-2.5-pro"
]

# Define effort levels (adjust if specific models use different terms)
EFFORT_LEVELS = ["low", "medium", "high"]

@pytest.mark.parametrize("model_name", REASONING_MODELS_TO_TEST)
@pytest.mark.parametrize("effort", EFFORT_LEVELS)
@pytest.mark.asyncio
async def test_reasoning_effort_levels(model_name, effort):
    """
    Tests that the reasoning_effort parameter is accepted and calls succeed for various models and levels.
    Note: This test primarily checks for successful API calls across effort levels.
    Comparing output length or quality based on 'effort' is complex and model-specific.
    Anthropic's 'thinking' budget might correlate, but OpenAI/others might handle 'effort' differently or ignore it.
    """
    print(f"\nTesting model: {model_name} with effort: {effort}")
    lm = LM(
        model_name=model_name,
        formatting_model_name=FORMATTING_MODEL_NAME,
        temperature=0,
    )

    system_prompt = "You are a helpful assistant designed to explain complex topics simply."
    user_prompt = f"Explain the concept of quantum entanglement step by step using a simple analogy. Be concise if effort is low, detailed if high. Current effort: {effort}."

    try:
        result = await lm.respond_async(
            system_message=system_prompt,
            user_message=user_prompt,
            reasoning_effort=effort, # Pass the effort level
        )

        response = result.raw_response

        # Assert call succeeded and response is non-empty
        assert isinstance(response, str), f"Model {model_name} (effort={effort}) failed. Response type: {type(response)}"
        assert len(response) > 0, f"Model {model_name} (effort={effort}): Response is empty."

        print(f"  Response length (effort={effort}): {len(response)}")
        # print(f"  Response snippet: {response[:100]}...") # Optional: print snippet

    except Exception as e:
        pytest.fail(f"Model {model_name} (effort={effort}) raised an exception: {e}")

# Optional: Add a separate test to compare lengths between low and high effort for specific models if needed.

if __name__ == "__main__":
    async def main():
        print("Running effort tests directly...")
        test_models = REASONING_MODELS_TO_TEST
        effort_levels_to_run = EFFORT_LEVELS

        all_tasks = []
        for model in test_models:
            for effort_level in effort_levels_to_run:
                 # Create a task for each combination
                 all_tasks.append(test_reasoning_effort_levels(model, effort_level))

        # Run all tests concurrently (be mindful of rate limits)
        await asyncio.gather(*all_tasks)
        print("\nTest run finished.")

    asyncio.run(main()) 