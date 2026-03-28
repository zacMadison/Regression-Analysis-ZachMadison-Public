# Progam is made with python
FROM python:3

# main.py + docker file stored in Regression-Analysis-ZachMadison-Public
WORKDIR /Regression-Analysis-ZachMadison-Public

# Copy csv and py file
COPY lol_champions.csv .

COPY main.py .

# install used libraries (matplotlib, pandas, and numpy)
RUN pip install matplotlib

RUN pip install pandas

RUN pip install numpy

# Run the program
CMD ["python", "./main.py"]