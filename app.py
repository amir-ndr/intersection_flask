from flask import Flask, request
from datetime import datetime
from flask.json import jsonify

app = Flask(__name__)

def parse_line(data):
    x = data['x']
    y = data['y']
    w = data['width']
    h = data['height']
    rec = (x, y, x+w, y+h)
    return rec

def inter_area(rec_main, rec):
    (main_x1, main_y1, main_x2, main_y2) = rec_main
    (x1, y1, x2, y2) = rec

    xi_1 = max(main_x1, x1)
    yi_1 = max(main_y1, y1)
    xi_2 = min(main_x2, x2)
    yi_2 = min(main_y2, y2)
    intersection_width = xi_2-xi_1
    intersection_height = yi_2-yi_1

    inter_area = max(intersection_width, 0) * max(intersection_height, 0)
    return inter_area


final = []
@app.route('/', methods=['GET', 'POST'])
def f():
    if request.method == 'POST':
        data = request.get_json()
        data_main = data['main']
        data_inputs = data['input']
        rec_main = parse_line(data_main)

        for i in range(len(data_inputs)):
            rec_dict = data_inputs[i]
            rec = parse_line(rec_dict)
            intersection_area = inter_area(rec_main, rec)
            if intersection_area>0:
                now = datetime.now()
                now_string = now.strftime("%Y-%m-%d %H:%M:%S")
                rec_dict['time'] = now_string
                rec_dict['intersection area'] = intersection_area
                final.append(rec_dict)

        return 'data received successfully!'
    else:
        return jsonify(final)

app.run(host="0.0.0.0", port=8080)