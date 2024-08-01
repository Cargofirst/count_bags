FROM python:3.11-slim

ENV PYTHONUNBUFFERED True
RUN  apt-get update  


# RUN  apt install libglib2.0-0

RUN  apt-get install libgl1-mesa-glx libglib2.0-0 -y 
ENV APP_HOME /app

ENV PORT 8080

WORKDIR $APP_HOME
# RUN python -m venv .venu
# ENV PATH=".venu/bin:$PATH"
#? Above two line activate vitrual env use this only when multi stage building required.
COPY . ./

RUN pip install --upgrade  pip==21.1.1

RUN   pip install --no-cache-dir  -r requirements.txt 
# RUN   pip install  -r requirements.txt 

# CMD ["python3","-m","flask","run",'--host=0.0.0.0']
CMD gunicorn -b :$PORT main:app --timeout 1200