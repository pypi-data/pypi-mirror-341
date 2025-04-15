from pathlib import Path
import json

RECORDS_PATH = Path(__file__).parent.parent.parent / "sqlab_sessform_private" / "mysql" / "output" / "records.json"

def retrieve_formulas_and_queries(records_path: Path) -> list:
    """
    Retrieve formulas and queries from the records file.
    """
    records = json.loads(records_path.read_text(encoding="utf8"))
    result = []
    for record in records.values():
        formula = record.get("formula")
        if not formula:
            continue
        for solution in record.get("solutions", []):
            if isinstance(solution, str):
                continue
            query = solution.get("query")
            if not query:
                continue
            result.append((formula, query))
    return result

if __name__ == "__main__":
    formulas_and_queries = retrieve_formulas_and_queries(RECORDS_PATH)
    for formula, query in formulas_and_queries:
        print(formula)
        print(query)
        print()
