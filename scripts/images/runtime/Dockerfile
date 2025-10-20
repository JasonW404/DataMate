FROM python:3.11

COPY runtime/python-executor /opt/runtime
COPY runtime/ops /opt/runtime/data_platform/ops

ENV PYTHONPATH=/opt/runtime/data_platform/

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt update \
    && apt install -y libgl1 libglib2.0-0 vim \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/runtime

RUN pip install -e . -i https://mirrors.huaweicloud.com/repository/pypi/simple \
    && pip install -r /opt/runtime/data_platform/ops/requirements.txt -i https://mirrors.huaweicloud.com/repository/pypi/simple \
    && pip cache purge

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime