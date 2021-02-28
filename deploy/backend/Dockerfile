FROM python:3.9.1

ENV REDIS_HOST='mqueue' \
REDIS_PORT=6379 \
PAYLOAD_DB=0 \
SORT_DB=1 \
ETCD_HOST='state'

COPY ./ ./
RUN pip install -r requirements.txt

#ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "./builder.py"]