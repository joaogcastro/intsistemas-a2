const express = require('express');
const axios = require('axios');
const redis = require('redis');

/////////////////////////////////////////////////
// Constants
/////////////////////////////////////////////////

const data = {
    temperature: (20 + Math.random() * 10).toFixed(2),
    pressure: (1000 + Math.random() * 50).toFixed(2),
    timestamp: new Date().toISOString()
};

const pythonApiUrl = 'http://localhost:5000/event';

/////////////////////////////////////////////////
// Redis
/////////////////////////////////////////////////

const redisClient = redis.createClient();

redisClient.on('error', (err) => {
  console.error('Redis error:', err);
});

async function connectRedis() {
  try {
    await redisClient.connect();
    console.log('Connected to Redis');
  } catch (error) {
    console.error('Failed to connect to Redis:', error);
    connectRedis();
  }
}

/////////////////////////////////////////////////
// Express
/////////////////////////////////////////////////

const app = express();
app.use(express.json());

app.get('/sensor-data', async (req, res) => {
    const cacheKey = 'sensor:data';

    try {
        const cached = await redisClient.get(cacheKey);
        if (cached) {
            console.log('Cached response');
            return res.json(JSON.parse(cached));
        }
        console.log('Fetching new data');
        // Cache for 60 seconds
        await redisClient.setEx(cacheKey, 60, JSON.stringify(data));
        res.json(data);
    } catch (error) {
        console.error('Error fetching sensor data:', error);
        res.status(500).json({ error: 'Failed to get sensor data' });
    }
});

app.post('/alert', async (req, res) => {
  try {
    const response = await axios.post(pythonApiUrl, req.body);
    res.json({ status: 'Alert sent', response: response.data });
  } catch (error) {
    console.error('Error sending alert:', error);
    res.status(500).json({ error: 'Failed to send alert to Python API' });
  }
});

async function init() {
    await connectRedis();
    app.listen(3000, () => {
        console.log(`Server running on http://localhost:3000`);
    });
}

init();
