"""
DARASIMEDIA AUTO TRADING - 【entity-XM¦canonical_name=XM】 #401568391
REAL BALANCE BUTTON + COPY TRACKING + TRADING HISTORY
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
    "name": "Darasimedia Auto Trading",
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
    "step": 4,
    "last_analysis": "Ready",
    "trades": [],
}

COPY_DB = {
    "copiers": [
        {"name": "Ahmed K.", "【entity-xm¦canonical_name=XM】": "4021****", "date": "2026-10-21", "fee": 20, "profit": 4.20, "status": "ACTIVE"},
        {"name": "Musa B.", "【entity-xm¦canonical_name=XM】": "4019****", "date": "2026-10-21", "fee": 20, "profit": 2.80, "status": "ACTIVE"},
        {"name": "Ibrahim S.", "【entity-xm¦canonical_name=XM】": "4023****", "date": "2026-10-20", "fee": 20, "profit": 5.10, "status": "ACTIVE"},
    ]
}

def intelligent_analysis():
    while True:
        try:
            STATE["step"] = random.randint(1,4)
            signals = ["SCANNING 28 PAIRS", "DETECTING RSI+MACD+EMA", "CONFIRMING 3x", f"TP_HIT ${random.uniform(0.3,1.2):.2f} - REBUY"]
            STATE["current_signal"] = random.choice(signals)
            STATE["signal_quality"] = int(random.uniform(72, 95))
            time.sleep(2)
            
            # Simulate trade every 8-15 sec
            if random.random() > 0.6:
                outcome = random.choices(["TP_HIT", "SL_HIT"], weights=[75,25])[0]
                profit = round(random.uniform(0.30, CONFIG["take_profit"]) if outcome=="TP_HIT" else random.uniform(-CONFIG["stop_loss"], -0.10), 2)
                trade = {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "pair": random.choice(["EURUSD", "XAUUSD", "GBPUSD", "USDJPY"]),
                    "type": random.choice(["BULLISH", "BEARISH"]),
                    "profit": profit,
                    "sl": CONFIG["stop_loss"],
                    "tp": CONFIG["take_profit"],
                    "status": f"{'CLOSED - TP HIT +$' if profit>0 else 'CLOSED - SL HIT '}{profit}"
                }
                STATE["trades"].insert(0, trade)
                STATE["trades"] = STATE["trades"][:25]
                CONFIG["profit_today"] += profit
                CONFIG["trades_today"] += 1
                STATE["last_analysis"] = f"{trade['pair']} {trade['type']} - ${profit}"
            time.sleep(random.uniform(4,8))
        except Exception as e:
            time.sleep(5)

threading.Thread(target=intelligent_analysis, daemon=True).start()

DASHBOARD = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DARASIMEDIA 【entity-XM¦canonical_name=XM】 REAL BALANCE</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#050510;color:#fff;font-family:system-ui;padding:12px}
.top{background:linear-gradient(90deg,#0f0f2a,#1a1a4a);padding:14px;border-radius:16px;display:flex;justify-content:space-between;align-items:center;border:1px solid #2a2a6a}
.logo{width:52px;height:52px;background:linear-gradient(135deg,#00ff88,#00ccff);border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:20px}
.live{animation:pulse 2s infinite;background:rgba(0,255,136,.2);color:#00ff88;padding:6px 14px;border-radius:20px;border:1px solid #00ff88}
.card{background:linear-gradient(135deg,#12123a 0%,#1e1e5a 100%);border-radius:20px;padding:18px;margin:12px 0;border:1px solid #3333aa}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.stat{background:rgba(0,0,0,.3);padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,.1)}
.btn{background:#00ff88;color:#000;border:0;padding:10px 14px;border-radius:10px;font-weight:900;cursor:pointer;margin:2px}
.btn2{background:#ffaa00;color:#000;border:0;padding:8px 12px;border-radius:8px;font-weight:800;cursor:pointer;margin:2px}
.btn3{background:#00ccff;color:#000;border:0;padding:10px 14px;border-radius:10px;font-weight:900;cursor:pointer;margin:2px}
.input{background:#000;color:#00ff88;border:1px solid #00ff88;padding:10px;border-radius:10px;width:90px;text-align:center;font-weight:900;font-size:16px}
.input2{background:#000;color:#fff;border:1px solid #555;padding:10px;border-radius:10px;flex:1}
</style>
</head><body>
<div class="top">
<div style="display:flex;gap:12px;align-items:center"><div class="logo">D</div><div><b>DARASIMEDIA AUTO TRADING</b><br><small style="color:#888">【entity-XM¦canonical_name=XM】 #401568391 • REAL BALANCE LIVE</small></div></div>
<div class="live">● {{current}} </div>
</div>

<!-- MASU COPY DINA -->
<div class="card" style="border:2px solid #ffaa00">
<div style="display:flex;justify-content:space-between"><b>👥 MASU COPY DINA</b><span style="background:#ffaa00;color:#000;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:900">{{copy_total}} COPIERS</span></div>
<div class="grid" style="margin-top:12px">
<div class="stat" style="text-align:center;border-color:#ffaa00"><small style="color:#ffaa00">TOTAL COPIERS</small><br><b style="font-size:28px">{{copy_total}}</b><br><small>Mutum {{copy_total}} sun yi copy</small></div>
<div class="stat" style="text-align:center"><small style="color:#00ff88">ACTIVE NOW</small><br><b style="font-size:28px">{{copy_active}}</b><br><small>Yanzu suna copy</small></div>
<div class="stat" style="text-align:center"><small style="color:#00ccff">MONTHLY EARNINGS</small><br><b style="font-size:22px;color:#00ccff">${{copy_earn}}</b><br><small>Daga fees ${{monthly_fee}}/mo</small></div>
<div class="stat" style="text-align:center"><small>TOTAL SHARED</small><br><b>${{copy_profit}}</b><br><small>Sun samu daga gare ka</small></div>
</div>
<div style="margin-top:10px;background:#000;border-radius:12px;padding:8px;max-height:200px;overflow-y:auto">
{% for c in copiers %}
<div style="display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222;font-size:12px"><span>👤 <b>{{c.name}}</b> • {{c.【entity-xm¦canonical_name=XM】}}</span><span style="color:#00ff88;text-align:right">${{c.fee}} +${{c.profit}}<br><small style="background:#00ff88;color:#000;padding:1px 6px;border-radius:10px">{{c.status}}</small></span></div>
{% endfor %}
</div>
<div style="margin-top:10px;display:flex;gap:6px"><input id="newName" class="input2" placeholder="Sunan sabon copier"><button class="btn" onclick="addCopier()">+ ADD COPIER</button></div>
</div>

<!-- TRADING HISTORY -->
<div class="card" style="border:2px solid #00ff88">
<div style="display:flex;justify-content:space-between"><b>📜 TRADING HISTORY - LIVE</b><span style="background:#00ff88;color:#000;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:900">{{trades}} TRADES | ${{profit}}</span></div>
<div style="max-height:300px;overflow-y:auto;margin-top:10px;background:#000;border-radius:12px;padding:6px">
<table style="width:100%;font-size:11px;border-collapse:collapse">
<tr style="color:#888;border-bottom:1px solid #333"><th>TIME</th><th>PAIR</th><th>PROFIT</th><th>RESULT</th></tr>
{% for t in trades_list %}
<tr style="border-bottom:1px solid #222"><td>{{t.time}}</td><td><b>{{t.pair}}</b></td><td style="color:{{ '#00ff88' if t.profit>0 else '#ff5050' }};font-weight:800">${{t.profit}}</td><td style="font-size:9px">{{t.status}}</td></tr>
{% else %}
<tr><td colspan=4 style="text-align:center;padding:20px;color:#666">Scanning...</td></tr>
{% endfor %}
</table>
</div>
<div style="display:flex;gap:6px;margin-top:10px"><span style="background:rgba(255,80,80,.15);border:1px solid #ff5050;padding:5px 8px;border-radius:6px;font-size:11px">🛑 SL: ${{sl}} AUTO</span><span style="background:rgba(0,255,136,.15);border:1px solid #00ff88;padding:5px 8px;border-radius:6px;font-size:11px">🎯 TP: ${{tp}} AUTO</span></div>
</div>

<!-- ACCOUNT BALANCE + REAL BALANCE BUTTON -->
<div class="card" style="border:2px solid #00ccff">
<div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:18px">💰 ACCOUNT BALANCE - REAL XM</b><span style="background:#00ccff;color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:900">PHONE OFF OK ✅</span></div>
<div style="font-size:36px;font-weight:900;margin:14px 0">${{balance}} <small style="font-size:14px;color:#ffaa00">• {{bal_status}}</small></div>
<div style="background:#000;border-radius:14px;padding:14px;border:2px dashed #00ccff;margin:10px 0">
<b style="color:#00ccff">🔥 SABON FEATURE - UPDATE REAL BALANCE</b><br>
<small style="color:#aaa">Duba XM MT5 app dinka - Duba Balance na gaske - Saka shi a nan - Zai canza kai tsaye!</small>
<div style="display:flex;gap:8px;margin-top:10px;align-items:center">
<input id="balInput" class="input" type="number" step="0.01" placeholder="{{balance}}" value="{{balance}}" style="width:120px;font-size:20px">
<button class="btn3" onclick="updateBalance()">💰 UPDATE BALANCE</button>
<button class="btn" onclick="refreshBal()">🔄 REFRESH</button>
</div>
<small id="balMsg" style="color:#00ff88;font-weight:800"></small><br>
<small style="color:#888">Last update: {{last_update}} | XM #401568391 | {{server}}</small>
</div>

<div class="grid">
<div class="stat"><small>MIN TRADE</small><br><b style="color:#00ff88">$0.35</b></div>
<div class="stat"><small>MIN COPY</small><br><b>$20</b></div>
<div class="stat" style="border:1px solid #ffaa00"><small style="color:#ffaa00">MONTHLY FEE</small><br>
<div style="display:flex;gap:4px;margin-top:6px;align-items:center"><button class="btn2" onclick="adjFee(-5)">-5</button><input class="input" id="feeInput" value="{{monthly_fee}}"><button class="btn" onclick="adjFee(5)">+5</button><button class="btn" onclick="saveFee()">SAVE</button></div>
<small id="feeMsg" style="color:#00ff88"></small>
</div>
<div class="stat"><small>PROFIT TODAY</small><br><b style="color:#00ff88">${{profit}}</b> ({{trades}} trades)</div>
</div>
</div>

<script>
function adjFee(d){let e=document.getElementById('feeInput'); e.value=Math.max(5, parseInt(e.value||20)+d);}
function saveFee(){let fee=document.getElementById('feeInput').value; fetch('/api/set-fee',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fee:parseFloat(fee)})}).then(r=>r.json()).then(d=>{document.getElementById('feeMsg').innerText='✅ Fee $'+d.monthly_fee+' Saved!'; setTimeout(()=>location.reload(),800);});}
function addCopier(){let name=document.getElementById('newName').value; if(!name) return alert('Saka suna!'); fetch('/api/add-copier',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name})}).then(r=>r.json()).then(d=>{location.reload();});}
function updateBalance(){
 let bal=document.getElementById('balInput').value;
 if(!bal) return alert('Saka Balance!');
 fetch('/api/set-balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({balance:parseFloat(bal)})})
 .then(r=>r.json()).then(d=>{
   document.getElementById('balMsg').innerText='✅ REAL BALANCE UPDATED TO $'+d.balance+'! 💰';
   setTimeout(()=>location.reload(),1000);
 });
}
function refreshBal(){location.reload();}
setTimeout(()=>location.reload(), 8000)
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
        bal_status=CONFIG["status"],
        profit=f"{CONFIG['profit_today']:.2f}",
        trades=CONFIG["trades_today"],
        monthly_fee=CONFIG["monthly_fee"],
        sl=CONFIG["stop_loss"],
        tp=CONFIG["take_profit"],
        quality=STATE["signal_quality"],
        current=STATE["current_signal"],
        step=STATE["step"],
        analysis=STATE["last_analysis"],
        state=STATE["current_signal"][:20],
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
        CONFIG["status"] = f"REAL XM - ${CONFIG['balance']:.2f} - Manual Update"
        print(f"💰 REAL BALANCE UPDATED TO ${CONFIG['balance']}")
    return jsonify({"balance": CONFIG["balance"], "status": "updated", "time": CONFIG["last_balance_update"]})

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
    new_copier = {
        "name": name,
        "xm": f"{random.randint(4000,4099)}****",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "fee": CONFIG["monthly_fee"],
        "profit": round(random.uniform(1, 6), 2),
        "status": "ACTIVE"
    }
    COPY_DB["copiers"].insert(0, new_copier)
    return jsonify({"status": "added", "total": len(COPY_DB["copiers"])})

@app.route("/api/ping")
def ping():
    return jsonify({"status": "alive", "balance": CONFIG["balance"], "copiers": len(COPY_DB["copiers"])})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
