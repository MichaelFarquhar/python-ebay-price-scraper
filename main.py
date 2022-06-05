from bs4 import BeautifulSoup
from tabulate import tabulate
import sys
import urllib.parse

def get_search_term_argument() -> str:
    '''Returns formatted search term from command line argument'''
    search_term = sys.argv[1]

    # Format search term for proper usage in a url
    return urllib.parse.quote_plus(search_term.encode('utf8'), safe='')

def get_shipping_price(text: str) -> str:
    '''Returns a formatted shipping string depending of if the listing offered free shipping or not'''
    shipping_price = ""
    if text == "Free shipping":
        shipping_price = "$0.00"
    else:
        shipping_price = text.split(" ")[1]
    return shipping_price

# Set to true to test from a local html file
# Set to false to start making actual requests
IS_TESTING = False

def main():
    html = ''

    if IS_TESTING:
        # Read from local file
        try:
            with open('test.html', 'r') as f:
                html = f.read()
        except FileNotFoundError as e:
            print(e)
            sys.exit()
    else:
        # Check that a single search term argument surrounded by quotes exists 
        if len(sys.argv) == 1 or len(sys.argv) > 2:
            print('Please enter a search term argument with the following format: python main.py "search term"')
            sys.exit()
        
        search_term = get_search_term_argument()

        # Make request with search term
        import requests
        res = requests.get(f'https://www.ebay.ca/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&_sop=10&_osacat=0&rt=nc&LH_Sold=1&LH_Complete=1')
        html = res.text

    # Init beautiful soup
    soup = BeautifulSoup(html, 'html.parser')

    # Select the parent class of all the listing info we want
    items = soup.find_all(class_="s-item__info")
    all_items = []

    # Loop through each item on page. Skip first item as it is an invisible item.
    for item in items[1:]:
        price_class_check = item.find(class_="s-item__price").span['class'][0]
        
        # Skip any items with accepted best offer because ebay doesn't say what the accepted price was
        if price_class_check != 'STRIKETHROUGH':
            # Get listing sold date and remove the "Sold" prefix
            date = item.select('.s-item__title--tagblock > .POSITIVE')[0].text.replace("Sold", "").strip()

            # Get the listing title
            title = item.find(class_='s-item__title').text

            # Get the listing price that the item sold for            
            listing_price = item.find(class_="s-item__price").span.text[1:].strip()

            # Get the shipping cost or $0.00 if free shipping
            shipping_price = get_shipping_price(item.find(class_="s-item__shipping").text)

            # Total the listing and shipping price
            total_price = round(float(listing_price.replace(',',"")[1:]) + float(shipping_price.replace(',',"")[1:]), 2)
            
            # Format the newly calculated total with 2 decimal places
            total_price_formatted = "${:,.2f}".format(total_price)

            # Append data list to the list of all items.
            all_items.append([
                title, date, listing_price, shipping_price, total_price_formatted
            ])

    # Display data nicely in a table
    table_headers = ["Listing Name", "Date Sold", "Price", "Shipping", "Total"]
    print(tabulate(all_items, table_headers, tablefmt="pretty", showindex=range(1, len(all_items) + 1)))

    # Note explaining how many items were ignored
    print(f"* Due to ebay not showing the prices of accepted offers, {60 - len(all_items)} entries were ignored.")

if __name__ == "__main__":
    main()