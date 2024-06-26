from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# 데이터 로드
data = pd.read_csv(r'C:\Users\ffjjo\OneDrive\바탕 화면\Capstone1\iphone_pricing/Final_capstone.csv')

MODELS = ['아이폰15프로맥스', '아이폰15프로', '아이폰15플러스', '아이폰15',
          '아이폰14프로맥스', '아이폰14프로', '아이폰14플러스', '아이폰14',
          '아이폰13프로맥스', '아이폰13프로', '아이폰13미니', '아이폰13',
          '아이폰12프로맥스', '아이폰12프로', '아이폰12미니', '아이폰12',
          '아이폰11프로맥스', '아이폰11프로', '아이폰11',
          '아이폰XS맥스', '아이폰XS', '아이폰XR', '아이폰X',
          '아이폰8플러스', '아이폰8',
          '아이폰7플러스', '아이폰7',
          '아이폰6플러스', '아이폰6S', '아이폰6',
          '아이폰5S', '아이폰5',
          '아이폰4S', '아이폰4',
          '아이폰3gs']
CAPACITIES = ['16GB','32GB', '64GB', '128GB', '256GB', '512GB', '1TB']

@app.route('/')
def index():
    return render_template('index.html', models=MODELS, capacities=CAPACITIES)

@app.route('/get_price', methods=['POST'])
def get_price():
    model = request.form['model']
    capacity = request.form['capacity']
    
    filtered_data = data[(data['모델명'] == model) & (data['용량'] == capacity)]
    
    # S급, A급, B급 가격을 비교하여 비정상적인 경우 데이터를 필터링
    if 'S급' in filtered_data['등급'].values and 'B급' in filtered_data['등급'].values:
        s_price = filtered_data[filtered_data['등급'] == 'S급']['가격'].mean()
        filtered_data = filtered_data[~((filtered_data['등급'] == 'B급') & (filtered_data['가격'] > s_price))]

    if 'A급' in filtered_data['등급'].values and 'B급' in filtered_data['등급'].values:
        a_price = filtered_data[filtered_data['등급'] == 'A급']['가격'].mean()
        filtered_data = filtered_data[~((filtered_data['등급'] == 'B급') & (filtered_data['가격'] > a_price))]
    
    if filtered_data.empty:
        grade_prices = {"S급": "데이터 부족", "A급": "데이터 부족", "B급": "데이터 부족"}
    else:
        grade_prices = filtered_data.groupby('등급')['가격'].mean().round(-3).to_dict()
       
        grade_prices = {k: f"{v:.0f} 원" if not pd.isna(v) else "데이터 부족" for k, v in grade_prices.items()}
    
        for grade in ['S급', 'A급', 'B급']:
            if grade not in grade_prices:
                grade_prices[grade] = "데이터 부족"
    
    return jsonify(grade_prices)

if __name__ == '__main__':
    app.run(debug=True)
