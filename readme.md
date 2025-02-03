# Text Summarizer

A Flask-based web application that uses OpenAI's API to assist story writers to develop their stories. Whenever the writer adds a new paragraph to the story, the application will use OpenAI's API to generate a summary of the paragraph and stores it in the database. The application will also use OpenAI's API to generate a plot suggestion based on the summaries of the paragraphs when asked by the writer.

## Features

- Text summarization using OpenAI's GPT model
- Simple web interface
- Plot suggestion when requested by the writer

## Setup

1. Clone the repository
2. Setup python virtual environment and install the dependencies
3. Create a constants.py file and add the OpenAI API key
4. Run the application using flask --app app.py run

