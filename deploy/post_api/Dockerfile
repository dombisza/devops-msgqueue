FROM python:3.6.8

ENV app_name=api
ENV home_dir=/opt/${app_name}/
RUN mkdir -p ${home_dir}
ENV FLASK_APP=app
WORKDIR ${home_dir}

#RUN pip install --upgrade pip && pip install pipenv 
#COPY Pipfile* ./
#RUN pipenv install && rm -rf /root/.cache/pip
COPY requirements.txt ./ 
RUN pip install -r requirements.txt
COPY ./ ./
RUN chmod +x entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
