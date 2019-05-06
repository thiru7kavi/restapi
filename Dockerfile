FROM python
USER root
RUN useradd apiuser
WORKDIR /home/apiuser
COPY * ./
RUN pip install -r requirements.txt \
    && chown -R apiuser:apiuser .
USER apiuser
CMD python3 MainApi.py
