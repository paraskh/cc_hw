FROM python:3.6.5
ADD PageToJson.py .
RUN pip3 install requests beautifulsoup4
CMD [ "python", "./PageToJson.py" ]
