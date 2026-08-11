# HighLoad and global integrations

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

[[_TOC_]]


## Chapter I

### **What is HighLoad?**
There is no specific definition for this term. Mostly it is used to mean:

1. **HighLoad as such**.
2. **Applications whose infrastructure is designed to handle HighLoad.**

There are also the following definitions:

- **HighLoad** — is when the IT system can no longer handle the current load.

- **HighLoad** — is when traditional approaches to IT infrastructure operations are no longer sufficient.

- **HighLoad** — is when a server can no longer handle the clients.

- **HighLoad** — is when the hardware cannot handle the increased load.

The highest load occurs due to:

 - Large number of concurrent users;
 - Large amounts of processing data;
 - Many complex calculations.

A "large number of requests" is a relative term. There is no hard and fast limit at which a project can be considered HighLoad: it depends on the infrastructure. Often, the HighLoad limit is set when the number of requests per second exceeds 100-1000. The same goes for the amount of data and calculations — it depends on the system requirements.

All of the above factors, both together and individually, characterize a HighLoad application. Such a system needs a lot of resources to run.

### **HighLoad systems characteristics**

HighLoad systems differ significantly from conventional systems for a number of reasons:

1. **Scalability**. A HighLoad system must be highly scalable because the load will increase over time. Additional processing power, disk space, and other resources will be required.

2. **Modularity**. When designing a HighLoad system, architects build it in modules. This approach ensures that any component can be replaced if it fails. Another option is to expand capabilities by adding new modules.

3. **Latency**. This parameter represents the minimum possible response time of the HighLoad system to a user request. The lower the value of this parameter, the faster the response time of the application.

4. **Uniqueness**. A HighLoad architecture is designed individually for each task, taking into account performance, load, and scalability requirements. There are no two HighLoad systems that are completely identical.

5. **Fault Tolerance**. Critical components of a HighLoad system are mandatorily duplicated. This approach ensures that if one component fails, it is automatically replaced by a duplicate component with no downtime.

Building HighLoad systems often requires careful design, a customized approach, and experience. 

We will go on to discuss the main ways to achieve this type of infrastructure.

### **What is scalability?**

Scalability refers to a desirable property of a system, network, or process that allows it to accommodate an increasing number of elements or objects, handle increasing loads efficiently, and have the ability to expand. In other words, the system is scalable if you don't have to redesign or duplicate it to maintain latency under heavy traffic loads.

There are two ways to scale the application: **Vertical** and **Horizontal**.

 **Vertical scaling** increases the power of individual system components to improve overall performance. This is done by replacing elements that can't handle the work with more powerful and faster ones. This is the simplest type of scaling and does not require any changes to the program.

Vertical scaling is often the simplest solution because it does not require code refactoring or complex configurations to optimize performance. With vertical scaling, you simply increase the available processing power of the system.

![vertical_scaling](misc/images/vertical_scaling.jpg)

Vertical scaling has its limitations, so many consider the following approach preferable for HighLoad systems. 

**Horizontal scaling** involves breaking the system into structural components that are distributed across multiple machines and increasing the number of servers that perform separate functions in parallel. It involves adding additional nodes to the system that work as a single unit and may require changes to the program to effectively use the increased number of resources.

![horizontal_scaling](misc/images/horizontal_scaling.jpg)

Horizontal scaling has far fewer physical and technological limitations. It is much easier to add more servers and more datacenters than it is to make a server extremely powerful. So the only practical limitation to horizontal scaling is the amount of resources you have available. Horizontal scaling also allows you to use dynamic scaling to efficiently handle changes in traffic. When traffic increases, more servers are connected to the network, and when traffic decreases, fewer servers are connected to the network to conserve resources.

### **Replication and Sharding** 

**Replication**

This term is related to horizontal scaling and means copying data between servers. When using this method, there are two types of servers: master and slave. The master is used to write or modify information, and the slaves are used to copy and read information from the master. Most often, one master and several slaves are used because there are usually more read requests than change requests. The main advantage of replication is the large number of copies of data. So even if the head server fails, any other server can take its place. However, as a scaling mechanism, replication is not very convenient. The reason for this is unsynchronization and delays in data transfer between servers. Most often, replication is used as a means to provide fault tolerance along with other scaling methods.

![replica](misc/images/replica.png)

**Sharding/Segmentation**

Sharding is horizontal data scaling, a database design principle that stores parts of a table separately on different physical servers. Sharding is the most appropriate solution for large-scale operations, especially when used in conjunction with replication. Unlike replication, sharding does not duplicate data, but instead separates it across different servers. This can help overcome technical limitations:

