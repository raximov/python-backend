# Authorization and DI

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

[[_TOC_]]

## Chapter I 

### Introduction

In this block, you will learn about Service Oriented Architecture, Microservice Architecture, authorization and authentication, RBAC and CBAC, JWT, gRPC, and DI.

## Chapter II

### Monolithic Architecture
A monolith is defined as an application as a unit. Traditionally, a monolithic solution is one executable on the server side and another on the client side.

A monolithic architecture is often a good option for a relatively small or simple application with a predictable load. For example, a minimum viable product (MVP) or a website that maintains static content.

The traditional approach to building applications by combining all functions into a single entity that combines the user interface and the server part is still relevant. The point is that it doesn't always make sense to complicate the architecture. If the requirements for a service (e.g., a website) include only speed, availability, and the ability to maintain static content that is freely available, then a monolithic architecture for such purposes is a natural choice. 

### SOA

SOA (**S**ervice-**O**riented **A**rchitecture) is a software development method that uses software components (called services) to create business applications. 

Each service provides business functionality, and services can communicate with each other by being written in different platforms and languages. When is this used? To reuse services in different systems or to combine independent services to perform complex tasks.

For example, many applications (even within the same company) require user authentication. Instead of rewriting the authentication code for each business process, you can create a single authentication service and reuse it for all applications.

Let's take a look at the main **benefits** of a service-oriented architecture.

1. *Reduced time to market*. If there are already existing services that can be reused, the development time of the system can be greatly reduced.
2. *Efficient maintenance*. With a well-developed infrastructure, maintaining a distributed system can be easier in some aspects. For example, it is possible to update services individually without shutting down the entire system. Also, services can be hosted on different machines, which also has certain advantages.
3. *Modularity*. Thanks to the separation of the system into services, it becomes easy to modify its parts.

<div align="center">

![soa](misc/images/soa.png)

</div>

So we realized that SOA is about great ideas: simplified service, faster time to market, etc. As is often the case, there is no single recipe for implementing a service-oriented architecture. However, there are a number of principles you can follow to get there.

1. *Standard Service Contract*. Each service has descriptive documents that define the functionality of the service and how it will be used.
2. *Loose coupling*. The fewer dependencies between services, the easier it is to modify them, because changes do not affect a large number of external components.
3. *Abstraction*. For customers or users, the service is a black box. They don't need to know how it works. They only get information about what it does through service contracts and other documents that describe the service.

Now let's see what a service-oriented architecture consists of.

<div align="center">

![details](misc/images/detalisation.svg)

</div>

- The service is the basic "building block" of SOA. Each service has an interface, an implementation and a contract.
    - The implementation is the service code.
    - Interface (Contract) means the way other services or systems interact with this service.

- The service provider creates, supports and provides one or more services that can be used by other users.

- The service consumer is the one who requests the provider to perform a particular service. The contract defines the rules by which the provider and consumer interact.

- The Service registry is a directory of available services.

And how does it all work? If services are more or less independent, how can they form a coherent system? Well, services can communicate with each other using established rules that define how data is transferred over the network. These rules are called data transfer protocols. For example, services can communicate using RESTful APIs, SOAP, RPC protocols.

### Microservice Architecture
MSA — **M**icro**s**ervice **A**rchitecture is an evolution of SOA. Microservices eliminate the drawbacks of SOA (e.g., limited scalability due to potential resource sharing) and make software more compatible with enterprise cloud environments.

Container technologies such as Docker and Kubernetes are often used to deploy MSA-based applications.

In a Microservices Architecture, an application is divided into a number of independently deployable services that interact through API interfaces. With this approach, each service can be deployed and scaled independently of the others. As a result, teams can deliver large, complex applications faster and more frequently. Unlike a monolithic application, a Microservices Architecture allows teams to introduce new features and changes more quickly without having to rewrite large chunks of existing code.

So what is the difference between MSA and SOA? You cannot say that MSA is always better than SOA. It is more accurate to say that each architecture serves a different purpose. Let's look at the differences between MSA and SOA in a table.

