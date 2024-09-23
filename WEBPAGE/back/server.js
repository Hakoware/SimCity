const express = require('express');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware para servir archivos estáticos comprimidos
app.use(express.static(path.join(__dirname, 'public'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.gz')) {
      res.setHeader('Content-Encoding', 'gzip'); // Asegurar que se envíen los archivos gzip correctamente
    }
  }
}));

// Ruta principal para servir el juego Unity
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});
