from flask import Flask, request, render_template,flash
import algorithm1, algorithm2, algorithm3  # Import algorithm modules
import regenerate_map
from initial_map import initial_map
import secrets
app = Flask(__name__)
app.debug = True
secret_key = secrets.token_hex(16)  # Generate a random 16-byte (32 characters) secret key

app.secret_key = secret_key
stations=[
'嘉禾望岗', '南浦', '体育西路', '广州塔', '岗顶',
'林和西', '京溪南方医院', '西塱', '厦滘', '公园前',
'龙归', '高增', '石壁', '市桥', '沥滘', '东晓南',
'华师', '五山', '坑口', '南洲', '白云公园',
'烈士陵园', '汉溪长隆', '白云大道北', '燕塘',
'陈家祠', '长寿路', '三元里', '会江', '江泰路',
'西门口', '江南西', '芳村', '江夏', '白云文化广场',
'客村', '石牌桥', '广州南站', '黄沙', '东山口',
'广州火车站', '萧岗', '体育中心', '永泰', '纪念堂',
'黄边', '杨箕', '越秀公园', '飞翔公园', '同和',
'花地湾', '大塘', '机场北', '昌岗', '天河客运站',
'机场南', '海珠广场', '市二宫', '洛溪', '番禺广场',
'农讲所', '大石', '珠江新城', '人和', '广州东站', '梅花园'
]
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method=="GET":
        initial_map() # Initialize the map when the page is first loaded

    if request.method == 'POST':
        # Retrieve start and end stations from the form submission
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        # Validate if the stations are in the supported list
        if start_station not in stations or end_station not in stations:
            error = "Starting or ending station is not in the list of supported stations. Please re-enter."
            return render_template('index.html', error=error)

        # Check if start_station and end_station are the same
        if start_station == end_station:
            error = "Starting and ending station cannot be the same"
            flash(error)
            return render_template('index.html', error=error)
        selected_algorithm = request.form['algorithm']
        # Determine which algorithm to use based on user selection
        if selected_algorithm == 'algorithm1':
            results = algorithm1.calculate_path(start_station, end_station)
        elif selected_algorithm == 'algorithm2':
            results = algorithm2.calculate_path(start_station, end_station)
        elif selected_algorithm == 'algorithm3':
            results = algorithm3.calculate_path(start_station, end_station)

        # Handle the case where no route is found
        if not results:
            error = "两站不可达"
            flash(error)
            return render_template('index.html', error=error)

        # Regenerate the subway route map based on the results
        regenerate_map.regenerate_map(results)
        # Display the results on the webpage
        return render_template('index.html', results=results)
    # Load the initial template for the webpage
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
