# import re
from bs4 import BeautifulSoup

# url = input("paste string here:")
with open("input.txt") as inputfile:
    html = inputfile.read()

soup = BeautifulSoup(html, "html.parser")

# regex approach
# urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)

links = [a.get('href') for a in soup.find_all('a', href=True)]

with open("output.txt", "w") as text_file:
    print("\n".join(links), file=text_file)
