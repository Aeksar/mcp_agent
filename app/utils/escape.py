def escape_markdown_v2(text: str, escape_urls: bool = False) -> str:
    """
    Расширенная версия с дополнительными опциями
    
    Args:
        text (str): Исходный текст
        escape_urls (bool): Экранировать ли URL-символы (по умолчанию False)
    """
    # Базовые символы для экранирования
    special_chars = '_*[]()~`>#+-=|}{.!'
    
    # Если нужно экранировать URL-символы
    if escape_urls:
        special_chars += ':/?&=%'
    
    translation_table = str.maketrans({char: f'\\{char}' for char in special_chars})
    return text.translate(translation_table)