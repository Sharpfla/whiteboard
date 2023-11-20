document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let lines = [];
    let selectedLine = null;
    let offsetX, offsetY;
  
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
  
    function startDrawing(e) {
      const mouseX = e.clientX - canvas.getBoundingClientRect().left;
      const mouseY = e.clientY - canvas.getBoundingClientRect().top;
  
      selectedLine = getSelectedLine(mouseX, mouseY);
  
      if (!selectedLine) {
        // If no line is selected, start a new line
        selectedLine = { x1: mouseX, y1: mouseY, x2: mouseX, y2: mouseY };
        lines.push(selectedLine);
      }
  
      offsetX = mouseX - selectedLine.x1;
      offsetY = mouseY - selectedLine.y1;
  
      isDrawing = true;
    }
  
    function draw(e) {
      if (!isDrawing || !selectedLine) return;
  
      const mouseX = e.clientX - canvas.getBoundingClientRect().left;
      const mouseY = e.clientY - canvas.getBoundingClientRect().top;
  
      selectedLine.x2 = mouseX - offsetX;
      selectedLine.y2 = mouseY - offsetY;
  
      // Clear the canvas and redraw all lines
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const line of lines) {
        drawLine(line);
      }
    }
  
    function stopDrawing() {
      isDrawing = false;
    }
  
    function drawLine(line) {
      ctx.beginPath();
      ctx.moveTo(line.x1, line.y1);
      ctx.lineTo(line.x2, line.y2);
      ctx.stroke();
    }
  
    function getSelectedLine(x, y) {
      for (const line of lines) {
        if (isPointOnLine(x, y, line)) {
          return line;
        }
      }
      return null;
    }
  
    function isPointOnLine(x, y, line) {
      const d1 = distance(x, y, line.x1, line.y1);
      const d2 = distance(x, y, line.x2, line.y2);
      const lineLength = distance(line.x1, line.y1, line.x2, line.y2);
  
      // Allow some tolerance (e.g., 5 pixels) for user interaction
      return d1 + d2 >= lineLength - 5 && d1 + d2 <= lineLength + 5;
    }
  
    function distance(x1, y1, x2, y2) {
      return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
    }
  });
   // not sure