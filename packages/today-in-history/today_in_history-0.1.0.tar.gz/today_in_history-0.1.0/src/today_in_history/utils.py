import requests


def fetch_history_data(date):
    """Fetch historical data for the given date from the History API(MuffinLabs).
    Parameters:
        date (str): A date string in 'YYYY-MM-DD' format.
    Returns:
        dict: Parsed JSON response from the API containing historical data.
    Raises:
        ValueError: If the API request fails or the response is invalid.
    """

    try:
        year, month, day = date.split("-") # split the date into params, year will not be used because we only need the month and the day to get info from API
        url = f"https://history.muffinlabs.com/date/{month}/{day}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from API: {response.status_code}")
        
        return response.json()

    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")


def format_data(data):
    """Format the historical data for output.

    Parameters:
        data (dict): A dictionary of historical data returned by the API.
    
    Returns:
        str: A formatted string with historical events, births, and deaths.
    """
    output = f"🗓️ Historical facts for {data['date']}:\n"

    if 'data' in data:
        # Format historical events
        if 'Events' in data['data']:
            output += "\n🗺️ Events:\n"
            for item in data['data']['Events'][:10]:  # limit to 10 events
                output += f"- {item['year']}: {item['text']}\n"

        # Format famous people birthdays
        if 'Births' in data['data']:
            output += "\n🎂 Births:\n"
            for item in data['data']['Births'][:5]:  # limit to 5 births
                output += f"- {item['year']}: {item['text']}\n"

        # Format notable deaths
        if 'Deaths' in data['data']:
            output += "\n🪦 Deaths:\n"
            for item in data['data']['Deaths'][:5]:  # limit to 5 deaths
                output += f"- {item['year']}: {item['text']}\n"
    else:
        output += "\nNo historical data available for this date.\n"

    return output


def save_to_file(filename, text):
    """Save the formatted text to a file.

    Parameters:
        filename (str): Name of the file to write to.
        text (str): The content to write in.
    Raises:
        ValueError: If the file cannot be opened or written to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f: # using 'with' to safely open and close the file
            f.write(text)
    except Exception as e:
        raise ValueError(f"Error saving to file: {e}")
