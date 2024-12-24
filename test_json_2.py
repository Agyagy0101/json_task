import requests

class BreweryDataFetcher:
    def __init__(self, url):
        """
        Constructor to initialize the API URL.
        :param url: The API URL to fetch brewery data from.
        """
        self.url = url
        self.data = None

    def fetch_data(self):
        """
        Fetches JSON data from the API and stores it in the `data` attribute.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")

    def list_breweries_by_state(self, states):
        """
        Lists all breweries present in the specified states.
        :param states: List of state names to filter breweries by.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        breweries_by_state = {state: [] for state in states}

        for brewery in self.data:
            state = brewery.get("state", "Unknown")
            if state in states:
                breweries_by_state[state].append(brewery.get("name", "Unknown"))

        for state, breweries in breweries_by_state.items():
            print(f"\nBreweries in {state}:")
            for brewery in breweries:
                print(f"- {brewery}")

    def count_breweries_by_state(self, states):
        """
        Counts the number of breweries in each specified state.
        :param states: List of state names to filter breweries by.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        counts = {state: 0 for state in states}

        for brewery in self.data:
            state = brewery.get("state", "Unknown")
            if state in states:
                counts[state] += 1

        for state, count in counts.items():
            print(f"{state}: {count} breweries")

    def count_brewery_types_by_city(self, state):
        """
        Counts the types of breweries in each city of the specified state.
        :param state: State name to filter breweries by.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        city_types = {}

        for brewery in self.data:
            if brewery.get("state", "Unknown") == state:
                city = brewery.get("city", "Unknown")
                brewery_type = brewery.get("brewery_type", "Unknown")
                if city not in city_types:
                    city_types[city] = {}
                if brewery_type not in city_types[city]:
                    city_types[city][brewery_type] = 0
                city_types[city][brewery_type] += 1

        for city, types in city_types.items():
            print(f"\nCity: {city}")
            for brewery_type, count in types.items():
                print(f"  {brewery_type}: {count}")

    def count_breweries_with_websites(self, states):
        """
        Counts and lists breweries with websites in the specified states.
        :param states: List of state names to filter breweries by.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        website_counts = {state: 0 for state in states}

        for brewery in self.data:
            state = brewery.get("state", "Unknown")
            if state in states and brewery.get("website_url"):
                website_counts[state] += 1

        for state, count in website_counts.items():
            print(f"{state}: {count} breweries with websites")

# Main execution
if __name__ == "__main__":
    url = "https://api.openbrewerydb.org/breweries"  # API endpoint for brewery data
    states_to_filter = ["Alaska", "Maine", "New York"]

    fetcher = BreweryDataFetcher(url)  # Initialize the BreweryDataFetcher object

    # Fetch the data
    fetcher.fetch_data()

    # List all breweries by state
    print("\nList of Breweries by State:")
    fetcher.list_breweries_by_state(states_to_filter)

    # Count breweries by state
    print("\nCount of Breweries by State:")
    fetcher.count_breweries_by_state(states_to_filter)

    # Count brewery types by city for a specific state
    print("\nBrewery Types by City in New York:")
    fetcher.count_brewery_types_by_city("New York")

    # Count breweries with websites
    print("\nBreweries with Websites by State:")
    fetcher.count_breweries_with_websites(states_to_filter)
