import os
from flask import Flask, render_template, request, jsonify
from logic import load_data, run_search

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(current_dir, 'templates'))

datasets = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def build():
    data = request.json
    budget = float(data['budget'])
    purpose = data['purpose']
    algo = data['algorithm'] # استلام نوع الخوارزمية من الواجهة
    
    result, cost, visited = run_search(algo, budget, purpose, datasets)
    
    if result:
        return jsonify({
            "success": True, 
            "build": result, 
            "total_cost": cost, 
            "nodes": visited,
            "algorithm_used": algo
        })
    return jsonify({"success": False, "message": "لم يتم العثور على تجميعة مناسبة بهذه الميزانية."})

if __name__ == '__main__':
    app.run(debug=True)