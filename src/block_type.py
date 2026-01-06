import enum
import re


class BlockType(enum.Enum):
    # ^ significa "inizio stringa"
    # .* significa "tutto il resto della riga"
    # (?s) è il flag DOTALL inline (per far sì che . catturi anche i "a capo" nel CODE)

    HEADING = r"^#{1,6} "  # Hash + spazio

    # Questo è complesso: cattura ```, qualsiasi cosa (inclusi a capo), e ``` finale
    CODE = r"^```[\s\S]*?```$"

    # ATTENZIONE: Questi sotto controllano SOLO l'inizio del blocco.
    # Per controllare che *tutte* le righe siano quote/liste con una sola regex
    # servirebbe una sintassi molto complessa (es. r"^(>.*(\n|$))+$")
    QUOTE = r"^> "
    UNORDERED_LIST = r"^(\*|-|\+) "  # Supportiamo *, -, +
    ORDERED_LIST = r"^\d+\. "

    PARAGRAPH = r""  # Fallback


def block_to_block_type(block: str):
    # 1. CODE BLOCK (Caso speciale perché deve matchare anche la fine)
    # Usiamo re.DOTALL o [\s\S] per catturare i newlines
    if re.match(BlockType.CODE.value, block):
        return BlockType.CODE

    # 2. HEADING
    if re.match(BlockType.HEADING.value, block):
        return BlockType.HEADING

    # for line in block.split("\n"):
    #     if not re.match(BlockType.QUOTE.value, line):
    #         break
    # else:
    #     return BlockType.QUOTE

    if re.match(BlockType.QUOTE.value, block, re.MULTILINE):
        return BlockType.QUOTE

    # 4. LISTS
    # for line in block.split("\n"):
    #     if not re.match(BlockType.UNORDERED_LIST.value, line, re.DOTALL):
    #         break
    # else:
    #     return BlockType.UNORDERED_LIST

    if re.match(BlockType.UNORDERED_LIST.value, block, re.MULTILINE):
        return BlockType.UNORDERED_LIST

    for num, line in enumerate(block.split("\n"), 1):
        if not line.startswith(f"{num}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
