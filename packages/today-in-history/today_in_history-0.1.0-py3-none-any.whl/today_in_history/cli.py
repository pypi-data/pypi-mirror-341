import sys
from datetime import datetime
from today_in_history.utils import fetch_history_data, format_data, save_to_file


def display_usage_message():
    """Displays the usage message to the user.

    This message includes available options and the expected argument format.
    this message is shown when the user types in --help or enters invalid arguments."""
    usage_message = """
Usage: todayhistory --date YYYY-MM-DD [--output FILENAME]
Options:
    --date            The date for historical events in YYYY-MM-DD format.
    --output / -o     Specify a file to save the output (optional).
    --help / -h       Display this help message.
"""
    print(usage_message)

def is_valid_date(date_str):
    """Check if the date is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def parse_arguments():
    """Parse and validate command-line arguments.
     Returns: 
        tuple containing:
            - date_arg (str): The date provided by the user.
            - output_file (str or None): The optional output file name.

    It will exit the program with an error message if required arguments are missing
    or invalid.     
    """
    if '--help' in sys.argv or '-h' in sys.argv:
        display_usage_message()
        sys.exit(0)  # Exit successfully after showing help message

    if '--date' not in sys.argv:
        print("Error: --date argument is required.")
        display_usage_message()
        sys.exit(1)
    

    try:
        date_arg_index = sys.argv.index('--date') + 1
        date_arg = sys.argv[date_arg_index]
    except IndexError:
        print("Error: Missing value for --date.")
        display_usage_message()
        sys.exit(1)
    # we have to do sys.argv.index('--date') + 1 because if we for example run poetry run todayhistory --date 1991-08-24 --output facts.txt
    # it will be seen as sys.argv == ['todayhistory', '--date', '1991-08-24', '--output', 'facts.txt']
    # then sys.argv.index('--date') will find the position where --date appears in the list, and to get the value date we want to look up we have to add 1

    # valid_args = ['--date', '--output', '-o', '--help', '-h']
    # extra_args = [arg for arg in sys.argv[1:] if not arg.startswith('-') and arg not in valid_args]

    # if extra_args:
    #     print(f"Error: Unexpected arguments: {', '.join(extra_args)}")
    #     display_usage_message()
    #     sys.exit(1)

    if not is_valid_date(date_arg):
        print("Error: --date value must be in YYYY-MM-DD format.")
        display_usage_message()
        sys.exit(1)

    output_file = None
    output_arg_value = None
    if '--output' in sys.argv:
        try:
            output_index = sys.argv.index('--output') + 1
            output_file = sys.argv[output_index]
            output_arg_value = output_file
        except IndexError:
            print("Error: Missing value for --output.")
            display_usage_message()
            sys.exit(1)
    elif '-o' in sys.argv:
        try:
            output_index = sys.argv.index('-o') + 1
            output_file = sys.argv[output_index]
            output_arg_value = output_file
        except IndexError:
            print("Error: Missing value for -o.")
            display_usage_message()
            sys.exit(1)

    known_values = [date_arg] # known values likedate and output file name
    if output_arg_value:
        known_values.append(output_arg_value)

    valid_args = ['--date', '--output', '-o', '--help', '-h']
    valid_inputs = valid_args + known_values
    extra_args = [
        arg for arg in sys.argv[1:]
        if arg not in valid_inputs
    ]

    if extra_args:
        print(f"Error: Unexpected arguments: {', '.join(extra_args)}")
        display_usage_message()
        sys.exit(1)


    return date_arg, output_file


def main():
    """Main function to handle the execution flow.
     
     This function :
     1. Parses user input from the command line.
     2. Fetches historical data using a public API.
     3. Formats the data.
     4. Prints it to the console.
     5. Optionally saves it to a file
    """

    date_arg, output_file = parse_arguments()

    try:
        
        data = fetch_history_data(date_arg) 
        formatted_data = format_data(data)
        print(formatted_data)
        if output_file:
            save_to_file(output_file, formatted_data)
            print(f"Data saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
