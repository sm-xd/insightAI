# Frontend Application

React-based frontend for InsightAI with Tailwind CSS styling.

## Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   │   └── visualizations/  # Visualization components
│   ├── context/      # React context providers
│   ├── services/     # API services
│   └── pages/        # Page components
└── tailwind.config.js # Tailwind configuration
```

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Components

### Visualization Components
- FolderTree: Directory structure visualization
- DependencyGraph: Module dependency visualization
- Additional visualizations can be added in `visualizations/`

### Core Components
- InsightDisplay: Renders role-specific insights
- FileUpload: Handles codebase upload
- RoleSelector: Role selection interface

## API Integration

Services in `services/api.js`:
```javascript
// Upload codebase
uploadCodebase(file: File): Promise<Response>

// Clone repository
cloneRepository(repoUrl: string): Promise<Response>

// Get insights
getInsights(codebaseId: string, role: string): Promise<Response>
```

## Adding Visualizations

1. Create component in `visualizations/`
2. Register in `visualizations/index.js`
3. Update `InsightDisplay` to handle new type

Example:
```javascript
// visualizations/MyViz.jsx
export default function MyViz({ data, config }) {
  // Implement visualization
}

// visualizations/index.js
export { MyViz }
```

## Styling

- Uses Tailwind CSS for styling
- Custom styles in `index.css`
- Component-specific styles in component files

## Environment Variables

`.env` file:
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

## Build & Deploy

```bash
# Create production build
npm run build

# Test production build locally
npm run serve

# Deploy (example with surge)
surge build my-app.surge.sh
```

## Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## Browser Support

Tested and supported in:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)