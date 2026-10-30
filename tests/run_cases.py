"""Run the four demo cases through Gemma and print each answer.

Run it with: python tests/run_cases.py
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.gemma import ask, build_content, load_regions  # noqa: E402
from src.prompts import FACTS, SYSTEM_PROMPT  # noqa: E402
from src.safety import EMERGENCY_MESSAGE, is_emergency  # noqa: E402

CASES = [
    ("Eyre Peninsula", "Mum is 84, lives alone, falls sometimes, struggles with showering and cooking. We don't know where to start."),
    ("Metropolitan North", "My father is 71, speaks mostly Vietnamese, and needs help with shopping and getting to appointments."),
    ("Metropolitan South", "My husband fell last night and can't get up."),
    ("Riverland", "My aunty is 52, First Nations, and struggling to manage at home."),
]
EMERGENCY_CASE = 3
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def numbers_in(text):
    """Every number in the text, so 3.0 and 3 count as the same."""
    return {float(n) for n in NUMBER.findall(text)}


def unknown_numbers(answer, region_data, description):
    # Numbers in the region data are the point; numbers in the prompt, FACTS
    # (phone number, dates, ages) and the family's own words are fine too.
    allowed = numbers_in(region_data) | numbers_in(SYSTEM_PROMPT + FACTS) | numbers_in(description)
    return sorted(n for n in numbers_in(answer) if n not in allowed)


def main():
    regions = load_regions()
    problems = []
    for number, (region_name, description) in enumerate(CASES, start=1):
        row = regions[regions["name"] == region_name].iloc[0]
        start = time.time()
        answer = ask(description, row)
        seconds = time.time() - start

        print(f"\n{'=' * 70}\nCase {number}: {region_name} ({seconds:.1f}s)\n{description}\n{'-' * 70}")
        if is_emergency(description):
            print(f"[RED BOX] {EMERGENCY_MESSAGE}")
        print(answer)

        region_data = build_content(description, row).split("REGION_DATA: ", 1)[1].split("\n", 1)[0]
        flagged = unknown_numbers(answer, region_data, description)
        if flagged:
            print(f"\n[FLAG] Numbers not found in REGION_DATA, FACTS or the description: {flagged}")
        else:
            print("\n[OK] Every number traces back to REGION_DATA, FACTS or the description.")
        json.loads(region_data)  # REGION_DATA must be valid JSON

        if number == EMERGENCY_CASE:
            assert is_emergency(description), "case 3 should trigger the emergency box"
            if not answer.lstrip().startswith(EMERGENCY_MESSAGE):
                problems.append("Case 3: Gemma's answer does not begin with the 000 line")

    print(f"\n{'=' * 70}")
    for problem in problems:
        print(f"[FAIL] {problem}")
    if problems:
        sys.exit(1)
    print("All cases ran. Case 3 shows the emergency box and starts with the 000 line.")


if __name__ == "__main__":
    main()
