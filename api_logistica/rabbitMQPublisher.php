<?php

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

class RabbitMQPublisher
{
    public static function sendMessage(array $message): bool
    {
        try {
            $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
            $channel = $connection->channel();

            $channel->queue_declare('php_events', false, false, false, false);

            $msg = new AMQPMessage(json_encode($message));
            $channel->basic_publish($msg, '', 'php_events');

            $channel->close();
            $connection->close();

            return true;
        } catch (Exception $e) {
            error_log('RabbitMQ Error: ' . $e->getMessage());
            return false;
        }
    }
}
