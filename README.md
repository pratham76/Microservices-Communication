The microservice architecture is one of the most popular forms of deployment, especially in larger organizations where there are multiple components that can be loosely coupled together. Not only does this make it easier to work on separate components independently, but ensures that issues in one component do not bring down the rest of the service. A microservices architecture consists of a collection of small, autonomous services where each service is self-contained and should implement a single business capability within a bounded context. This also comes with the advantage that a single system can scale thereby limiting the resources to required components. For example, during a shopping sale, the cart and payment microservices might need more resources than the login microservice.

This is a basic microservices implementaion using docker container where multiple microservices interact among them using rabbitmq,which is a message passing mechanism 

To execute the above project the ip address of the mongodb container should be added to the network section of docker compose file 

networks:
  default:
    ipam:
      config:
        - subnet: 172.18.0.0/16
          ip_range: 172.18.0.6/30

the above subnet and ip address should be changed according to your mongodb container's ip address which can be viewed using the following command
-> docker ps
-> get the container id of dongodb
-> docker inspect <container id>
-> here we can observe the ip address of the mongodb container use the same to update in the docker compose file


to build the project(provide u have docker installed and set up inyour system) use

docker-compose up --build

for healthcheck functionality: curl http://localhost:5000/health_check
for insert functionality: curl -X POST -d "Name=NAME&SRN=SRN&Section=SECTION" http://localhost:5000/insert_record
for display records functionality: curl http://localhost:5000/read_database
for delete functionality: curl http://localhost:5000/delete_record?SRN=SRN

alternatively to stop it use

docker-compose down 
