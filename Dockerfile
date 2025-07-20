FROM openjdk:21-jdk-slim

ENV METABASE_VERSION=0.55.8

RUN apt-get update && apt-get install -y libstdc++6 libgcc1 curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

RUN curl -L -o metabase.jar https://downloads.metabase.com/v${METABASE_VERSION}/metabase.jar

EXPOSE 3000

CMD ["java", "-jar", "/app/metabase.jar"]
