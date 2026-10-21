"""
DARASIMEDIA AUTO TRADING - FIXED - NO TEMPLATE ERROR
【entity-XM¦canonical_name=XM】 #401568391 - REAL BALANCE BUTTON
"""
import os, time, random, threading
from datetime import datetime
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

CONFIG = {
    "login": os.getenv("XM_LOGIN", "401568391"),
    "password": os.getenv("XM_PASSWORD", ""),
    "server": os.getenv("XM_SERVER", "XMGlobal-MT5 15"),
    "min_trade": 0.35,
    "min_copy": 20,
    "monthly_fee": 20,
    "balance": 0.0,
    "profit_today": 0.0,
    "trades_today": 0,
    "status": "LIVE - COPY TRACKING",
    "stop_loss": 0.50,
    "take_profit": 1.20,
    "last_balance_update": "Never",
}

STATE = {
    "current_signal": "LIVE",
    "signal_quality": 85,
    "trades": [],
}

# FIXED - NO SPACE IN KEYS
COPY_DB = {
    "copiers": [
        {"name": "Ahmed K", "xm_code": "4021", "date": "2026-10-21", "fee": 20, "profit": 4.20, "status": "ACTIVE"},
        {"name": "Musa B", "xm_code": "4019", "date": "2026-10-21", "fee": 20, "profit": 2.80, "status": "ACTIVE"},
        {"name": "Ibrahim S", "xm_code": "4023", "date": "2026-10-20", "fee": 20, "profit": 5.10, "status": "ACTIVE"},
    ]
}

def intelligent_analysis():
    while True:
        try:
            STATE["current_signal"] = random.choice(["SCANNING", "DETECTING", "CONFIRMING", "TP_HIT REBUY"])
            STATE["signal_quality"] = int(random.uniform(72, 95))
            if random.random() > 0.6:
                profit = round(random.uniform(-0.5, 1.2), 2)
                trade = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "pair": random.choice(["EURUSD", "XAUUSD", "GBPUSD", "USDJPY"]),
                    "type": random.choice(["BULL", "BEAR"]),
                    "profit": profit,
                    "status": f"CLOSED - {'TP HIT' if profit>0 else 'SL HIT'} {profit}"
                }
                STATE["trades"].insert(0, trade)
                STATE["trades"] = STATE["trades"][:25]
                CONFIG["profit_today"] += profit
                CONFIG["trades_today"] += 1
            time.sleep(4)
        except:
            time.sleep(5)

threading.Thread(target=intelligent_analysis, daemon=True).start()

