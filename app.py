from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reel Insights</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body class="bg-black text-[#f5f5f5] font-sans pb-16 select-none">
    
    <!-- Top Header -->
    <div class="flex justify-between items-center px-4 py-3 border-b border-[#262626] sticky top-0 bg-black z-20">
        <div class="flex items-center space-x-3">
            <h1 class="text-base font-semibold">Reel insights</h1>
        </div>
        <button onclick="saveInsights()" class="text-[#0095f6] font-semibold text-sm">Done</button>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-[#262626] text-sm text-[#a8a8a8] justify-around bg-black">
        <button class="py-2.5 border-b-2 border-white text-white font-medium">Overview</button>
        <button class="py-2.5">Engagement</button>
        <button class="py-2.5">Audience</button>
    </div>

    <div class="p-4 space-y-4">
        
        <!-- Reel Preview Card -->
        <div class="bg-[#121212] p-3 rounded-xl border border-[#262626] flex items-center space-x-4">
            <div class="w-16 h-24 bg-[#262626] rounded-lg overflow-hidden flex items-center justify-center">
                <span class="text-xs text-zinc-400">Reel</span>
            </div>
            <div class="grid grid-cols-4 gap-2 flex-1 text-center">
                <div>
                    <label class="text-[10px] text-[#a8a8a8]">Likes</label>
                    <input type="number" id="likesInput" class="w-full bg-[#1a1a1a] border border-[#363636] rounded p-1 text-xs text-center font-bold text-white focus:outline-none" value="2799">
                </div>
                <div>
                    <label class="text-[10px] text-[#a8a8a8]">Comments</label>
                    <input type="number" id="commentsInput" class="w-full bg-[#1a1a1a] border border-[#363636] rounded p-1 text-xs text-center font-bold text-white focus:outline-none" value="51">
                </div>
                <div>
                    <label class="text-[10px] text-[#a8a8a8]">Shares</label>
                    <input type="number" id="sharesInput" class="w-full bg-[#1a1a1a] border border-[#363636] rounded p-1 text-xs text-center font-bold text-white focus:outline-none" value="283">
                </div>
                <div>
                    <label class="text-[10px] text-[#a8a8a8]">Saves</label>
                    <input type="number" id="savesInput" class="w-full bg-[#1a1a1a] border border-[#363636] rounded p-1 text-xs text-center font-bold text-white focus:outline-none" value="454">
                </div>
            </div>
        </div>

        <!-- Who viewed your reel -->
        <div class="bg-[#121212] p-4 rounded-xl border border-[#262626]">
            <h2 class="text-xs font-semibold text-[#a8a8a8] mb-3">Who viewed your reel</h2>
            <div class="space-y-3">
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span>Followers</span>
                        <input type="text" id="followersPct" class="w-16 bg-[#1a1a1a] border border-[#363636] rounded text-right px-1 text-xs font-bold text-white" value="41.2%">
                    </div>
                    <div class="w-full bg-[#262626] h-1.5 rounded overflow-hidden">
                        <div class="bg-[#0095f6] h-full w-[41%]"></div>
                    </div>
                </div>
                <div>
                    <div class="flex justify-between text-xs mb-1">
                        <span>Non-followers</span>
                        <input type="text" id="nonFollowersPct" class="w-16 bg-[#1a1a1a] border border-[#363636] rounded text-right px-1 text-xs font-bold text-white" value="58.8%">
                    </div>
                    <div class="w-full bg-[#262626] h-1.5 rounded overflow-hidden">
                        <div class="bg-[#0095f6] h-full w-[59%]"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Audience Details (Country / Custom Editor) -->
        <div class="bg-[#121212] p-4 rounded-xl border border-[#262626]">
            <div class="flex justify-between items-center mb-3">
                <h2 class="text-xs font-semibold text-[#a8a8a8]">Audience Details</h2>
                <span class="text-[10px] text-[#0095f6]">Hop Clipping Ready</span>
            </div>
            <div class="space-y-3">
                <div>
                    <label class="text-[11px] text-[#a8a8a8]">Top Country Name</label>
                    <input type="text" id="countryName" class="w-full bg-[#1a1a1a] border border-[#363636] rounded-lg p-2 text-sm font-bold text-white focus:outline-none focus:border-[#0095f6]" value="India">
                </div>
                <div>
                    <label class="text-[11px] text-[#a8a8a8]">Country Percentage (%)</label>
                    <input type="text" id="countryPct" class="w-full bg-[#1a1a1a] border border-[#363636] rounded-lg p-2 text-sm font-bold text-white focus:outline-none focus:border-[#0095f6]" value="54.2%">
                </div>
            </div>
        </div>

        <!-- Update Button -->
        <button onclick="saveInsights()" class="w-full bg-[#0095f6] hover:bg-[#1877f2] active:scale-[0.98] transition p-3.5 rounded-xl font-semibold text-white text-sm shadow-lg">
            Save & Update Insights
        </button>

    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function saveInsights() {
            let data = {
                likes: document.getElementById('likesInput').value,
                comments: document.getElementById('commentsInput').value,
                shares: document.getElementById('sharesInput').value,
                saves: document.getElementById('savesInput').value,
                followersPct: document.getElementById('followersPct').value,
                nonFollowersPct: document.getElementById('nonFollowersPct').value,
                countryName: document.getElementById('countryName').value,
                countryPct: document.getElementById('countryPct').value
            };

            fetch('/api/update-insights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                tg.close();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to update.');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/update-insights', methods=['POST'])
def update_insights():
    data = request.json
    print("Hop Clipping Data Saved:", data)
    return jsonify({
        "status": "success", 
        "message": "Reel insights updated successfully!"
    })

if __name__ == '__main__':
    app.run(debug=True)
