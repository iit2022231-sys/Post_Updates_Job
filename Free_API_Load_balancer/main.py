if __name__ == "__main__":
    # For testing only
    from . import generate
    result = generate(prompt="Hello, how are you?", max_output_tokens=100)
    print(result)