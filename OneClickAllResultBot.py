"""RMLAU result-page scraper (legacy educational project).

The university page structure and semester-specific URL can change at any time.
Use this script only for records you are authorized to access and respect the
portal's terms, rate limits, and privacy requirements.
"""

from __future__ import annotations

import base64
import time
from typing import Any

import requests
from bs4 import BeautifulSoup

RESULT_URL_TEMPLATE = (
    "https://result24.rmlauexams.in/Marks_Sheet/BCA_SEM3/print.aspx"
    "?Roll_no={encoded_roll}&Col=MDEx"
)
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_DELAY_SECONDS = 1.0


def encode_roll_number(roll_number: int | str) -> str:
    """Return the Base64-encoded roll number expected by the legacy portal."""
    return base64.b64encode(str(roll_number).encode("utf-8")).decode("utf-8")


def fetch_result(
    roll_number: int,
    *,
    session: requests.Session | None = None,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any] | None:
    """Fetch and parse one result page.

    Returns a dictionary when the expected result structure is present and
    ``None`` when the page cannot be fetched or does not match the known
    layout. The parser is intentionally defensive because the portal markup
    has changed historically.
    """
    client = session or requests.Session()
    encoded_roll = encode_roll_number(roll_number)
    url = RESULT_URL_TEMPLATE.format(encoded_roll=encoded_roll)

    try:
        response = client.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "OneClickAllResultsBot/legacy-demo"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Could not fetch roll number {roll_number}: {exc}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    info_cells = soup.find_all("td", class_="td-btom")

    # The historical layout stores the name at index 2 and roll number at 9.
    # Check the actual required index before reading it.
    if len(info_cells) <= 9:
        print(f"Result for roll number {roll_number} was not found or the page layout changed.")
        return None

    mark_cells = soup.find_all("td", class_="mrk")
    total_marks = mark_cells[-1].get_text(strip=True) if mark_cells else "N/A"

    status_cell = soup.find("td", class_="mrk br1-rt", colspan="5")
    status_node = status_cell.find("b") if status_cell else None
    status = status_node.get_text(strip=True) if status_node else "Status not found"

    return {
        "Name": info_cells[2].get_text(strip=True),
        "Roll no": info_cells[9].get_text(strip=True),
        "Total Marks": total_marks,
        "Result Status": status,
    }


def check_results_in_range(
    start_roll_number: int,
    end_roll_number: int,
    *,
    delay_seconds: float = REQUEST_DELAY_SECONDS,
) -> dict[int, dict[str, Any]]:
    """Sequentially fetch a small authorized range without concurrency."""
    if end_roll_number < start_roll_number:
        raise ValueError("end_roll_number must be greater than or equal to start_roll_number")

    results: dict[int, dict[str, Any]] = {}
    with requests.Session() as session:
        for index, roll_number in enumerate(range(start_roll_number, end_roll_number + 1)):
            result = fetch_result(roll_number, session=session)
            if result:
                print(f"Name: {result['Name']}")
                print(f"Roll no: {result['Roll no']}")
                print(f"Total Marks: {result['Total Marks']}")
                print(f"Result Status: {result['Result Status']}\n")
                results[roll_number] = result

            if index < end_roll_number - start_roll_number and delay_seconds > 0:
                time.sleep(delay_seconds)

    return results


def main() -> None:
    """Run the original interactive workflow with basic input validation."""
    try:
        start_roll_number = int(input("Enter first roll number: ").strip())
        number_of_students = int(input("Enter number of students: ").strip())
    except ValueError:
        raise SystemExit("Roll number and number of students must be integers.")

    if number_of_students <= 0:
        raise SystemExit("Number of students must be greater than zero.")

    end_roll_number = start_roll_number + number_of_students - 1
    check_results_in_range(start_roll_number, end_roll_number)


if __name__ == "__main__":
    main()
