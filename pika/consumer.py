from PikaClient import MessageReceiver

if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    message_receiver = MessageReceiver(
        "<broker-id>",
        "<username>",
        "<password>",
        "<region>"
    )

    # Consume the message that was sent.
    message_receiver.get_message("rem_queue")

    #Consume multiple messages in an event loop.
    #message_receiver.consume_messages("hello world queue")

    # Close connections.
    message_receiver.close()