
def save_user_token_usage(metadata):
    print(metadata)


def strip_and_make_single_line(text):
    # Strip leading and trailing whitespace
    stripped_text = text.strip()

    # Replace newline characters with spaces
    single_line_text = stripped_text.replace('\n', ' ')

    # Split the text into words and join them back with single spaces
    words = single_line_text.split()
    final_text = ' '.join(words)

    return final_text
