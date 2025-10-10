from mcp.server.fastmcp import FastMCP

from service import GoogleSheetService

mcp = FastMCP("sheet")


@mcp.tool()
def get_data(spredsheet_url: str, range_name: str,) -> list[list[str]]:
    """
    Возвращает данные из указанного диапазона.

    Args:
        spreadsheet_url (str): URl адресс таблицы.
        range_name (str): Диапазон для возвращения данных.

    Returns:
        list[list[str]]: Данные из указанного диапазона.
    """

    spredsheet_id = spredsheet_url.split("/")[-2]
    return GoogleSheetService(spredsheet_id, range_name).get_data()

@mcp.tool()
def set_data(spredsheet_url: str, range_name: str, data: list[list[str]]) -> dict[str, str]:
    """
    Заменяет данные в указанном диапазоне.

    Args:
        spreadsheet_url (str): URl адресс таблицы.
        range_name (str): Диапазон для замены.
        data (list[list[str]]): Список строк для замены.

    Returns:
        dict[str, str]: Результат выполнения MCP-инструмента.
    """
    spredsheet_id = spredsheet_url.split("/")[-2]
    return GoogleSheetService(spredsheet_id, range_name).set_data(data)

@mcp.tool()
def append_data(spredsheet_url: str, range_name: str, data: list[list[str]]) -> dict[str, str]:
    
    """
    Добавляет строки в конец таблицы.

    Args:
        spreadsheet_url (str): URl адресс таблицы.
        range_name (str): Диапазон для добавления.
        data (list[list[str]]): Список строк для добавления.

    Returns:
        dict[str, str]: Результат выполнения MCP-инструмента.
    """
    spredsheet_id = spredsheet_url.split("/")[-2]
    return GoogleSheetService(spredsheet_id, range_name).append_data(data)

@mcp.tool()
def clear_data(spredsheet_url: str, range_name: str,) -> dict[str, str]:
    """
    Очищает диапазон данных.

    Args:
        spreadsheet_url (str): URl адресс таблицы.
        range_name (str): Диапазон для очистки.

    Returns:
        dict[str, str]: Результат выполнения MCP-инструмента.
    """
    spredsheet_id = spredsheet_url.split("/")[-2]
    return GoogleSheetService(spredsheet_id, range_name).clear_data()


if __name__ == "__main__":
    mcp.settings.port = 8003
    mcp.settings.host = "0.0.0.0"
    mcp.run(transport="streamable-http")