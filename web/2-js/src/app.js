const express = require('express');
const serialize = require('node-serialize');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

app.get('/', (req, res) => {
  const html = `
  <!DOCTYPE html>
  <html>
  <head>
      <title>🍪 Cookie 指挥官</title>
      <style>
          body { font-family: 'Courier New', monospace; background: #1a1a1a; color: #00ff00; padding: 20px; }
          .container { border: 2px solid #00ff00; padding: 20px; max-width: 800px; margin: auto; }
          h1 { text-align: center; text-shadow: 0 0 5px #00ff00; }
          .user-info { margin: 20px 0; padding: 15px; border: 1px dashed #00ff00; }
          .hint { color: #888; }
          #response { white-space: pre-wrap; background: #000; padding: 10px; display: none; }
      </style>
  </head>
  <body>
      <div class="container">
          <h1>🛸 USER PROFILE TERMINAL</h1>
          <div class="user-info">
              <p>> 当前用户: <span id="username">${getUsername(req)}</span></p>
              <p>> 权限等级: <span id="role">${isAdmin(req) ? '管理员' : '游客'}</span></p>
          </div>
          <div class="hint">
              <p>💡 提示: 尝试控制你的 Cookie 来提升权限！</p>
              <p>当前 Cookie: <code style="color:#fff">${req.cookies.user || '无'}</code></p>
          </div>
          <div id="response"></div>
      </div>
      <script>
          // 自动跳转到 /profile 触发反序列化逻辑
          window.onload = () => {
              fetch('/profile')
                .then(res => res.text())
                .then(data => {
                  document.getElementById('response').innerText = data;
                  document.getElementById('response').style.display = 'block';
                });
          }
      </script>
  </body>
  </html>
  `;
  res.send(html);
});

app.get('/profile', (req, res) => {
  if (req.cookies.user) {
    try {
      const userData = Buffer.from(req.cookies.user, 'base64').toString();
      const user = serialize.unserialize(userData);
      res.send(`Hello, ${user.username}!`);
    } catch (e) {
      res.send('Error: 非法用户数据!');
    }
  } else {
    const guestCookie = Buffer.from(serialize.serialize({ 
      username: 'guest',
      isAdmin: false 
    })).toString('base64');
    res.cookie('user', guestCookie, { httpOnly: true });
    res.redirect('/');
  }
});

function getUsername(req) {
  try {
    const userData = req.cookies.user ? 
      serialize.unserialize(Buffer.from(req.cookies.user, 'base64').toString()) : {};
    return userData.username || '未知用户';
  } catch {
    return '数据损坏';
  }
}

function isAdmin(req) {
  try {
    const userData = req.cookies.user ? 
      serialize.unserialize(Buffer.from(req.cookies.user, 'base64').toString()) : {};
    return userData.isAdmin === true;
  } catch {
    return false;
  }
}

app.listen(9000, () => console.log('Server running on http://localhost:9000'));

