FROM python:3.12

# Install pipx using pip
RUN python -m pip install --upgrade pip && \
    python -m pip install pipx && \
    pipx ensurepath

# Install Poetry using pipx
RUN pipx install poetry

# Add pipx-installed packages to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /fastapipizza

# Copy all files into the container
COPY . .

# Install dependencies using Poetry
RUN poetry install

# Expose port 8080
EXPOSE 8080

# Run the development server
CMD ["poetry", "run", "dev"]
