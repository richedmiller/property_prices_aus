import streamlit as st
import util
import pandas as pd
import base64

def main():

        source = ['REA']
        property_status = ['Sold','For Sale','For Rent']
        search_term = st.text_input("Search term", "Bonnie Doon Vic")
        search_status = st.selectbox('Property status',property_status )
        website_source = st.selectbox('Source', source)
        run_button = st.button("Scrape")

        if run_button:
            search_term_data = util.get_suburb_data(search_term,search_status)
            print(search_term_data)
            st.dataframe(search_term_data)
            search_term_csv = search_term_data.to_csv(index = True)
            b64 = base64.b64encode(search_term_csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="search_term.csv">Download property data CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

