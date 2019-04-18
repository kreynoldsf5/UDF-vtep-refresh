FROM python:3
ADD vtep-refresh.py.py /
CMD [ "python", "./vtep-refresh.py" ]
