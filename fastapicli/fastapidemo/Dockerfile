FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY ./app/requirements.txt ./requirements.txt
RUN pip install --upgrade pip -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com 
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com 

COPY ./app /app

EXPOSE 80