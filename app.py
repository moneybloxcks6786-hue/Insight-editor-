from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    # templates ഫോൾഡറിനുള്ളിലെ index.html ഫയൽ ലോഡ് ചെയ്യുന്നു
    return render_template('index.html')

@app.route('/api/update-insights', methods=['POST'])
def update_insights():
    data = request.json
    reach = data.get('reach')
    engagement = data.get('engagement')
    
    # ഇവിടെ ഡാറ്റ പ്രോസസ്സ് ചെയ്യാം അല്ലെങ്കിൽ പ്രിന്റ് ചെയ്ത് നോക്കാം
    print(f"Received Reach: {reach}, Engagement: {engagement}")
    
    return jsonify({
        "status": "success", 
        "message": "Insights updated successfully!"
    })

if __name__ == '__main__':
    app.run(debug=True)