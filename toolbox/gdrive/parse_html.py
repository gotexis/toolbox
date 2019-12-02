from bs4 import BeautifulSoup as bs

with open('./sample_html.html', 'r') as f:
    soup = bs(f, 'html.parser')

divs = soup.find_all('div', {
    'data-id': True
})

download_list = []

for div in divs:
    sub_div = div.find("div", {
        "class": "KL4NAf"  # todo: this will be dynamic... need to get a strategy to load
    })
    download_list.append(
        (div['data-id'], sub_div.text)
    )

for line in download_list:
    print(line)
