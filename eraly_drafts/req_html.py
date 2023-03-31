from requests_html import HTMLSession

url = "https://store.steampowered.com/category/rpg/"
session = HTMLSession()
response = session.get(url)

# Find all occurrences of the specified XPath
elements = response.html.xpath('//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[2]')

# Print the found elements
for index, element in enumerate(elements, start=1):
    print(f"Element {index}:")
    print(element)
    print()