| MSA                                                                            | SOA                                                                                                                                   |
|--------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Microservices typically use lightweight protocols (REST/HTTP, etc.).              | SOA supports multi-protocols.                                                                                                   |
| Focuses on the division of tasks.                                              | Focuses on reuse.                                                                                           |
| Uses simple messaging systems.                                                 | Uses a service provider (also called an Enterprise Service Bus (ESB)) for communication.                   |
| Microservices use the " divide as little architecture as possible" approach.   | SOA uses a "share as much architecture as possible" approach (eliminating reuse, one of the basic principles of SOA). |
| Failures are well taken care of (microservices are almost independent).        | Errors and failures are poorly handled compared to MSA.                                                                               |
| Each microservice uses its own independent database.                           | Services in SOA share a single data repository.                                                                                      |
| Suitable for small web systems.                                                | Suitable for large, complex business applications.                                                                                      |

The line between SOA and MSA is very arbitrary and vague, so many of the things in the table can apply to both architectures.

An example of a Microservice Architecture ("Web API store") is shown in the figure below.

<div align="center">

![msa](misc/images/msa.svg)

</div>

### Advantages of Microservice Architecture
* Iterative development. A microservices-based software architecture lends itself well to an agile software development organization based on an iterative approach. By decomposing a running application into separate, loosely coupled services, new features and functionality can be tested and added without the risk of stopping the application.
* Flexibility. Microservices provide greater flexibility in the software development process at multiple levels at once. This allows different teams to work on different services at the same time, and makes it easier to bring new team members into the development process because code that is broken into separate functional pieces is easier to read and understand.
* Freedom to choose the technology stack. In a monolithic architecture where services are tightly coupled, it is important to maintain consistency in the technologies used in the application. They must also be compatible with each other, which is not the case with all programming languages and software development tools. Loosely coupled microservices offer much greater freedom in the choice of technology stack. To the point where a development team can even create separate services with a completely different set of development tools.
* Availability. One of the biggest benefits of a microservice architecture is that loosely coupled services provide greater application reliability and availability. If one service fails, the rest of the application typically continues to work for users.
* Scalability. Another advantage of microservices is that this approach is well suited for scaling applications. The modularity of microservices makes it easy to add new features directly to a running application. Although the initial cost of a microservices architecture is higher, it can be much cheaper to scale than a monolithic application due to a combination of the above benefits.
* Performance. You can also significantly improve performance by distributing services and loads across multiple servers.

### Disadvantages of Microservice Architecture
* Synchronization complexity. A distributed system, such as microservices, inevitably adds complexity because its parts must be synchronized to function as a single software system. And when services are distributed across servers, you need to prepare the infrastructure for microservices to work together.
* Higher upfront costs. While trying to scale a monolithic application significantly can be a nightmare, resulting in dramatically higher direct development costs, a Microservices Architecture requires higher upfront costs. Each microservice requires a dedicated development team (although one team may be responsible for multiple microservices). In addition, an automated testing and deployment (CI/CD) process must be established. All of this leads to higher upfront costs.
* The need for DevOps. A distributed system like microservices requires skilled orchestration, typically using Kubernetes and other DevOps tools and processes. This means you'll need to hire at least one DevOps engineer, which also increases costs.

### Authentication and authorization

Scary and very similar words. What do they mean? Let's look at the term *identification*.

**Identification** is a process that results in an identifier for an identification subject that uniquely identifies that subject in the information system. In simple terms, it is the process of determining *who* is making a request to the system. 

**Authentication** is the process of verifying the authenticity of a user by comparing the password he or she enters with the password stored in the database. Simply put, it is a check that the person making the request is not pretending to be someone else.

**Authorization** is the granting of rights to a specific person or group of people to perform specific actions. After successful identification and authorization, the user must be given the rights to do something in the system according to the chosen model of access to resources.

You deal with these procedures all the time. Let us take Sberbank Online as an example. First, you enter your username (or phone number), which the system uses to identify the account to which you are trying to log in. If the identification is successful, you proceed to the authentication procedure. You enter your password. If you successfully enter a password, the system may ask you to enter another code (for example, a code from an SMS) — this is called **two-factor authentication**. If it's successful, you move on to the authorization process: the system grants you access rights to information about your accounts, loans, bonuses, etc.

### Access control models

System security administration can be very expensive and inefficient, especially if you have to consider each new user individually and make individual decisions about their rights each time. In addition, this approach is prone to errors and information leakage. Thus, there is a clear need for an orderly control of user rights by means of proven access models.

