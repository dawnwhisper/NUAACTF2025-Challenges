from flask import Flask, request, render_template, render_template_string
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

TIMELOCK_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>时间裂隙锚定系统</title>
    <style>
        :root {
            --primary: #00ff88;
            --bg: #0a0a14;
            --surface: #1a1a2f;
            --border: rgba(0, 255, 136, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: var(--bg);
            color: #e0e7ff;
            font-family: 'Inter', system-ui, sans-serif;
            min-height: 100vh;
            display: grid;
            place-items: center;
            position: relative;
            overflow: hidden;
        }

        .matrix-effect {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            opacity: 0.1;
            z-index: 0;
        }

        .terminal {
            position: relative;
            background: var(--surface);
            width: min(90%, 500px);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 0 40px rgba(0, 255, 136, 0.1);
            z-index: 1;
        }

        .terminal::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: inherit;
            box-shadow: inset 0 0 20px rgba(0, 255, 136, 0.1);
            pointer-events: none;
        }

        h1 {
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 2rem;
            color: var(--primary);
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
        }

        .input-field {
            position: relative;
            margin-bottom: 2rem;
        }

        .input-field input {
            width: 100%;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .input-field input:focus {
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
            border-color: var(--primary);
        }

        .submit-btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #00ff88 0%, #00ccff 100%);
            border: none;
            border-radius: 6px;
            color: var(--bg);
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
            position: relative;
            overflow: hidden;
        }

        .submit-btn::after {
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(255, 255, 255, 0.1);
            opacity: 0;
            transition: opacity 0.2s ease;
        }

        .submit-btn:hover::after {
            opacity: 1;
        }

        .submit-btn:active {
            transform: scale(0.98);
        }

        #response {
            margin-top: 1.5rem;
            min-height: 2rem;
            text-align: center;
            font-family: 'Source Code Pro', monospace;
        }

        .alert {
            position: fixed;
            top: 1rem;
            right: -100%;
            background: var(--surface);
            padding: 1rem 2rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            transition: right 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
        }

        .alert.active {
            right: 1rem;
        }

        @media (max-width: 480px) {
            .terminal {
                padding: 1.5rem;
            }
            
            h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <canvas class="matrix-effect" id="matrix"></canvas>
    
    <div class="terminal">
        <h1>⏳ 时空锚点生成器 v2.0</h1>
        
        <form id="registerForm">
            <div class="input-field">
                <input 
                    type="text" 
                    name="username"
                    placeholder="输入量子签名 (a-z0-9_)"
                    pattern="[a-zA-Z0-9_]{3,20}"
                    required
                    autocomplete="off"
                >
            </div>
            <button type="submit" class="submit-btn">
                生成时空锚点
            </button>
        </form>
        
        <div id="response"></div>
    </div>

    <div class="alert" id="alert"></div>

    <script>
        // 矩阵背景动画
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = '01';
        const fontSize = 14;
        const columns = canvas.width/fontSize;
        const drops = [];
        
        for(let x = 0; x < columns; x++) drops[x] = 1;

        function drawMatrix() {
            ctx.fillStyle = 'rgba(10, 10, 20, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff88';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) 
                    drops[i] = 0;
                
                drops[i]++;
            }
        }

        setInterval(drawMatrix, 50);

        // 表单处理
        const form = document.getElementById('registerForm');
        const alertBox = document.getElementById('alert');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '⌛ 锚点生成中...';
            
            try {
                const formData = new FormData(form);
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.text();
                
                if (!response.ok) {
                    showAlert(result, 'error');
                } else {
                    showAlert('✅ 锚点生成成功', 'success');
                    document.getElementById('response').innerHTML = `
                        <div style="color: var(--primary)">
                            ${result.split('：')[1]}
                        </div>
                    `;
                    form.reset();
                }
            } catch (err) {
                showAlert('⚠️ 时间流异常：连接失败', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '生成时空锚点';
            }
        });

        function showAlert(message, type) {
            alertBox.textContent = message;
            alertBox.className = `alert ${type} active`;
            setTimeout(() => {
                alertBox.classList.remove('active');
            }, 3000);
        }
    </script>
</body>
</html>
'''

def sanitize_input(username):
    blacklist = ['config', 'os', 'system', 'eval', 'exec', 'import', 'request', 'subprocess', 'popen', 'globals']
    if any(re.search(rf'\b{word}\b', username, re.IGNORECASE) for word in blacklist):
        return None
    return username

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        sanitized = sanitize_input(username)
        if not sanitized:
            return "⚠️ 时间流扰动：检测到非法字符！", 400
        
        log = f"时空访客记录：{render_template_string(sanitized)}"
        with open("/tmp/timelock.log", "a") as f:
            f.write(log + "\n")
        
        return f"✅ 时空ID已生成：{os.urandom(8).hex()}"

    return render_template_string(TIMELOCK_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
