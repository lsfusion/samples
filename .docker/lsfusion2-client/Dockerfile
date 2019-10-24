FROM openjdk:8

RUN set -eux; \
# enable https repository
    apt-get update; \
    apt-get install -y --no-install-recommends \
            apt-transport-https \
            ca-certificates \
            ; \
# install lsfusion2-client from the private repository
    wget --quiet -O - https://download.lsfusion.org/apt/GPG-KEY-lsfusion | apt-key add -; \
    echo deb https://download.lsfusion.org/apt all main > /etc/apt/sources.list.d/lsfusion.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            lsfusion2-client \
            ; \
# cleanup
    rm -rf /var/lib/apt/lists/*;

EXPOSE 8080

CMD /usr/share/lsfusion2-client/bin/catalina.sh run