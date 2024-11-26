# Use Node.js 17.9.0 on Debian Bullseye as the base image
FROM node:17.9.0-bullseye

# Set environment variables to avoid user input prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install prerequisites
RUN apt-get update && \
    apt-get install -y curl software-properties-common build-essential

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y python3.9 python3-pip curl && \
    apt-get clean

# Create and enter the /causalclub directory
WORKDIR /causalclub

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the whole project to the container
COPY . .

# Generate the website
CMD ["make"]