In database theory, the following access models exist:

- MAC — Mandatory Access Control;
- DAC — Discretionary Access Control;
- RBAC — Role-Based Access Control;
- ABAC — Attribute-Based Access Control.

But since we are considering access to the *system*, only two models stand out — Role-Based Access Control and Claim-Based Access Control (RBAC and CBAC).

#### **RBAC**
User permissions are grouped into **roles**. And roles are assigned to **subjects**. So the difficulty of assigning permissions disappears: they are already logically grouped in some role. Examples of roles in the case of our store: salesman, consultant (for example, consultant may not have access to sales service methods), buyer, courier, etc.

A common mistake with RBAC is to group users and assign rights to them instead of *grouping access rights* into roles, which are then assigned to users. 

An advantage of RBAC is segregation of duties, which is often the reality of business.

A disadvantage of RBAC is the need to develop a detailed role model.

You can see an example in C# in the materials.

#### **CBAC**

"Claim" can mean many things, but for now we will use the term "assertion". What is an assertion? You can think of it as a kind of tag/label attached to a user. Examples: pensioner, European, administrator, etc. 

This approach is clearly broader than RBAC, because it is easy to reduce a requirements-based model to a role-based model by leaving only one assertion of type "role" and assigning it the values "consultant", "administrator", etc. The point is that we create a more flexible system by adding multiple assertions of different types.

Different languages have different tools for implementing these models.

You can see an example in C# in the materials.

### JWT tokens

It is well known that according to the REST methodology, the server does not need to know anything about the previous states of any client. The client sends a request to the server with all the necessary information at once.

Since the server does not store any data about the client's state, and almost every modern system uses authorization, you need some way to "signal" to the server that the client sending the request is already authorized. Yes, you could send a login and password each time in the request parameters, but this is extremely insecure. The solution is **JSON Web Token** (or **JWT**).

The idea of tokens isn't that complicated: let's store the user's token and id in the database instead of login and password, and give the token on the first request using a hash function of some unique user properties (id, login, password). That way, subsequent requests don't require a username and password, just a token. The token is often given a lifetime, after which it becomes invalid.

JWT has advantages: it is self-sufficient, all necessary information can be stored in the token itself. Let's have a look at the structure of a token.

#### Token Structure

The token consists of 3 main parts:

- Header,
- Payload,
- Signature.

The header and the payload are created separately, then the signature is created based on them.

The header consists of the fields "type" and "algorithm" (hash signature):
```
{
    "typ": "JWT",
    "alg": "HS256"
}
```
[Official website](jwt.io) offers only two hash algorithms: HS256 and RS256.

The payload is any data we want to keep inside the token. However, the standard provides several predefined fields: iss (issuer), sub (subject), exp (expiration time), iat (issued at), etc.

An example of payload:
```
{
    "iss": "Cool dev team",
    "sub": "auth",
    "my_attr_for_data": "I love ice cream!"
}
```

**Important!** The payload is not encrypted, so be careful.

Finally, the signature is created based on the header and the payload. 

First, the header and the payload are converted from JSON format to base64Url:

```
Header: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Payload: eyJpc3MiOiJDb29sIGRldiB0ZWFtIiwic3ViIjoiYXV0aCIsIm15X2F0dHJfZm9yX2RhdGEiOiJJIGxvdmUgaWNlIGNyZWFtISJ9
```

Then the strings are concatenated with a dot and hashed with the specified algorithm. Suppose the user's password is `qwerty123`. Then we get the signature with the following function:

```python
HS256('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' + '.' + 'eyJpc3MiOiJDb29sIGRldiB0ZWFtIiwic3ViIjoiYXV0aCIsIm15X2F0dHJfZm9yX2RhdGEiOiJJIGxvdmUgaWNlIGNyZWFtISJ9', 'qwerty123') = m-XiMqPrcoXQrORjJPjddx53DhB8lgAB-WGaA2iQGVs
```

