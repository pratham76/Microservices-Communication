The microservice architecture is one of the most popular forms of deployment, especially in larger organizations where there are multiple components that can be loosely coupled together. Not only does this make it easier to work on separate components independently, but ensures that issues in one component do not bring down the rest of the service. A microservices architecture consists of a collection of small, autonomous services where each service is self-contained and should implement a single business capability within a bounded context. This also comes with the advantage that a single system can scale thereby limiting the resources to required components. For example, during a shopping sale, the cart and payment microservices might need more resources than the login microservice.

To execute the above project the ip address of the mongodb container should be added to the network section od docker compose file and use the command

docker-compose up --build

to stop the microprocess use

docker-compose down 
