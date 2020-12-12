// <%text>

$( document ).ready(() =>{
    window.measurements = new Measurements();
    window.measurements.getData(7);

    $('#changeRange button').click( (event) => {
        const delta = parseInt($(event.target).data('delta'));
        window.measurements.getData(delta);
    }
    );

});

class Measurements {
    constructor() {
        this.__name___ = 'Measurements';
        this.data = [];
        this.queryInfo = {};
        this.latest = {};
        this.sensorDetails = {};
    }

    getData(delta) {
        jQuery.get(`/read?delta=${delta}`, {}, ({data, sensor, start, stop, sensor_details}) => {
            //returned is {"data": [{"datetime": "2020-12-12T10:46:16.358734", "sensor": "test:A", "value": 100.0}],
            //             "start": "2020-12-07T10:46:27.094380",
            //             "stop": "2020-12-12T10:46:27.094407",
            //             "sensor": "all"}
            // and sensor_details:
            // {"test:A": {'id': '1', 'sensor': 'test:A', 'location': 'localhosted', 'model': 'None', 'unit': '°C',
            //                  'graph_color': '#c0c0c0', 'dashed': 'True', 'axis': 'hundred'},
            //
            this.queryInfo = {start: start, stop: stop, sensor: sensor};
            this.sensorDetails = sensor_details;
            this.data = data.sort((a,b) => Date.parse(a.datetime) > Date.parse(b.datetime) ? 1 : -1);
            this.applyData();
        });
    };

    applyData() {
        // called by .getData.
        // newest_last
        console.log(this.__name___);
        if (Object.keys(this.latest).length === 0) {
            this.latest = this.data.reduce((accumulator, currentValue) => {accumulator[currentValue.sensor] = currentValue.value; return accumulator}, {});
            this.showLatest();
        }
        this.plot();
    }

    getLineDetails(sensor) {
        const details = this.sensorDetails[sensor];
        const lineDetails = {};
        if (details === undefined) {
            lineDetails.color = '#dcdcdc';
        } else {
            lineDetails.color = details.graph_color;
            if (details.dashed === 'True') {
                lineDetails.dash = 'dashdot';
            }
        }
        //{"test:A": {'id': '1', 'sensor': 'test:A', 'location': 'localhosted', 'model': 'None', 'unit': '°C',
        //             //                  'graph_color': '#c0c0c0', 'dashed': 'True', 'axis': 'hundred'},
    }

    getUnit(sensor) {
        const details = this.sensorDetails[sensor];
        if (details === undefined) {
            return '[AU]'
        } else {
            return details.unit;
        }
    }

    getExtras(sensor) {
        const details = this.sensorDetails[sensor];
        if (details === undefined) {
            return 'N/A'
        } else {
            return `Location: ${details.location}.<br/> Model: ${details.model}`;
        }
    }

    showLatest() {
        const latest_div = $('#latest');
        latest_div.children().detach();
        latest_div.append(`<ul></ul>`);
        const ul = latest_div.children('ul');
        Object.keys(this.latest).forEach(key => {
           ul.append(`<div class="card m-2">
                    <div class="card-header">
                        ${key}
                      </div>
                        <div class="card-body">
                          <h3 class="card-title">${this.latest[key]}${this.getUnit(key)}</h3>
                          <p class="card-text text-muted">${this.getExtras(key)}</p>
                        </div>
                      </div>`);
        });
    }

    plot() {
        // data is an array to objects.
        // transposed is {"test:A":{"datetimes":["2020-12-12T10:46:16.358734"],"values":[100]}}"
        // note plurals...
        const transposed = this.data.reduce((accumulator, currentValue) => {
            if (accumulator[currentValue.sensor] === undefined) {
                accumulator[currentValue.sensor] = {'datetimes': [], 'values': []}}
            accumulator[currentValue.sensor].datetimes.push(currentValue.datetime);
            accumulator[currentValue.sensor].values.push(currentValue.value);
            return accumulator
            }, {});

        const sensorLines = {"test:A": {color: '#ff7f0e'},
                            // old.
                            'Outside temperature': {color: '#ff7f0e', dash: 'dashdot'},
                            'Outside humidity': {color: '#1f77b4', dash: 'dashdot'},
                            'Humidity' : {color: '#1f77b4'},
                            'CO_2': {color: '#8c564b'},
                            'TVOC': {color: '#2ca02c'}
        };
        // {color: '#ff7f0e', dash: 'dashdot'}
        const traces = Object.entries(transposed)
                             .map(([sensor, {datetimes, values}], i) => ({
                                                                            x: datetimes,
                                                                            y: values,
                                                                            name: sensor,
                                                                            type: 'scatter',
                                                                            line: this.getLineDetails(sensor),
                                                                            mode: 'lines'
                                                                        })
                             );


var layout = {
  title: 'Measurements',
  xaxis: {domain: [0.15, 0.7]},
  yaxis: {title: 'Temperature [°C]', range: [5,30], dtick: 1},
  // yaxis2: {
  //   title: 'Humidity [%]',
  //   overlaying: 'y',
  //   side: 'right',
  //   range: [0,100], dtick: 100/25
  // },
  // yaxis3: {
  //   title: 'Amount [ppm]',
  //   overlaying: 'y',
  //   side: 'right',
  //   range: [0,10000], dtick: 10000/25,
  //   anchor: "free",
  //   overlaying: "y",
  //   position: 0.85
  // },
  // shapes: {{ shapes|safe}}
};

        Plotly.newPlot('graph', traces, layout);

    }
}

// </%text>