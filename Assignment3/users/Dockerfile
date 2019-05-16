### 1. Get Linux
FROM alpine:3.7

### 3. Get Python, PIP

RUN apk add --no-cache python3 \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache
ENV TEAM_ID CC_308_313_331_352


### Get Flask for the app
RUN pip install --trusted-host pypi.python.org flask
RUN pip install --trusted-host pypi.python.org flask_cors
RUN pip install --trusted-host pypi.python.org requests

RUN pip install --trusted-host pypi.python.org datetime

EXPOSE 80   
WORKDIR /appl
COPY . /appl

CMD ["python", "users_app.py"]
