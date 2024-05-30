from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import tkinter as tk
import json
app = Flask(__name__)

root = tk.Tk()
root.title("")
root.geometry("180x160")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    #file = request.files['file']
    #if file:
    #    print("have")
            
    if 'clientFile' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['clientFile']

    if file:
        df_true = pd.read_excel('True.xlsx')
        df_pre = pd.read_excel(file)
        result_left = pd.merge(df_true, df_pre, on='number', how='left')
        print("Left Join:\n", result_left)
        conf_matrix = confusion_matrix(result_left['label_x'], result_left['label_y'], labels=['loyal', 'partial churn', 'churn'])
        print(conf_matrix)
        print("成功")
        # 計算準確率
        accuracy = accuracy_score(result_left['label_x'], result_left['label_y'])
        print(f"Accuracy: {accuracy:.2f}")
        # 顯示混淆矩陣並標注標籤名稱
        # disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['loyal', 'p_churn', 'churn'])
        # disp.plot(cmap=plt.cm.Blues) 
            
        #label = tk.Label(root, text='準確率:'+str(accuracy), font=("Helvetica", 16))
        #label.pack(padx=20, pady=20)
        print('準確率:'+str(accuracy))
        #test = json.dumps(json.loads(result_left.to_json(orient="records")))
        excel_data = json.loads(result_left.to_json(orient="records"))
        
        matrix = {
            "1":str(conf_matrix[0][0]),
            "2":str(conf_matrix[0][1]),
            "3":str(conf_matrix[0][2]),
            "4":str(conf_matrix[1][0]),
            "5":str(conf_matrix[1][1]),
            "6":str(conf_matrix[1][2]),
            "7":str(conf_matrix[2][0]),
            "8":str(conf_matrix[2][1]),
            "9":str(conf_matrix[2][2]),
        }
        print(matrix)
        data = {"status": "true" ,"data": excel_data, "accuracy":str(accuracy), "matrix": matrix}

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)