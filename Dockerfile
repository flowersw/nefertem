FROM fedora:28
ENV LANG=en_US.UTF-8

RUN dnf update -y && \
    dnf install -y --setopt=tsflags=nodocs which python3-pip git && \
    dnf clean all && \
    pip3 install pipenv

COPY ./ /tmp/nefertem
RUN pushd /tmp/nefertem && \
    pipenv lock -r > requirements.txt && \
    pip3 install -r requirements.txt && \
    pip3 install . && \
    mkdir -p /tmp/nefertem-workdir && \
    chmod 777 /tmp/nefertem-workdir && \
    rm -rf /tmp/nefertem

# An arbitrary user.
USER 1042
WORKDIR /tmp/nefertem-workdir
ENTRYPOINT ["nefertem"]
CMD ["run-all"]
