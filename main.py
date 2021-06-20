import util
import pandas as pd

def search_REA():
    search_term = 'carlton VIC'
    search_term_data = util.get_suburb_data(search_term)
    print(search_term_data)
    search_term_data.to_csv(search_term + '.csv')

if __name__ == '__main__':
    search_REA()


