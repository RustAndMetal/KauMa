FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --yes git build-essential libcjson-dev openjdk-17-jdk libbcprov-java libgoogle-gson-java libssl-dev gcc g++ libbotan-2-dev nlohmann-json3-dev python3 python3-pip rustc && rm -fr /var/cache/apt/* /var/lib/apt/lists/*
RUN pip3 install cryptography requests

WORKDIR /labwork
COPY . .
RUN ./build
ENTRYPOINT ["./kauma"]