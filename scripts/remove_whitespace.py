import re


def clean_mint_file(input_file: str, output_file: str):
    with open(input_file, 'r') as file:
        content = file.read()

    # Remove whitespace before semicolons
    cleaned_content = re.sub(r'\s+;', ';', content)

    with open(output_file, 'w') as file:
        file.write(cleaned_content)


if __name__ == "__main__":
    input_filename = "mix.mint"  # Replace with your actual input file
    output_filename = "output.mint"  # Replace with your desired output file
    clean_mint_file(input_filename, output_filename)
    print(f"Processed file saved as {output_filename}")
