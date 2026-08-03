# Message Brokers and Distributed Cache

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

[[_TOC_]]

## Chapter I

### Message Brokers

A message broker is a type of architecture in which elements of the system "talk" to each other through an intermediary. It helps to relieve Web services because they don't have to send messages: it does all the work involved in this process.

We can say that in the work of any message broker two basic entities are used: producer (publisher of messages) and consumer (subscriber).

One entity creates messages and sends them to another consumer entity. The message broker can either store transmitted messages in its persistent storage (robust policy) or transmit them only through RAM without writing them to disk (fast policy).

There are several options:

* The message is sent directly from the sender to the receiver.

In this case, each message is used only once:
![scenario1](./misc/images/scenario1.png)

* Publication/subscription scheme.

In this messaging scheme, the sender does not know the recipients and simply posts to a specific topic. Consumers who are subscribed to this topic receive the message. Furthermore, it is possible to work with the distribution of tasks among subscribers on the basis of this system. I.e. the logic of work is built when messages for different consumers are published in the same topic. Everyone "sees" the unique token of his message and takes it for execution. The message can be delivered and processed either by all subscribers or only by the very first subscriber.

![scenario2](./misc/images/scenario2.png)

**What are message brokers for?**

* To organize communication between services, even if some of them are currently down. This means that the producer can send messages regardless of whether the consumer is currently active.

* Asynchronous task processing can increase the performance of the system as a whole.

* Ensure the reliability of message delivery: Brokers typically provide mechanisms for sending messages repeatedly at the same time or after a certain time. In addition, appropriate routing is provided for messages that are not delivered.

* Reduce the connectivity of system services.

**Disadvantages of Message Brokers**:

* The complexity of the overall system as another element is added. In addition, there is a dependence on the reliability of the distributed network, as well as the potential for problems due to the need for data consistency, as some elements of the system may have irrelevant data.

* The typically asynchronous operation of the entire system, as well as its distributed nature, can lead to errors that are difficult to resolve.

* Mastering such systems is not the easiest thing to do and can take a considerable amount of time.

The most popular message brokers are:
* RabbitMQ;
* Apache Kafka.
  
Speaking of RabbitMQ, we can say that it is a classic broker in which there are two entities described above — the producer (the system that generates messages about a variety of events) and the subscriber, who is the recipient of these messages.

Both entities interact with the message queue, which is a repository where the messages that are sent are collected.

The system is designed to support mutual notification of successful delivery on both sides: once the producer has sent the target message and it has been received, the system sends a notification of successful reception to the producer. In turn, the consumer sends a notification to the system when the message is successfully received. If the reception is not successful, an information message is sent and the message from the producer remains in the queue until it is received by the subscriber.

The main feature of this broker is the ability to set up flexible routing: when a message is sent, it does not necessarily have to take a straight path from the producer to the subscriber. It can pass through a number of intermediate exchange nodes, which can redirect it to different queues.

Within this broker, the information exchange is initiated by the producer, only he sends the message to the network, while the subscriber cannot request it himself (so-called "push delivery of messages").

Apache Kafka is a broker that, unlike RabbitMQ, stores all messages as a distributed log and ensures that the order of the messages reflects the order in which they arrive in the system. A message in this log is stored for a certain period of time, and the work is designed so that producers write new messages to the system and subscribers request them themselves. If necessary, the storage of messages is organized within topics. In other words, you could say that there is a certain kind of groups of messages within a topic.

If we try to justify the choice of one system or another, we should consider that RabbitMQ allows configuring even very complex message delivery scenarios, which gives developers the flexibility to build the desired event notification scenario. At the same time, it should be noted that the order of message delivery is not guaranteed.

In turn, the Apache Kafka broker is designed more for building high-load systems of bigdata, because its paradigm of parallel processing, replication allows you to create a fairly reliable system and provide unlimited scalability. The high throughput and the ability to retrieve messages from the queue over a period of time (because they are stored in the queue, as we said earlier, exactly in the order they were sent) are powerful tools for analyzing what is happening in a historical perspective.

### Server Sent Events (SSE)

SSE is a standard that describes ways to begin transferring data to clients from the moment the client first connects. The standard is widely used to send update messages or continuous data streams to the client browser. It is designed to enhance cross-browser streaming through a JavaScript API called EventSource, which allows the client to specify a URL to retrieve the event stream of interest.

```javascript
const evtSource = new EventSource("//api.example.com/...", { withCredentials: true } );
```

Once you have created an EventSource instance, you can begin receiving messages from the server by adding an OnMessage event handler:
```javascript
evtSource.onmessage = function(event) {
  const newElement = document.createElement("li");
  const eventList = document.getElementById('list');

  newElement.innerHTML = "message: " + event.data;
  eventList.appendChild(newElement);
}
```
This code takes incoming messages (i.e., notifications from the server that do not have an event field) and adds the message text to the list in the HTML document.

You can also handle events with addEventListener():

```javascript
evtSource.addEventListener("ping", function(event) {
  const newElement = document.createElement("li");
  const time = JSON.parse(event.data).time;

  newElement.innerHTML = "ping at " + time;
  eventList.appendChild(newElement);
});
```

This code is similar to the code above, except that it is automatically called whenever the server sends a message with the event field set to "ping"; it then parses JSON into the data field and outputs that information.

### WebSockets

The WebSocket specification defines an API for establishing a "socket-based" connection between a web browser and a server. Simply put, it is a persistent connection between a client and a server that they can use to send data to each other at any time.

The client establishes a connection by performing a process called the WebSocket handshake. This process begins when the client sends a standard HTTP request to the server. This request includes an upgrade header that tells the server that the client wants to establish a WebSocket connection.

Let's see what establishing such a connection looks like from the client side:

```javascript
// Creating a new WebSocket connection.
var socket = new WebSocket('ws://websocket.example.com');
```

The URL used for WebSocket connections uses the ws scheme. There is also a wss schema for secure WebSocket connections, which is the equivalent of HTTPS.

This shows the beginning of the process of opening a WebSocket connection to the websocket.example.com server.

It is important to understand that client disconnects must be handled correctly.

### Distributed Cache
A distributed cache is a cache shared by multiple application servers, usually maintained as an external service to the application servers that access it. A distributed cache can improve application performance and scalability, especially when the application is hosted by a cloud service or server farm.

A distributed cache has several advantages over other caching scenarios where cached data is stored on separate application servers.

With distributed caching, the data is:

* Is consistent across requests to multiple servers.
* Survives server restarts and application deployments.
* Doesn't use local memory.

**Redis Distributed Cache**

Redis is an open source, in-memory data store that is often used as a distributed cache.

## Chapter II

So let's get to the task:

1. You need to write a service that generates events about changes in product attributes (cost and remaining quantity).
    * The service is a worker that takes a random product and changes its field values on a timer. This is the generated timeout event.
2. Events should be sent to our application's gateway (API), which should update product information in the database, and update the same information for clients via WebSockets and SSE.
    * Implement simple echo clients (WebSockets and SSE) in JavaScript, which will receive updated information about the product and display it on the console.
3. Message delivery should take place in the gateway via a message broker (rabbitMq or Apache Kafka). 
4. The product images for responses should be cached in Redis.