- If the database is operating at its performance limit, you can break it into pieces and distribute read requests among them.

- Accelerate data access for users in a specific region. For example, international social networks can store Russian-language content on servers closer to Russia.

- Meet regulatory requirements. For example, keep confidential data on a shard with public access disabled.

- Increase availability. If the database resides on an unsharded host, a failure of that host will result in the loss of all data. If the database is sharded, if one shard fails, all data remains available on other shards. You can also configure shard replication. This way you avoid loss if the server goes down. And by placing your shard replicas in different availability zones, you get a fault-tolerant system.

- Increase request speed. Requests can be slow because they are competing for server resources. Sharding eliminates the competition by running requests in parallel on different servers. 

As great as sharding is, it also has its drawbacks:

- There is manual sharding and automatic sharding. Manual sharding is when developers choose the principle of sharding and implement it themselves. And automated is when the DBMS can do it out of the box (e.g. MongoDb) and developers just have to turn it on and configure it.

- Sharding data correctly is not an easy task. If you do it wrong, the servers will be used irrationally (for example, a lot of cross-server requests will be required).

- The unbalanced distribution of data among the shards creates hotspots — parts of the database that are accessed much more frequently than others. Requests to hotspots are processed much more slowly. 

![replica](misc/images/sharding.png)

### **OAuth 2.0**

OAuth 2.0 is an authorization protocol that allows you to grant one service (application) the rights to access user resources on another service. The protocol eliminates the need to trust an application with a username and password and allows you to grant a limited set of rights, not all at once.

The OAuth 2.0 specification defines a delegation protocol that allows clients to securely access user resources on the provider service. This approach eliminates the need for the user to enter a password beyond the service provider: the entire process is reduced to pressing the "I agree to grant access to..." button. The idea is that with a well-protected account, a user can use it to authenticate to other services without revealing his or her password.

OAuth 2.0 scheme:

![replica](misc/images/oauth2.png)

1. The client requests permission from the resource owner.
2. The client receives permission.
3. The client requests an access token by authenticating to the authorization server and providing an authorization grant.
4. The authentication server authenticates the client by checking the authorization grant and, if valid, issues an access token and a refresh token.
5. The client requests a secure resource from the provider and authenticates itself by presenting an access token.
6. The provider verifies the access token and, if valid, serves the request.

So we see that the ultimate goal is to obtain access and update tokens. Next, the client communicates with the data provider until the access token expires. Then, to access the provider's data again, the client must use the refresh token and send a request to generate a new access/refresh token pair.

**Advantages and disadvantages of OAuth 2.0**

The benefits of the OAuth 2.0 protocol include the following:

- Resources are accessed via HTTP/HTTPS using the token specified in the headers. This allows you to use OAuth in almost any solution: mobile and desktop applications, websites, and even browser plugins.

- Ability to authorize the user.

- Popularity, i.e. most companies use it in their APIs.

- Ease of implementation and large amount of "literature".

- Out-of-the-box solutions that can be modified to suit your needs.

The drawbacks:

- There is no single established format, so you have to have a separate implementation for each service.

- When authenticating, you sometimes have to make additional requests to get even minimal information about the user. This is solved by using a JWT-token, but not all services support it.

- If the token is stolen, the intruder has access to the protected data for some time. A signed token can be used to minimize this possibility.

## Chapter II

1. It is necessary to take the functionality to work with images in a separate service.
     * Implement a simple sharding that will allow distributing the load on 4 machines. The service must have 4 strings of connection to different Postgres databases in the config (create them on one Postgres server for now), in which it should distribute the images evenly. Since the identifier of the photo is UUID, it is easy to ensure uniformity by analyzing the string representation of UUID. If UUID starts with 0-3, then write or search for UUID in the first base, if 4-7 — in the second, 8-b — in the third, c-f — respectively in the fourth.
     * Our Store API needs to access this service to get the correct image. (The implementation can be done via HTTP, gRPC, or message broker. You can choose your own approach), which will also do the sharding. 
2. Implement authorization in Store API OAuth using Google API. You can get username, email and other data needed to store user information.
     * According to the received data it is necessary to create a user in the local database, but there is no need to store credentials for him, for further authorization of the user we will delegate authentication to the OAuth service from Google.
     * Access to all methods except registration and authorization should be closed for public use as before, and the authorization you implemented before should remain.
     * Client_id and Client_secret must be environment variables.