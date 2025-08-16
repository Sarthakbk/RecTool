const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Mock API endpoint
app.post('/api/jd', (req, res) => {
  try {
    const jobData = req.body;
    
    // Validate required fields
    const requiredFields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions'];
    const missingFields = requiredFields.filter(field => !jobData[field]);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Missing required fields: ${missingFields.join(', ')}`
      });
    }
    
    // Simulate processing delay
    setTimeout(() => {
      console.log('Received Job Description:', JSON.stringify(jobData, null, 2));
      
      res.status(201).json({
        success: true,
        message: 'Job Description saved successfully',
        data: {
          id: Date.now(),
          ...jobData,
          created_at: new Date().toISOString()
        }
      });
    }, 1000);
    
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Mock API server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`API endpoint: http://localhost:${PORT}/api/jd`);
}); 