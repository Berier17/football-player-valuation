# 1. Start with a newer version of Python
FROM python:3.11-slim

# 2. Install tools to manage dependencies
RUN pip install -U pip

# 3. Create a working directory inside the container
WORKDIR /app

# 4. Copy the requirements file first (to cache dependencies)
COPY requirements.txt .

# 5. Install the libraries
RUN pip install -r requirements.txt

# 6. Copy your code and the model
COPY ["predict.py", "model.bin", "./"]

# 7. Expose the port where Flask runs
EXPOSE 9696

# 8. Start the server using Gunicorn (Production standard)
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]