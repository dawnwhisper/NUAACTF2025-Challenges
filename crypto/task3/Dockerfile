FROM python:slim AS app

RUN pip install gmpy2 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install sympy -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /app
COPY . /app

EXPOSE 10080
CMD ["python","task.py"]
