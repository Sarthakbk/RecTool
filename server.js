const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: 'http://localhost:3000', // Change if frontend runs elsewhere
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type'],
}));
app.use(express.json());

// Mock data storage (in memory)
let jobDescriptions = [];

// GET endpoint to retrieve all job descriptions
app.get('/api/jd', (req, res) => {
  try {
    res.json({
      success: true,
      data: jobDescriptions,
      count: jobDescriptions.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to load job descriptions',
      error: error.message
    });
  }
});

// GET endpoint to retrieve a specific job description by ID
app.get('/api/jd/:id', (req, res) => {
  try {
    const { id } = req.params;
    const jobDescription = jobDescriptions.find(jd => jd.id == id);
    
    if (!jobDescription) {
      return res.status(404).json({
        success: false,
        message: 'Job description not found',
        data: null
      });
    }
    
    res.json({
      success: true,
      data: jobDescription
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to load job description',
      error: error.message
    });
  }
});

// Mock API endpoint
app.post('/api/jd', (req, res) => {
  try {
    const jobData = req.body;

    // Validate required fields
    const requiredFields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions'];
    const missingFields = requiredFields.filter(
      (field) => jobData[field] == null || jobData[field] === ""
    );

    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Missing required fields: ${missingFields.join(', ')}`,
        data: null,
      });
    }

    // Simulate processing delay
    setTimeout(() => {
      console.log('📥 Received Job Description:', JSON.stringify(jobData, null, 2));

      // Create new job description with ID
      const newJobDescription = {
        id: Date.now(),
        ...jobData,
        created_at: new Date().toISOString(),
      };

      // Store in mock data
      jobDescriptions.push(newJobDescription);

      res.status(201).json({
        success: true,
        message: 'Job Description saved successfully',
        data: newJobDescription,
      });
    }, 1000);

  } catch (error) {
    console.error('❌ Error processing job description:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error',
      data: null,
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('❌ Unhandled error:', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    data: null,
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
    data: null,
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📱 Health check: http://localhost:${PORT}/health`);
  console.log(`🔗 API endpoint: http://localhost:${PORT}/api/jd`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received, shutting down gracefully');
  process.exit(0);
});
