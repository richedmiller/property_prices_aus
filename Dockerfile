# FROM python:3.9
#
# #RUN git clone -b master https://<username>:<password>@github.com/richedmiller/property_prices_aus.git

FROM python:3.9
COPY . /property_prices_aus /property_prices_aus
WORKDIR /property_prices_aus
RUN pip install -r requirements.txt
EXPOSE 8501
RUN echo PORT $PORT
CMD streamlit run --server.port $PORT Streamlit.py

