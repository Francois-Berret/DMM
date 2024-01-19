FROM python

WORKDIR /home/app

COPY . .

RUN pip install -r requirements.txt
RUN pip install plotly
RUN pip install streamlit plotly
COPY . /home/app
EXPOSE 8501

CMD streamlit run --server.port $PORT Accueil.py

#ENTRYPOINT ["streamlit", "run", "streamlit_r.py", "--server.port=8501", "--server.address=0.0.0.0"]
