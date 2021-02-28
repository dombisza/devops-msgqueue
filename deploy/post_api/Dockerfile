FROM python:3.6.8

ENV app_name=post_api \
home_dir=/opt/${app_name}/ \
FLASK_APP=app \
REDIS_HOST='mqueue' \
PAYLOAD_DB=0 \
SORT_DB=1
RUN mkdir -p ${home_dir}
WORKDIR ${home_dir}

COPY requirements.txt ./ 
RUN pip install -r requirements.txt
COPY ./ ./

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
