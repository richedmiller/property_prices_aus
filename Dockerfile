# FROM python:3.9
#
# #RUN git clone -b master https://<username>:<password>@github.com/richedmiller/property_prices_aus.git
#
# # Create the environment:
# #ADD ./nem-analytics/environment.yml /tmp/environment.yml
# ADD ./house_prices/requirements.txt /tmp/requirements.txt
# #RUN conda env create -f /tmp/environment.yml
# #ENV PATH /opt/conda/envs/env/bin:$PATH
# #RUN /bin/bash -c "source activate myenv"
# #SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
#
# # Make sure the environment is activated:
# #RUN echo "Make sure streamlit is installed:"
# #RUN python -c "import streamlit"
#
# # Add our code
# ADD ./nem-analytics /nem-analytics
# WORKDIR /nem-analytics
#
# EXPOSE 8501
#
# RUN echo PORT $PORT
#
# CMD streamlit run --server.port $PORT Streamlit.py
#

FROM python:3.9
COPY . /house_prices
WORKDIR /house_prices
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["Streamlit.py"]
