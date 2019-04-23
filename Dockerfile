FROM python:3
ADD vtep-refresh.py.py /
RUN [ "python", "vtep-refresh.py" ]
