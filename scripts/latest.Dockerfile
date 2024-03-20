FROM ubuntu:20.04 as python_base
#============= 安装python3.8 ============

#使用阿里云源
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update

#pypy下安装pillow需要，这个可以根据后续依赖的库，在这里添加
# RUN apt-get install -y zlib1g.dev libjpeg9-dev
# RUN apt-get install -y vim iputils-ping
RUN apt-get install -y python3.8 python3-pip python3.8-distutils python3.8-dev
RUN DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai apt-get -y install default-libmysqlclient-dev build-essential pkg-config
RUN apt-get clean

# #============= 支持中文 ==================
RUN apt-get install -y language-pack-zh-hans
RUN locale-gen zh_CN.UTF-8 && locale-gen en_US.UTF-8
ENV LC_ALL='zh_CN.UTF-8'
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip3 install virtualenv
# #========================================
#or https://pypi.mirrors.ustc.edu.cn/simple/

#============================================
#安装一个全局的pypy，后面是virtualenv安装即可
RUN mkdir -p /opt/apps
# 创建存放日志目录
RUN mkdir -p /opt/apps/logs
#==================== 直接下载方式====================
#考虑到下载速度，在外部先下载好，当然，如果网络够快的，直接下载也可以
#RUN curl -L -o pypy.tar.bz2 https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.3.1-linux64.tar.bz2
#RUN mkdir pypy
#RUN tar jxvf pypy.tar.bz2 -C pypy --strip-components=1
#==================== 外部下载方式 ===================
# ADD build/pypy.tar.bz2 .
# RUN mv pypy* pypy
# #===================================================
# RUN pypy/bin/pypy3 -m ensurepip
#===========================================

#=====================
#前面的这些步骤，可以作为任意一个使用python的docker镜像的基础
#=====================
#考虑到在多数情况下，requirements.txt很少变化，为了加快速度，可以放在前面，使用缓存

#=================extractor ===================
RUN mkdir -p /opt/apps/pipeline_model
RUN mkdir -p /opt/apps/pipeline_model/data
RUN mkdir -p /opt/apps/pipeline_model/data/logs
RUN mkdir -p /opt/apps/pipeline_model/data/pdfs

WORKDIR /opt/apps/pipeline_model
# COPY ./requirements.pypy.txt  ./requirements.pypy.txt
RUN virtualenv -p python3 python


COPY ./requirements.txt ./requirements.txt
COPY ./requirements.new.txt ./requirements.new.txt
COPY ./requirements.setup.txt ./requirements.setup.txt
COPY ./requirements.dev.txt ./requirements.dev.txt

RUN python/bin/pip install -r requirements.setup.txt --no-cache-dir
RUN python/bin/pip install -r requirements.new.txt --no-cache-dir

COPY ./main ./main
COPY ./setup.py ./setup.py
COPY ./version.py ./version.py

COPY ./themes ./themes
COPY ./conf ./conf
COPY ./model ./model

# RUN python/bin/pip wheel -w wheels --no-deps -e .
# RUN rm -r ./src

# # RUN python/bin/pip install -U ./wheels/memect_dag_server-3.1.4-py3-none-any.whl
# RUN python/bin/pip install memect_dag_server --no-index --find-link=wheels


COPY ./scripts/entrypointv4.sh ./scripts/entrypointv4.sh
RUN chmod +x ./scripts/entrypointv4.sh

#====
ENTRYPOINT ["./scripts/entrypointv4.sh"]
