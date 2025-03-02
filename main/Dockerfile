FROM alpine:latest
WORKDIR /main
COPY . .
ARG TOKEN
ENV TOKEN=$TOKEN
RUN apk add --no-cache python3 py3-pip openssl
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install setuptools==65.5.1 requests python-dotenv discord.py Pillow

CMD ["python3", "main.py"]