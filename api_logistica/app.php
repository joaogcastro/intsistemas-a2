<?php
require_once __DIR__ . '/vendor/autoload.php';
require_once 'rabbitMQPublisher.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

header('Content-Type: application/json');

if ($uri === '/equipments' && $method === 'GET') {
    echo json_encode([
        ['id' => 1, 'name' => 'Forklift'],
        ['id' => 2, 'name' => 'Crane'],
        ['id' => 3, 'name' => 'Conveyor Belt'],
    ]);
    exit;
}

if ($uri === '/dispatch' && $method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON']);
        exit;
    }

    $success = RabbitMQPublisher::sendMessage($input);
    if ($success) {
        echo json_encode(['status' => 'Message dispatched']);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to dispatch message']);
    }
    exit;
}

http_response_code(404);
echo json_encode(['error' => 'Not Found']);
