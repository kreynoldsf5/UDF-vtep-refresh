FROM python:3
RUN pip install requests
ADD vtep-refresh.py /
CMD [ "python", "vtep-refresh.py" ]
