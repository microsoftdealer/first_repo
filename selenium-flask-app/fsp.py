from flask import Flask, request, jsonify
app = Flask(__name__)
from calc import sum_int
from selen import parse_dolgi, parse, parse_black
import asyncio


@app.route('/getDolgi')
async def get_dolgi():
    sur_name = request.args['lname']
    name = request.args['name']
    m_name = request.args['mname']
    b_date = request.args['bdate']
    answer = await parse_dolgi(lname, name, mname, bdate)
    return answer


@app.route('/get')
def parse_driver_license():
  license = request.args['license']
  answer = parse(license)
  return jsonify(answer)


@app.route('/getBlack')
async def get_black():
    fio = request.args['fio']
    answer = await parse_black(fio)
    return answer


@app.route('/calc')
def sum_ints():
    int_a = int(request.args['int_a'])
    int_b = int(request.args['int_b'])
    result = sum_int(int_a, int_b)
    return result
