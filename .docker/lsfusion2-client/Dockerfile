FROM openjdk:8

COPY lsfusion.list /etc/apt/sources.list.d/
ADD  https://download.lsfusion.org/apt/GPG-KEY-lsfusion /tmp/

#RUN apt-key add /tmp/GPG-KEY-lsfusion \
#    && rm /tmp/GPG-KEY-lsfusion
#    && apt-get update \
#    && apt-get install -y --no-install-recommends lsfusion2-client

EXPOSE 80