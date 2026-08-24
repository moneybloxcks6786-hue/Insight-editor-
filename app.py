from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body class="bg-black text-white font-sans antialiased pb-16 select-none">

    <!-- Instagram Top Header -->
    <div class="flex justify-between items-center px-4 py-3 border-b border-zinc-800 sticky top-0 bg-black z-30">
        <span class="text-xl font-bold tracking-tighter italic">Instagram</span>
        <div class="flex space-x-4">
            <svg aria-label="Notifications" class="_ab6-" color="#f5f5f5" fill="#f5f5f5" height="24" role="img" viewBox="0 0 24 24" width="24"><path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 6.015-5.198 8.444-1.55 1.486-3.13 2.808-4.302 3.738-.173.138-.395.213-.622.213-.227 0-.449-.075-.622-.213-1.172-.93-2.752-2.252-4.302-3.738C5.152 15.137 2.5 12.194 2.5 9.122a4.989 4.989 0 0 1 4.708-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.117 1.763.137 0 .277-.588 1.117-1.763a4.21 4.21 0 0 1 3.676-1.941z"></path></svg>
            <svg aria-label="Direct" class="_ab6-" color="#f5f5f5" fill="#f5f5f5" height="24" role="img" viewBox="0 0 24 24" width="24"><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="22" x2="9.218" y1="3" y2="15.782"></line><polygon fill="none" points="11.983 20.91 22 13 22 3 12 3 2 13 11.983 20.91" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></polygon></svg>
        </div>
    </div>

    <!-- Main Feed / Profile Switcher View -->
    <div id="mainView" class="p-4 space-y-6">
        <!-- Profile Header Mock -->
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-16 h-16 bg-gradient-to-tr from-yellow-500 to-pink-500 p-0.5 rounded-full">
                    <div class="w-full h-full bg-black rounded-full flex items-center justify-center font-bold text-lg">W</div>
                </div>
                <div>
                    <h2 class="font-semibold text-sm">whop.clipping</h2>
                    <p class="text-xs text-zinc-400">Content Creator</p>
                </div>
            </div>
            <button onclick="openInsights()" class="bg-[#0095f6] text-white px-4 py-1.5 rounded-lg text-xs font-semibold">View Insights</button>
        </div>

        <!-- Simulated Post / Reel for Clipping Approval -->
        <div class="bg-zinc-900 rounded-xl overflow-hidden border border-zinc-800">
            <div class="p-3 flex items-center justify-between border-b border-zinc-800 text-xs">
                <span class="font-semibold">whop.clipping</span>
                <span class="text-[#0095f6] font-medium">Sponsored</span>
            </div>
            <div class="h-64 bg-zinc-800 flex items-center justify-center text-zinc-500 font-semibold relative">
                [ Tap 'View Insights' Above to Edit Stats ]
            </div>
            <div class="p-3 text-xs space-y-1">
                <p><span class="font-semibold">whop.clipping</span> Making serious passive income online! 🚀</p>
                <p class="text-zinc-500 text-[10px]">View insights to check performance</p>
            </div>
        </div>
    </div>

    <!-- Instagram Insights Editor Modal (Hidden by default, shown on click) -->
    <div id="insightsModal" class="hidden fixed inset-0 bg-black z-50 overflow-y-auto pb-20">
        <!-- Top Insights Header -->
        <div class="flex justify-between items-center px-4 py-3 border-b border-zinc-800 bg-black sticky top-0 z-20">
            <div class="flex items-center space-x-3">
                <button onclick="closeInsights()" class="text-white text-lg font-bold">←</button>
                <h1 class="text-base font-semibold">Insights</h1>
            </div>
            <button onclick="saveInsights()" class="text-[#0095f6] font-semibold text-sm">Done</button>
        </div>

        <div class="p-4 space-y-4">
            <!-- Overview Card -->
            <div class="bg-zinc-900 p-4 rounded-xl border border-zinc-800">
                <div class="flex justify-between text-xs text-zinc-400 mb-2">
                    <span>Performance (Last 30 days)</span>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="text-[11px] text-zinc-400">Reach</label>
                        <input type="text" id="reachInput" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg p-2 text-base font-bold mt-1 text-white focus:outline-none" value="342.5K">
                    </div>
                    <div>
                        <label class="text-[11px] text-zinc-400">Accounts Engaged</label>
                        <input type="text" id="engagedInput" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg p-2 text-base font-bold mt-1 text-white focus:outline-none" value="89.1K">
                    </div>
                </div>
            </div>

            <!-- Content Interactions -->
            <div class="bg-zinc-900 p-4 rounded-xl border border-zinc-800">
                <h2 class="text-xs font-semibold text-zinc-400 uppercase mb-3">Content Interactions</h2>
                <div class="space-y-3 divide-y divide-zinc-800">
                    <div class="flex justify-between items-center pt-1">
                        <span class="text-sm">Likes</span>
                        <input type="text" id="likesInput" class="w-28 bg-zinc-800 border border-zinc-700 rounded-lg p-1.5 text-right font-bold text-white" value="24.5K">
                    </div>
                    <div class="flex justify-between items-center pt-3">
                        <span class="text-sm">Comments</span>
                        <input type="text" id="commentsInput" class="w-28 bg-zinc-800 border border-zinc-700 rounded-lg p-1.5 text-right font-bold text-white" value="1,420">
                    </div>
                    <div class="flex justify-between items-center pt-3">
                        <span class="text-sm">Shares</span>
                        <input type="text" id="sharesInput" class="w-28 bg-zinc-800 border border-zinc-700 rounded-lg p-1.5 text-right font-bold text-white" value="6,840">
                    </div>
                    <div class="flex justify-between items-center pt-3">
                        <span class="text-sm">Saves</span>
                        <input type="text" id="savesInput" class="w-28 bg-zinc-800 border border-zinc-700 rounded-lg p-1.5 text-right font-bold text-white" value="4,120">
                    </div>
                </div>
            </div>

            <!-- Audience Demographics -->
            <div class="bg-zinc-900 p-4 rounded-xl border border-zinc-800">
                <h2 class="text-xs font-semibold text-zinc-400 uppercase mb-3">Audience Demographics</h2>
                <div class="space-y-3">
                    <div>
                        <label class="text-[11px] text-zinc-400">Top Country (Tier 1)</label>
                        <div class="flex space-x-2 mt-1">
                            <input type="text" id="countryName" class="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg p-2 text-sm font-bold text-white" value="United States">
                            <input type="text" id="countryPct" class="w-24 bg-zinc-800 border border-zinc-700 rounded-lg p-2 text-sm font-bold text-white text-right" value="72.4%">
                        </div>
                    </div>
                    <div>
                        <label class="text-[11px] text-zinc-400">Age Range</label>
                        <input type="text" id="ageRange" class="w-full bg-zinc-800 border border-zinc-700 rounded-lg p-2 text-sm font-bold mt-1 text-white" value="18-24 (64%)">
                    </div>
                </div>
            </div>

            <button onclick="saveInsights()" class="w-full bg-[#0095f6] hover:bg-[#1877f2] p-3.5 rounded-xl font-semibold text-white text-sm shadow-lg">
                Save & Update Insights
            </button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        function openInsights() {
            document.getElementById('insightsModal').classList.remove('hidden');
        }

        function closeInsights() {
            document.getElementById('insightsModal').classList.add('hidden');
        }

        function saveInsights() {
            let data = {
                reach: document.getElementById('reachInput').value,
                engaged: document.getElementById('engagedInput').value,
                likes: document.getElementById('likesInput').value,
                comments: document.getElementById('commentsInput').value,
                shares: document.getElementById('sharesInput').value,
                saves: document.getElementById('savesInput').value,
                countryName: document.getElementById('countryName').value,
                countryPct: document.getElementById('countryPct').value,
                ageRange: document.getElementById('ageRange').value
            };

            fetch('/api/update-insights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                closeInsights();
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
    print("Saved Data:", data)
    return jsonify({
        "status": "success", 
        "message": "Instagram insights updated successfully!"
    })

if __name__ == '__main__':
    app.run(debug=True)
