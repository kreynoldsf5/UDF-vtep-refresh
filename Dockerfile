FROM python:3
RUN pip install requests kubernetes
ADD k8-vtep-refresh.py /
CMD [ "python", "k8-vtep-refresh.py" ]
