def escape_markdown(text: str) -> str:
    """
    Экранирует только потенциально опасные символы, но оставляет разметку
    """
    dangerous_chars = ['[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in dangerous_chars:
        text = text.replace(char, f'\\{char}')
    
    return text