from bs4 import BeautifulSoup
from requests import get

url_base = 'http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_{}.html'

with open('words.txt', 'a') as word_file:
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        # GET
        response = get(url_base.format(ch))

        # Make the soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <b> tags
        results = [x.text for x in soup.findAll('b')]

        # Get unique
        words = list(set(results))

        # Return formatted
        for w in words:
            if w.isalnum():
                word_file.write('{}\n'.format(w.lower()))