The only thing left to do is to get the token itself, so we have to connect the header, payload and signature through a point:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJDb29sIGRldiB0ZWFtIiwic3ViIjoiYXV0aCIsIm15X2F0dHJfZm9yX2RhdGEiOiJJIGxvdmUgaWNlIGNyZWFtISJ9.m-XiMqPrcoXQrORjJPjddx53DhB8lgAB-WGaA2iQGVs
```
The received token can be tested [on the official website](https://jwt.io/).

Without knowing the private key (password) you cannot change the signature. If the signature is wrong, the data cannot be changed (the token is invalid because of the wrong signature). In this way, the data on the server is protected against changes.

You can do all of the above steps on your own. This is a good exercise to make sure that JWT doesn't work like magic, but in a fairly simple and straightforward way.

After the first login with password, the client returns the generated JWT. With each subsequent request, the client passes the JWT token it has already received to the API in the manner specified by the API (for example, via a header or request parameter). When the server receives the JWT, it decodes the header and payload (checking for reserved fields). Then it performs a signature (the server knows the user's secret key/password), and if it matches the signature from the token, the authorization is passed.

Of course, you can implement the above algorithm yourself. However, there are many libraries available for authorization using JWT. You can read more about them on the official [JWT](https://jwt.io/libraries) portal.

### gRPC

The REST methodology has become incredibly popular among developers. However, in recent years, another technology — gRPC — has been actively developed.

gRPC is a modern, high-performance open source platform that evolves the aging RPC (Remote Procedure Call) protocol.

The goal of RPC is to make remote procedure calls as similar as possible to local procedure calls. Interaction in RPC is based on the client-server model. The client and server do not interact with normal HTTP requests, but with remote procedure calls. The IDL (Interface Description Language) is used to specify the contract for the functions and data types to be called. You can see how RPC works in the image below.

<div align="center">

![rpc](misc/images/rpc.png)

</div>

gRPC copies this architectural style of client-server interaction through function calls. It turns out that gRPC is not a new concept, just an evolution of older technologies.

Let's take a look at why gRPC has become so popular in recent years.

1. The abstraction is simple: it uses function calls to make HTTP requests, which can be confusing when reading the code.
2. Supports many languages.
3. Good request execution speed (efficiency).

gRPC is also used in the Microservices Architecture you just read about. As you know, microservices can be written in different languages, and one microservice can call many other microservices. Using gRPC, we abstract away from the technology used in the microservices we want. It all boils down to a classic procedure call in the code.

<div align="center">

![rpc-1](misc/images/rpc-1.png)

</div>

A typical gRPC client application calls a local in-process function that implements a business operation. Internally, this local function (essentially a stub) calls another function on the remote computer. What appears to be a local call essentially becomes a transparent out-of-process call to a remote service. "Under the hood", RPC implements point-to-point network communication, serialization, and code execution on different machines.

This allows the application code to focus on business functions while gRPC handles the communication.

Again, it is impossible not to notice the performance of gRPC. If gRPC uses basically the same ideas as classic RPC, what makes it different? The answer: HTTP / 2, as well as one-way and two-way streaming, which allows gRPC to be used for streaming and event-driven data transfers in both directions.

In 2015, Google introduced support for HTTP/2 to replace the old HTTP/1.1 in the Chrome browser. With the traditional HTTP protocol, you can't send multiple requests or get multiple responses together in one connection. A new connection would have to be created for each of them. This type of request/response multiplexing is now possible in HTTP/2. It allows you to retrieve useful data from multiple requests with the same header, thus identifying them as a single request. 

It also solves the problem of huge headers in requests. HTTP/2 has a very interesting strategy to deal with this, called HPack. First, everything in HTTP / 2 is encrypted before it is sent, including the headers. This really helps with performance, but it's not the most important thing about header compression. HTTP / 2 displays the headers on both the client and server sides. Based on this, HTTP / 2 can determine if the header contains the same value, and only sends the header value if it is different from the previous header.

gRPC is a binary protocol that uses Google's protobuf protocol to serialize its frames.

#### Protobuf

Let's talk about Protobuf (Protocol Buffer), the most commonly used Interface Definition Language (IDL). This is where the basic data and functional contracts are stored as a proto file.

The contracts are described in files with the extension `.proto`. Based on the proto file, the `protoc` compiler generates both client and server code. The code includes:

- Typed objects shared by client and server.
- A typed base class that implements all the network communication, which you can later inherit and extend.
- A client stub that calls the necessary gRPC services to call a remote procedure.

At runtime, each message is serialized into a standard Protobuf representation and sent from the client to the server (or vice versa). Unlike JSON or XML, Protobuf messages are serialized into a binary byte sequence.

An example of what a proto file for [Hello, world!](https://github.com/grpc/grpc-go/tree/master/examples/helloworld) looks like using gRPC on Go is shown below.

```proto
// Copyright 2015 gRPC authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

