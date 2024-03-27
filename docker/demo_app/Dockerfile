# 使用 OpenJDK 作为基础镜像
FROM sofa_demo_app_base as build
WORKDIR /app
COPY ./kc-sofastack-demo/ .
COPY ./tree /usr/bin/tree

# print file content stock-mng/pom.xml
RUN cat /app/stock-mng/pom.xml

RUN mvn clean package
RUN tree /app

# Copy jar to java image
FROM openjdk:17-jdk
WORKDIR /app
RUN java -version


COPY --from=build /app/stock-mng/target/stock-mng-0.0.1-SNAPSHOT.jar /app/stock-mng-0.0.1-SNAPSHOT.jar
COPY --from=build /app/balance-mng/balance-mng-bootstrap/target/balance-mng-bootstrap-0.0.1-SNAPSHOT.jar /app/balance-mng-bootstrap-0.0.1-SNAPSHOT.jar
RUN ls

# hold
CMD java -jar /app/balance-mng-bootstrap-0.0.1-SNAPSHOT.jar
