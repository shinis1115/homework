from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
# 목표: 정보입력후 주문하기 버튼 클릭시 주문 목록에 추가
def save_order():
    # 1. client로부터 data 받기
    name_receive = request.form['name_give']
    quantity_receive = request.form['quantity_give']
    addr_receive = request.form['addr_give']
    phone_receive = request.form['phone_give']

    # 2. MongoDB에 저장
    doc = {
        'name': name_receive,
        'quantity': quantity_receive,
        'addr': addr_receive,
        'phone': phone_receive
    }
    db.shopping_mall.insert_one(doc)
    # 3. json 형식으로 정보 제공 : 입력 성공 확인 및 반환할 msg 값
    return jsonify({'result': 'success', 'msg':'주문이 완료되었습니다!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
# 목표 : 주문 목록 보여주기
def view_orders():
    orders = list(db.shopping_mall.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)