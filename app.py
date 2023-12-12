from flask import Flask, render_template, request, redirect, url_for
global a
from ks import main
from maps import get_data
import random

amen = {
  'ac': 'AC',
  'geyser': 'Geyser',
  'locker': 'Lockers',
  'security': 'Security',
  'common': 'Common Room',
  'wifi': 'WiFi',
  'food': 'Food'
}
app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
  if request.method == "POST":
    proximity = request.form.get("dropdown")
    budget = request.form.get("slider")
    ac_count = request.form.get('acCount')
    geyser_count = request.form.get('geyserCount')
    locker_count = request.form.get('lockerCount')
    security_count = request.form.get('securityCount')
    common_count = request.form.get('commonCount')
    wifi_count = request.form.get('wifiCount')
    food_count = request.form.get('foodCount')
    amenities_count = 0
    amenities = []
    global location
    location = request.form.get('place')
    dict = {
      'ac': ac_count,
      'geyser': geyser_count,
      'locker': locker_count,
      'security': security_count,
      'common': common_count,
      'wifi': wifi_count,
      'food': food_count
    }
    checked_checkboxes = []
    global options
    options = [('2', '0-2 kms'), ('5', '2-5 kms'), ('10', '5-10 kms'),
               ('20', '10-20 kms')]
    selected = proximity
    for i, j in dict.items():
      if int(j) % 2:
        amenities_count += 1
        amenities.append(i)
        checked_checkboxes.append(i)
    # Example list of checkboxes to be checked
    data = get_data(location, int(budget), amenities_count)
    resno = len(data)
    am_gen = [random.randint(0, 7 - amenities_count) for i in range(resno)]
    l1 = []
    count = 0
    for i in am_gen:
      j = amenities[:]
      count += 1
      for n in range(i):
        k = random.choice([_ for _ in amen if _ not in j])
        if k not in j:
          j.append(k)
      l1.append(j)
    ksdata = knapsack(data)
    rec = main(ksdata, int(budget), amenities_count, int(proximity))
    if len(rec) < 1:
      return ('No results found')
    rem = [i for i in rec]
    if rem[0] == 'No results found':
      return ('No results found')
    try:
      rec = {rem[0]: data.pop(rem[0])}
    except KeyError:
      return render_template('index3.html',
                             loc=location,
                             slider_value=budget,
                             checked_checkboxes=checked_checkboxes,
                             selected_option=proximity,
                             options=options)
    count = 1
    l1 = [[amen[j] for j in i] for i in l1]
    for _, i in data.items():
      a = ','.join(l1[count])
      i = i + (a, )
      data[_] = i
      count += 1
    for _, i in rec.items():
      a = ','.join(l1[0])
      i = i + (a, )
      rec[_] = i

  return render_template('index2.html',
                         rec=rec,
                         data=data,
                         loc=location,
                         resno=resno,
                         checked_checkboxes=checked_checkboxes,
                         slider_value=budget,
                         selected_option=selected,
                         options=options)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
  if request.method == 'POST':
    data = request.get_json()
    amenities = data.get('checkboxes')
    proximity = data.get('dropdownValue')
    budget = data.get('rangeOneValue')
    amenities_count = len(amenities)
    data = get_data(location, int(budget), amenities_count)
    resno = len(data)
    ksdata = knapsack(data)
    rec = main(ksdata, int(budget), amenities_count, int(proximity))
    rem = [i for i in rec]
    rec = {rem[0]: data.pop(rem[0])}
    return redirect(url_for('submit'))
  return render_template('index2.html',
                         rec=rec,
                         data=data,
                         loc=location,
                         resno=resno,
                         checked_checkboxes=amenities,
                         slider_value=budget,
                         selected_option=proximity,
                         options=options)


def knapsack(data):
  x = []
  for i in data.items():
    y = []
    y.append(i[0])
    for j in i[1]:
      if len(y) == 1:
        y.append(float(j))
      elif len(y) in [2, 3]:
        y.append(int(j))
    x.append(tuple(y))
  return x
 
if __name__ == '__main__':
  app.run()
