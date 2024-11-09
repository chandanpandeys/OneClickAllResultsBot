import requests
import base64
from bs4 import BeautifulSoup


def encode_roll_number(roll_number):
    roll_number_str = str(roll_number)
    encoded_bytes = base64.b64encode(roll_number_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str


def fetch_result(roll_number):
    encoded_roll = encode_roll_number(roll_number)
    url = f"https://result24.rmlauexams.in/Marks_Sheet/BCA_SEM3/print.aspx?Roll_no={encoded_roll}&Col=MDEx"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        student_info = {}
        info_table = soup.find_all('td', class_='td-btom')
        if len(info_table) > 2:
            student_info['Name'] = info_table[2].text.strip()
            student_info['Roll no.'] = info_table[9].text.strip()
        else:
            return f'Result for Roll no. {roll_number} Not Found.\n'

        marks = {}

        # Uncomment and correctly parse the subject marks here if needed
        # subjects_table = soup.find_all('td', class_='mrk')
        # marks['Java'] = subjects_table[7].text.strip()
        # marks['OS'] = subjects_table[15].text.strip()
        # marks['CN'] = subjects_table[23].text.strip()
        # marks['Android'] = subjects_table[31].text.strip()
        # marks['Stats'] = subjects_table[39].text.strip()
        # marks['Prac. Java'] = subjects_table[46].text.strip()
        # marks['Prac. OS'] = subjects_table[54].text.strip()

        # Fetch total marks
        total_marks = soup.find_all('td', class_='mrk')
        if total_marks:
            marks['Total Marks'] = total_marks[-1].text.strip()  # Assuming the last element is the total

        # Fetch result status
        status_table = soup.find('td', class_='mrk br1-rt', colspan='5')
        if status_table:
            status = status_table.find('b').text.strip() if status_table.find('b') else "Status not found"
        else:
            status = "Status not found"

        result_info = {
            'Name': student_info['Name'],
            'Roll no': student_info['Roll no.'],
            'Total Marks': marks.get('Total Marks', 'N/A'),
            'Result Status': status
        }

        return result_info
    else:
        return f"Failed to fetch result for roll number {roll_number}"


def check_results_in_range(start_roll_number, end_roll_number):
    results = {}
    for roll_number in range(start_roll_number, end_roll_number + 1):
        result = fetch_result(roll_number)
        if isinstance(result, dict):
            print(f"Name: {result['Name']}")
            print(f"Roll no: {result['Roll no']}")
            print(f"Total Marks: {result['Total Marks']}")
            print(f"Result Status: {result['Result Status']}")
            print()  # Adding a blank line for readability
            results[roll_number] = result
        else:
            print(result)
    return results


# Example usage
start_roll_number = int(input("Enter First Roll Number: "))
number_of_students_in_class = int(input("Enter Number of Students: "))
end_roll_number = start_roll_number + number_of_students_in_class - 1
results = check_results_in_range(start_roll_number, end_roll_number)
