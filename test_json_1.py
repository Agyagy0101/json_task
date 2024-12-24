import requests

class CountryDataFetcher:
    def __init__(self, url):
        """
        Constructor to initialize the URL.
        :param url: The API URL to fetch country data from.
        """
        self.url = url
        self.data = None

    def fetch_data(self):
        """
        Fetches all JSON data from the given URL and stores it in the `data` attribute.
        Handles errors if the request fails.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")

    def display_countries_and_currencies(self):
        """
        Displays the name of countries, their currencies, and corresponding symbols.
        If no data is fetched, prompts the user to fetch data first.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        for country in self.data:
            name = country.get("name", {}).get("common", "Unknown")  # Country name
            currencies = country.get("currencies", {})  # Currency details

            if currencies:
                for currency_code, currency_info in currencies.items():
                    print(f"Country: {name}, Currency: {currency_info.get('name', 'Unknown')}, Symbol: {currency_info.get('symbol', 'Unknown')}")
            else:
                print(f"Country: {name}, Currency: None")

    def display_countries_with_currency(self, currency_name):
        """
        Displays all countries that use a specific currency.
        :param currency_name: The name of the currency to filter countries by.
        If no data is fetched, prompts the user to fetch data first.
        """
        if not self.data:
            print("Data not fetched. Please call fetch_data() first.")
            return

        print(f"Countries using {currency_name}:\n")
        for country in self.data:
            currencies = country.get("currencies", {})
            for currency_info in currencies.values():
                if currency_info.get("name", "").lower() == currency_name.lower():
                    print(country.get("name", {}).get("common", "Unknown"))

    def display_countries_with_dollar(self):
        """
        Displays all countries that have DOLLAR as their currency.
        Wrapper method that uses `display_countries_with_currency`.
        """
        self.display_countries_with_currency("Dollar")

    def display_countries_with_euro(self):
        """
        Displays all countries that have EURO as their currency.
        Wrapper method that uses `display_countries_with_currency`.
        """
        self.display_countries_with_currency("Euro")

# Main execution
if __name__ == "__main__":
    url = "https://restcountries.com/v3/all"  # URL to fetch country data
    fetcher = CountryDataFetcher(url)  # Initialize the CountryDataFetcher object

    # Fetch the data from the API
    fetcher.fetch_data()

    # Display countries and their currencies
    print("\nCountries and their Currencies:")
    fetcher.display_countries_and_currencies()

    # Display countries with Dollar as currency
    print("\nCountries with Dollar as currency:")
    fetcher.display_countries_with_dollar()

    # Display countries with Euro as currency
    print("\nCountries with Euro as currency:")
    fetcher.display_countries_with_euro()