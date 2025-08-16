# RecTool - Job Description Entry Tool

A responsive ReactJS application for entering and managing job descriptions with a modern, user-friendly interface.

## Features

- **Responsive Design**: Two-column layout on desktop, single-column stacked on mobile
- **Form Validation**: Real-time validation with error messages
- **Modern UI**: Clean, professional design using TailwindCSS
- **Toast Notifications**: Success and error feedback using react-hot-toast
- **API Integration**: POST requests to `/api/jd` endpoint
- **Input Validation**: Numeric fields accept only positive integers
- **Form Reset**: Automatic form reset after successful submission

## Layout Structure

### Header
- Page title: "Job Description Entry"
- Subtext explaining the purpose
- Help icon button (?) in top-right corner

### Main Content (Two-column layout)
**Left Column - JD Details Form**
- Basic Information section
  - JD Title (required)
  - Primary Skill (required)
  - Secondary Skills
  - Mode dropdown (Onsite/Remote/Hybrid, required)
  - Tenure in months (required)
  - Open Positions (required)
  - Available Positions
- Fitment Criteria section
  - Experience range (min/max)
  - Budget range (min/max)
  - JD Keywords

**Right Column - From Customer**
- Original JD section (large textarea)
- Notes section (Special Instructions)

### Footer
- Right-aligned SAVE button with loading state

## Technology Stack

- **React 18** with Hooks (useState, useEffect)
- **TailwindCSS** for styling
- **Axios** for HTTP requests
- **React Hot Toast** for notifications
- **Heroicons** for icons
- **Express.js** for mock API server

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RecTool
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development environment (React + API server)**
   ```bash
   npm run dev
   ```
   
   This will start both:
   - React development server on port 3000
   - Mock API server on port 3001

4. **Alternative: Run servers separately**
   ```bash
   # Terminal 1: Start API server
   npm run server
   
   # Terminal 2: Start React app
   npm start
   ```

5. **Build for production**
   ```bash
   npm run build
   ```

## API Endpoint

The application expects a POST endpoint at `/api/jd` that accepts the following JSON structure:

```json
{
  "jd_title": "Senior React Developer",
  "primary_skill": "ReactJS",
  "secondary_skills": "NodeJS, MySQL",
  "mode": "Hybrid",
  "tenure_months": 12,
  "open_positions": 5,
  "available_positions": 3,
  "experience_min": 3,
  "experience_max": 5,
  "budget_min": 60000,
  "budget_max": 90000,
  "jd_keywords": "React, JavaScript, Frontend",
  "original_jd": "Full job description text...",
  "special_instruction": "Candidate must join within 30 days."
}
```

### Mock API Server

The project includes a mock Express server (`server.js`) that:
- Runs on port 3001
- Provides the `/api/jd` endpoint
- Validates required fields
- Returns mock responses with 1-second delay
- Includes CORS support for development

## Form Validation

### Required Fields
- JD Title
- Primary Skill
- Mode
- Tenure in months
- Open Positions

### Validation Rules
- Numeric fields accept only positive integers
- Experience max must be greater than experience min
- Budget max must be greater than budget min
- Real-time error clearing on input

## Responsive Behavior

- **Desktop (lg+)**: Two-column grid layout
- **Mobile/Tablet**: Single-column stacked layout
- **Form fields**: Responsive grid for experience and budget ranges
- **Consistent spacing**: 12-16px vertical spacing between elements

## Styling

- **Colors**: Primary blue theme with gray accents
- **Borders**: Rounded corners (4-8px radius)
- **Shadows**: Subtle shadows for depth
- **Typography**: Clear hierarchy with 16-18px section headers
- **Focus states**: Blue ring focus indicators

## Development

### Project Structure
```
RecTool/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── JobDescriptionEntry.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── server.js
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

### Key Components
- `JobDescriptionEntry`: Main form component with all functionality
- `FormField`: Reusable form field component supporting different input types
- Form validation and submission logic
- Responsive layout management

### Available Scripts
- `npm start`: Start React development server
- `npm run server`: Start mock API server
- `npm run dev`: Start both servers concurrently
- `npm run build`: Build for production
- `npm test`: Run tests

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is licensed under the MIT License. 