syntax = "proto3";

option go_package = "google.golang.org/grpc/examples/helloworld/helloworld";
option java_multiple_files = true;
option java_package = "io.grpc.examples.helloworld";
option java_outer_classname = "HelloWorldProto";

package helloworld;

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

gRPC provides full support for most popular development stacks, including Java, JavaScript, C#, Go, Swift, and NodeJS.

This makes gRPC an interesting REST API replacement that you can use in your projects. You can take a further look at what metadata is, how streaming works, interceptors, and about load balancing in gRPC. It's a pretty interesting topic, and more importantly, it's evolving rapidly. 

### Dependency Injection, IoC Containers

Finally, let's talk about a very interesting pattern used in software component design — Dependency Injection (DI).

According to the Single Responsibility Principle (SRP), an object delegates the care of building the dependencies it needs to an external generic mechanism (Dependency Injector). The concept of DI containers or IoC containers is introduced, which store specific implementations of a given interface or base class and later "inject" them into class constructors.

<div align="center">

![di](misc/images/di-1.png)

</div>

Thus the code does not explicitly call the constructor of the class. The class into which the dependency is injected does not know anything about the injected implementation, it just uses the interface. This makes it easy to swap implementations of interfaces in a program.

<div align="center">

![di-1](misc/images/di-2.png)

</div>

This pattern is implemented in .NET out of the box in ASP.NET and in other languages or frameworks:
* Java Spring: the main packages of the Spring Framework IoC container are org.springframework.beans and org.springframework.context;
* GO: [Wire](https://github.com/google/wire) from Google and [Fx](https://github.com/uber-go/fx) from Uber (It uses [dig](https://github.com/uber-go/dig));
* Python: [opyoid](https://github.com/illuin-tech/opyoid) 

You can see an example in c# in the materials.

## Chapter III

1. If the Dependency injection pattern was not used in block 2, it must be used in this block. Implement injection implementations using interfaces through the IOC container.
2. It is necessary to implement an authorization service (a separate application) that will be used to authenticate and authorize users to the appliance store.
    
    * The authorization service must have its own storage (PostgreSQL). To do this, create a new database and inject a connection string into your service (not a new table, but a new database!).
    * The authorization service must communicate using the gRPC protocol only. Configure it as a gRPC server, describe the .proto file describing the methods provided.
    * The authorization service must provide the following methods:
         - Creating a user from input data (email, first name, last name, phone number, password) returns a signed token.
         - One of the most important principles of computer security must be respected: the system must not store the passwords of its users in plain text.Passwords in the database should be stored in hashed form with salt (an arbitrary concatenated string before hashing).Also, you cannot use outdated and vulnerable md5 and sha1 hashing algorithms. This way, even if your database falls into the hands of intruders, they won't know the real passwords used by your clients.
         - Verifying the username/password pair (authenticating the user) returns the token.
         - Changing the user password
         - Password recovery method: Send password to user's email (You don't need to implement sending the password to the email itself. Instead, implement a stub for sending to email in the form of password output to authorization service console).
3. Add a registration (/register), authorization (/auth), and password recovery (/reset) method to the appliance store. These methods are not authenticated, but only go to the authorization service to verify or create data.
4. Implement endpoint authorization of all APIs based on verification in the authentication service.To authenticate the user, you must go to the authentication service and confirm the validity of the token. If the token is valid, the method is available; if not, it returns 401.
    * Authorization in controller methods should be based on a self-written authorization attribute whose logic resides in the application's middleware. That is, you must authenticate the user before sending the request to the handler.
    * The JWT token must be passed in the Authorization header.

I.e. the authenticator (middleware) goes to the authorization service you wrote via gRPC and passes it to the handler if successful. 

**Important! ** Don't forget that gRPC runs on top of HTTP/2.

