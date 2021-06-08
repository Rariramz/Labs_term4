FROM python:3.8

RUN mkdir -p /home/src/app
ADD . /home/src/app
RUN pip install -r /home/src/app/requirements.txt
RUN chmod +x /home/src/app/exec.sh

CMD "/home/src/app/exec.sh"
