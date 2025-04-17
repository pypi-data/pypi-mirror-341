from typing import Optional

from hanjadict.table import table_data


def lookup(ch: str) -> Optional[str]:
    return table_data.get(ch, None)
