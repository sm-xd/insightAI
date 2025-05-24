const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/count', (req, res) => {
  res.json({ count: Math.floor(Math.random() * 100) });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});