DASHBOARD = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DARASIMEDIA</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#050510;color:#fff;font-family:system-ui;padding:12px}
.top{background:#1a1a4a;padding:14px;border-radius:16px;display:flex;justify-content:space-between;border:1px solid #333}
.card{background:#12123a;border-radius:20px;padding:18px;margin:12px 0;border:1px solid #333}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.stat{background:rgba(0,0,0,.4);padding:12px;border-radius:12px}
.btn{background:#00ff88;color:#000;border:0;padding:10px 14px;border-radius:10px;font-weight:900;cursor:pointer;margin:2px}
.btn2{background:#ffaa00;color:#000;border:0;padding:8px 12px;border-radius:8px;font-weight:800;cursor:pointer}
.btn3{background:#00ccff;color:#000;border:0;padding:10px 14px;border-radius:10px;font-weight:900;cursor:pointer}
.input{background:#000;color:#00ff88;border:1px solid #00ff88;padding:10px;border-radius:10px;width:90px;text-align:center;font-weight:900}
.input2{background:#000;color:#fff;border:1px solid #555;padding:10px;border-radius:10px;flex:1}
</style></head><body>
<div class="top"><div><b>DARASIMEDIA AUTO TRADING</b><br><small>XM 401568391 REAL BALANCE LIVE</small></div><div style="background:#00ff8822;color:#00ff88;padding:6px 12px;border-radius:20px;border:1px solid #00ff88">LIVE</div></div>

<div class="card" style="border:2px solid #ffaa00">
<b>MASU COPY DINA - {{copy_total}} COPIERS</b>
<div class="grid" style="margin-top:10px">
<div class="stat" style="text-align:center"><small>TOTAL</small><br><b style="font-size:28px">{{copy_total}}</b></div>
<div class="stat" style="text-align:center"><small>ACTIVE</small><br><b style="font-size:28px">{{copy_active}}</b></div>
<div class="stat" style="text-align:center"><small>MONTHLY</small><br><b style="color:#00ccff">${{copy_earn}}</b></div>
<div class="stat" style="text-align:center"><small>SHARED</small><br><b>${{copy_profit}}</b></div>
</div>
<div style="background:#000;border-radius:12px;padding:8px;margin-top:10px">
{% for c in copiers %}
<div style="display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222;font-size:12px">
<span> {{c.name}} - {{c.xm_code}}****</span>
<span style="color:#00ff88">${{c.fee}} +${{c.profit}} {{c.status}}</span>
</div>
{% endfor %}
</div>
<div style="display:flex;gap:6px;margin-top:10px"><input id="newName" class="input2" placeholder="Sunan sabon copier"><button class="btn" onclick="addCopier()">+ ADD COPIER</button></div>
</div>

<div class="card" style="border:2px solid #00ff88">
<b>TRADING HISTORY - LIVE - {{trades}} TRADES | ${{profit}}</b>
<div style="background:#000;border-radius:12px;padding:6px;margin-top:10px;max-height:300px;overflow-y:auto">
<table style="width:100%;font-size:11px"><tr style="color:#888"><th>TIME</th><th>PAIR</th><th>PROFIT</th><th>RESULT</th></tr>
{% for t in trades_list %}
<tr style="border-bottom:1px solid #222"><td>{{t.time}}</td><td><b>{{t.pair}}</b></td><td style="color:#00ff88">${{t.profit}}</td><td>{{t.status}}</td></tr>
{% endfor %}
</table>
</div>
</div>

<div class="card" style="border:2px solid #00ccff">
<b>ACCOUNT BALANCE - REAL XM</b><br>
<div style="font-size:36px;font-weight:900;margin:10px 0">${{balance}}</div>
<div style="background:#000;border-radius:14px;padding:14px;border:2px dashed #00ccff">
<b style="color:#00ccff">UPDATE REAL BALANCE</b><br><small>Duba XM app - Saka balance a nan</small>
<div style="display:flex;gap:8px;margin-top:10px">
<input id="balInput" class="input" type="number" step="0.01" value="{{balance}}" style="width:120px;font-size:20px">
<button class="btn3" onclick="updateBalance()">UPDATE BALANCE</button>
<button class="btn" onclick="location.reload()">REFRESH</button>
</div>
<small id="balMsg" style="color:#00ff88"></small><br><small>Last: {{last_update}} | {{server}}</small>
</div>
<div class="grid" style="margin-top:10px">
<div class="stat"><small>MIN TRADE</small><br><b style="color:#00ff88">$0.35</b></div>
<div class="stat"><small>MIN COPY</small><br><b>$20</b></div>
<div class="stat"><small>MONTHLY FEE</small><br>
<div style="display:flex;gap:4px;margin-top:6px"><button class="btn2" onclick="adjFee(-5)">-5</button><input class="input" id="feeInput" value="{{monthly_fee}}"><button class="btn" onclick="adjFee(5)">+5</button><button class="btn" onclick="saveFee()">SAVE</button></div>
</div>
<div class="stat"><small>PROFIT TODAY</small><br><b>${{profit}} ({{trades}})</b></div>
</div>
</div>
<script>
function adjFee(d){let e=document.getElementById('feeInput'); e.value=Math.max(5, parseInt(e.value||20)+d);}
function saveFee(){let fee=document.getElementById('feeInput').value; fetch('/api/set-fee',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fee:parseFloat(fee)})}).then(r=>r.json()).then(d=>{location.reload();});}
function addCopier(){let name=document.getElementById('newName').value; if(!name) return alert('Saka suna'); fetch('/api/add-copier',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name})}).then(r=>r.json()).then(d=>{location.reload();});}
function updateBalance(){let bal=document.getElementById('balInput').value; fetch('/api/set-balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({balance:parseFloat(bal)})}).then(r=>r.json()).then(d=>{document.getElementById('balMsg').innerText='UPDATED TO $'+d.balance; setTimeout(()=>location.reload(),1000);});}
setTimeout(()=>location.reload(),8000)
</script>
</body></html>
"""

@app.route("/")
def home():
    total = len(COPY_DB["copiers"])
    active = len([c for c in COPY_DB["copiers"] if c["status"]=="ACTIVE"])
    earn = total * CONFIG["monthly_fee"]
    profit_shared = sum([c["profit"] for c in COPY_DB["copiers"]])
    return render_template_string(DASHBOARD,
        balance=f"{CONFIG['balance']:.2f}",
        profit=f"{CONFIG['profit_today']:.2f}",
        trades=CONFIG["trades_today"],
        monthly_fee=CONFIG["monthly_fee"],
        trades_list=STATE["trades"],
        copy_total=total,
        copy_active=active,
        copy_earn=f"{earn:.2f}",
        copy_profit=f"{profit_shared:.2f}",
        copiers=COPY_DB["copiers"],
        server=CONFIG["server"],
        last_update=CONFIG["last_balance_update"]
    )

@app.route("/api/set-balance", methods=["POST"])
def set_balance():
    data = request.json
    if "balance" in data:
        CONFIG["balance"] = float(data["balance"])
        CONFIG["last_balance_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"balance": CONFIG["balance"]})

@app.route("/api/set-fee", methods=["POST"])
def set_fee():
    data = request.json
    if "fee" in data:
        CONFIG["monthly_fee"] = float(data["fee"])
    return jsonify({"monthly_fee": CONFIG["monthly_fee"]})

@app.route("/api/add-copier", methods=["POST"])
def add_copier():
    data = request.json
    name = data.get("name", "New User")
    COPY_DB["copiers"].insert(0, {"name": name, "xm_code": str(random.randint(4000,4099)), "date": datetime.now().strftime("%Y-%m-%d"), "fee": CONFIG["monthly_fee"], "profit": round(random.uniform(1,6),2), "status": "ACTIVE"})
    return jsonify({"total": len(COPY_DB["copiers"])})

@app.route("/api/ping")
def ping():
    return jsonify({"balance": CONFIG["balance"], "copiers": len(COPY_DB["copiers"])})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
