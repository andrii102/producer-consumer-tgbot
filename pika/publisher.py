from PikaClient import MessageSender

# class BasicMessageSender(BasicPikaClient):

#     def declare_queue(self, queue_name):
#         print(f"Trying to declare queue({queue_name})...")
#         self.channel.queue_declare(queue=queue_name)

#     def send_message(self, exchange, routing_key, body):
#         channel = self.connection.channel()
#         channel.basic_publish(exchange=exchange,
#                               routing_key=routing_key,
#                               body=body)
#         print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

#     def close(self):
#         self.channel.close()
#         self.connection.close()

if __name__ == "__main__":

    # Initialize Basic Message Sender which creates a connection
    # and channel for sending messages.
    message_sender = MessageSender(
        "<broker-id>",
        "<username>",
        "<password>",
        "<region>"
    )

    # Declare a queue
    message_sender.declare_queue("rem_queue")

    # Send a message to the queue.
    message_sender.send_message(exchange="", routing_key="rem_queue", body=b'Hello World!')

    # Close connections.
    message_sender.close()