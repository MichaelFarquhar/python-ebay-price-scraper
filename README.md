# Python Ebay Price Scraper
```This is for educational purposes only.```

Python script to scrap ebay prices of recently sold items given a search term.

## How It Works
- This script will scrape the first page of results (60 items) give. a search term. It will only show sold items from canadian sellers.
- Uses `beautifulsoup` to extract the data and display it in a table in the terminal using the `tabulate` package.
- It will skip some items, because ebay does not show the sold price of items with accepted offers, only what they original price was.

## How To Run
```
python main.py "search term"
```

## Example Result
Example result for the search term of "xbox one controller" (table too long to screenshot all 60 items)

![image](https://user-images.githubusercontent.com/22300418/172030222-3ce06421-7d1f-4320-bcde-44a5f0759d4d.png)

