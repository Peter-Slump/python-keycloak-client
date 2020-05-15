

docker run -d -p 8180:8080 $(pwd)/realms:/tmp --name kc -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=password jboss/keycloak:4.8.3.Final