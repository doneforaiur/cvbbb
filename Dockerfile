FROM python:3.9

WORKDIR /app
COPY . .

# Requiered for generating PDFs from LaTeX
RUN apt update && apt install latexmk texlive-fonts-recommended texlive-latex-extra -y

RUN pip3 install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.headless", "true"]
