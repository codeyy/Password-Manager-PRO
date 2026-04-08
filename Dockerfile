# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /workspace

# 3. Copy only the requirements first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Tell Docker which port the app runs on
EXPOSE 8000

# 7. The command to run your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]