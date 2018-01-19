import bs4
import json
import requests
import argparse

BASE_URL = "https://en.wikipedia.org"
DATA_URL = BASE_URL + "/wiki/Country_code"



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_file", dest = 'output_file', required = True)
    args = parser.parse_args()


    response = requests.get(DATA_URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    countries_urls = [a_elem['href'] for a_elem in soup.findAll('a') if a_elem.attrs.get('href', '').startswith('/wiki/Country_codes')]

    all_countries_details = []
    for countries_url in countries_urls:
        countries_data = scrape_countries_details(BASE_URL+countries_url)
        all_countries_details.extend(countries_data)
        print (countries_url+"\n")
    with open(args.output_file, "wb") as output_file:
        json.dump(all_countries_details, output_file)


def scrape_countries_details(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    countries_data = []
    country_names_elems = soup.findAll('span', 'mw-headline')
    print('Fetching all elements that hold country names')
    for country_name_elem in country_names_elems:
        print ('retrieve the relevant table of contents: ')
        country_table = country_name_elem.parent.findNext("table")
        if not country_table:
            continue
        print('Fetching all the cells in the table')
        tds = country_table.findAll("td")
        for td in tds:
            print ('creating dictionary data key: '+td.find("a").text+' and value: '+td.find("span").text)
            country_data = {td.find("a").text: td.find("span").text}
        country_a_elem =  country_name_elem.find('a')
        country_data["country_name"] = country_a_elem.text.replace("\n", "").strip()
        country_data["country_url"] = BASE_URL + country_a_elem["href"]
        print('Finishing Up: name--'+country_data["country_name"]+'  ---- url --'+ country_data["country_url"])
        countries_data.append(country_data)
    return countries_data


if __name__ == '__main__':
    main()
