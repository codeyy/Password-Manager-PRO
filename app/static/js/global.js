//layout
  //globalvars
    globalThis.delList = []
    globalThis.search_data = []
  //end globalvars
  const glow = document.getElementById('glow');

  document.addEventListener('mousemove', (e) => {
    glow.style.top = e.clientY + 'px';
    glow.style.left = e.clientX + 'px';
  });
  const snowCount = 60; // Number of snowflakes
  for (let i = 0; i < snowCount; i++) {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = String.fromCharCode(Math.random() * 100); // Snowflake character
    snowflake.style.left = Math.random() * 100 + "vw";
    snowflake.style.zIndex = Math.floor(Math.random() - 1);
    snowflake.style.animationDuration = 10 + Math.random() * 10 + "s";
    snowflake.style.fontSize = 8 + Math.random() * 10 + "px";
    snowflake.style.animationDelay = Math.random() *10 + "s";
    snowflake.style.color = `rgba(0, ${Math.random() * 240}, 255, 0.9)`;
    snowflake.style.opacity = 0.6;
    snowflake.style.zIndex = 1;
    document.body.appendChild(snowflake);
  }
  for (let i = 0; i < snowCount; i++) {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = String.fromCharCode(Math.random() * 100); // Snowflake character
    snowflake.style.left = Math.random() * 100 + "vw";
    snowflake.style.zIndex = Math.floor(Math.random() - 1);
    snowflake.style.animationDuration = 10 + Math.random() * 10 + "s";
    snowflake.style.fontSize = 7 + Math.random() * 10 + "px";
    snowflake.style.animationDelay = Math.random() * 10 + "s";
    snowflake.style.color = `rgba(${Math.random() * 90}, 0, 255, 9)`;
    snowflake.style.opacity = 0.5;
    snowflake.style.zIndex = 1;
    document.body.appendChild(snowflake);
  }
  
  if (document.getElementById('indc')){
  setTimeout(function() {
  document.getElementById('indc').classList.add('fade-out');}, 3000)}