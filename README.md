# 🗑️ Trash Recognition API

A Flask API that uses Claude Vision to detect trash in photos.  
Deploy for free on Render, then call it from your game HTML.

---

## 🚀 Deploy on Render (Free)

### Step 1 — Upload to GitHub
1. Create a new GitHub repository (e.g. `trash-api`)
2. Upload all 4 files: `app.py`, `requirements.txt`, `render.yaml`, `README.md`

### Step 2 — Create a Render account
1. Go to **https://render.com** and sign up (free)
2. Connect your GitHub account

### Step 3 — Create a new Web Service
1. Click **"New +"** → **"Web Service"**
2. Choose your `trash-api` GitHub repo
3. Render will auto-detect the `render.yaml` settings
4. Click **"Create Web Service"**

### Step 4 — Add your API key
1. In Render dashboard → your service → **"Environment"** tab
2. Add:
   - Key: `ANTHROPIC_API_KEY`
   - Value: your Anthropic API key (from https://console.anthropic.com)
3. Click **"Save Changes"** → service will redeploy

### Step 5 — Get your API URL
After deploy, your URL will look like:
```
https://trash-recognition-api.onrender.com
```

---

## 📡 Update Your Game HTML

Find the `showTrashConfirm` function in your game and replace it with:

```javascript
// Replace YOUR_RENDER_URL with your actual Render URL
var TRASH_API_URL = 'https://YOUR_RENDER_URL.onrender.com/recognize';

function handleTrashPhoto(event){
  var file = event.target.files[0];
  event.target.value = '';
  if(!file) return;

  var reader = new FileReader();
  reader.onload = function(e){
    var dataUrl = e.target.result;
    var b64 = dataUrl.split(',')[1];

    // Show loading modal
    showModal('🔍 AI 辨識中...', 
      '<div style="text-align:center;padding:28px 0">' +
      '<div style="font-size:56px">🤖</div>' +
      '<div style="font-size:15px;font-weight:900;margin:14px 0">AI 正在分析照片...</div>' +
      '</div>'
    );

    fetch(TRASH_API_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ image: b64, mime_type: file.type || 'image/jpeg' })
    })
    .then(function(r){ return r.json(); })
    .then(function(result){
      if(result.error){ throw new Error(result.error); }
      showPhotoResult(result, dataUrl);
    })
    .catch(function(err){
      showModal('❌ 辨識失敗', 
        '<div style="text-align:center;padding:20px">' +
        '<div style="font-size:13px;font-family:Noto Sans TC">' + err.message + '</div>' +
        '<button class="sticker-btn ghost" onclick="closeModal()">關閉</button>' +
        '</div>'
      );
    });
  };
  reader.readAsDataURL(file);
}

function showPhotoResult(result, dataUrl){
  if(!result.is_trash){
    showModal('🔍 辨識結果',
      '<div style="text-align:center;padding:16px 0">' +
      '<img src="' + dataUrl + '" style="max-width:100%;max-height:160px;border-radius:10px;border:2px solid var(--ink);margin-bottom:12px">' +
      '<div style="font-size:18px;font-weight:900;margin:8px 0">這不是垃圾！</div>' +
      '<button class="sticker-btn ghost" onclick="closeModal()">關閉</button>' +
      '</div>'
    );
    return;
  }
  incPhotoDailyCount();
  totalMoney += 100; catCoins += 15;
  questProgress.trash = (questProgress.trash||0) + 1;
  writeSave(); refreshHomeUI();
  showModal('🎉 偵測到垃圾！',
    '<div style="text-align:center;padding:6px 0">' +
    '<img src="' + dataUrl + '" style="max-width:100%;max-height:140px;border-radius:10px;border:2px solid var(--ink);margin-bottom:10px">' +
    '<div style="font-size:18px;font-weight:900;color:var(--coral)">辨識到：' + (result.trash_type||'垃圾') + '</div>' +
    '<div style="display:flex;gap:10px;justify-content:center;margin:12px 0">' +
    '<div style="background:var(--gold);border:3px solid var(--ink);border-radius:12px;padding:8px 18px;font-weight:900;font-size:20px;box-shadow:3px 3px 0 var(--ink)">💰 +100</div>' +
    '<div style="background:var(--lavender);border:3px solid var(--ink);border-radius:12px;padding:8px 18px;font-weight:900;font-size:20px;box-shadow:3px 3px 0 var(--ink)">🪙 +15</div>' +
    '</div>' +
    (result.eco_tip ? '<div style="background:#f0ffe8;border:2px solid rgba(26,16,8,.15);border-radius:10px;padding:9px;font-size:11px;font-family:Noto Sans TC;text-align:left;margin-bottom:10px">💡 ' + result.eco_tip + '</div>' : '') +
    '<button class="sticker-btn mint" onclick="closeModal()" style="font-size:15px;padding:11px 28px">✅ 收下獎勵！</button>' +
    '</div>'
  );
}
```

---

## 🧪 Test Your API

After deployment, test it in your browser:
```
https://YOUR_RENDER_URL.onrender.com/
```
Should return: `{"message": "Trash Recognition API is running!", "status": "ok"}`

---

## 📁 File Structure
```
trash-api/
├── app.py           ← Main Flask server
├── requirements.txt ← Python dependencies
├── render.yaml      ← Render deployment config
└── README.md        ← This file
```
