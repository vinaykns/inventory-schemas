FROM fedora:31
MAINTAINER "Vinay Kapalavai" <vkapalav@redhat.com>

RUN yum -y install vim screen python3-pip python3-virtualenv jq git-core

RUN mkdir /home/inventory-schemas
COPY schemas /home/inventory-schemas/schemas
COPY samples /home/inventory-schemas/samples
COPY tools /home/inventory-schemas/tools
COPY README.md /home/inventory-schemas/README.md

RUN cd /home/inventory-schemas/; rm -rf tools/venv; bash tools/init.sh

STOPSIGNAL SIGRTMIN+3

CMD ["sleep", "infinity"]