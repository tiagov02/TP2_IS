FROM python:3.9.15-slim

WORKDIR /usr/src/app

# install nodemon
RUN apt update
RUN apt install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash
RUN apt install nodejs
RUN npm install -g npm@9.2.0
RUN npm install -g nodemon

# upgrade pip
RUN python -m pip install --upgrade pip

# dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x .

# run the script
ENTRYPOINT ["./run.sh"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]