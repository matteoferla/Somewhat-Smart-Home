// <%text>

$(document).ready(() => {
    window.measurements = new Measurements();
    window.measurements.getNights(7);
    window.measurements.getData(7);
    window.measurements.getPhotos(7);

    // refresh
    window.timer = setInterval(()=> {
                                            window.measurements = new Measurements();
                                            window.measurements.getNights(7);
                                            window.measurements.getData(7);
                                            window.measurements.getPhotos(7);
                                            },
                                60*60*1e3);


    $('#changeRange button').click((event) => {
            const delta = parseInt($(event.target).data('delta'));
            window.measurements.getNights(delta);
            window.measurements.getData(delta);
            window.measurements.getPhotos(delta);
        }
    );

    $('#scrollDelta').change((event) => {
        const delta = parseInt($(event.target).val());
        window.measurements.getNights(delta);
        window.measurements.getData(delta);
        window.measurements.getPhotos(delta);
    });

});

class Measurements {
    constructor() {
        this.__name___ = 'Measurements';
        this.data = [];
        this.queryInfo = {};
        this.latest = {};
        this.sensorDetails = {};
        this.photos = [];
        this.nights = [];
        this.twilights = [];
    }

    getPhotos(delta) {
        jQuery.get(`/show?delta=${delta}`, {}, ({start, stop, photos}) => {
            this.photos = photos.sort((a, b) => Date.parse(a.datetime) < Date.parse(b.datetime) ? 1 : -1)
                                .reduce((accumulator, currentValue) => {
                                        if (currentValue.path === 'None') {}
                                        else if (accumulator[currentValue.sensor] === undefined) {
                                            accumulator[currentValue.sensor] = [currentValue];
                                        } else {
                                            accumulator[currentValue.sensor].unshift(currentValue);
                                        }

                                        return accumulator
                                    }, {});

            this.showLatestPhoto();
        });
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
            this.data = data.sort((a, b) => Date.parse(a.datetime) > Date.parse(b.datetime) ? 1 : -1);
            this.applyData();
        });
    };

    getNights(delta) {
        jQuery.get(`/night?delta=${delta}`, {}, ({nights, twilights}) => {
            this.nights = nights;
            this.twilights = twilights;
        });
    }

    applyData() {
        // called by .getData.
        // newest_last
        if (Object.keys(this.latest).length === 0) {
            this.latest = this.data.reduce((accumulator, currentValue) => {
                accumulator[currentValue.sensor] = currentValue;
                return accumulator
            }, {});
            this.showLatestMeasurements();
        } else {
            //there is nothing to show :(
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
        return lineDetails;
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

    showLatestMeasurements() {
        const latest_div = $('#latest');
        latest_div.children().detach();
        // latest_div.append(`<ul></ul>`);
        // const ul = latest_div.children('ul');
        Object.keys(this.latest).forEach(key => {
            latest_div.append(`<div class="card m-2">
                    <div class="card-header">
                        ${key}
                      </div>
                        <div class="card-body">
                          <h3 class="card-title">${Number(this.latest[key].value.toFixed(1))}
                                                 ${this.getUnit(key)}</h3>
                          <p class="card-text text-muted">
                            ${this.getExtras(key)}
                          <br/>
                            (${this.latest[key].datetime})
                          </p>
                        </div>
                      </div>`);
        });
    }


    makePhotoCard(sensor, i) {
        const entry = this.photos[sensor][i];
        return `
<div class="card m-2">
   <img src="${entry.path}" class="card-img-top" alt="${sensor}" data-sensor="${sensor}">
   <div class="card-body">
      <h3 class="card-title">${sensor}</h3>
      <div class="card-text" data-sensor="${sensor}">
         <div class="d-flex flex-row">
            <div class="align-self-start">
               <button class="btn btn-outline-success photobtn previous" data-sensor="${sensor}" data-goto="${i - 1}">                         
               <i class="fas fa-chevron-left"></i>
               </button>
            </div>
            <div class="flex-fill text-center"  data-sensor="${sensor}" data-id="${entry.id}">${entry.datetime}</div>
            <div class="align-self-end">
               <button class="btn btn-outline-success photobtn next" data-sensor="${sensor}"  data-goto="${i + 1}">                         
               <i class="fas fa-chevron-right"></i>
               </button>
            </div>
         </div>
      </div>
   </div>
</div>`
    }

    showLatestPhoto() {
        const group_div = $('#photocards');
        group_div.children().detach();
        Object.keys(this.photos).forEach((sensor) => {
            const m = this;
            group_div.append(this.makePhotoCard(sensor, this.photos[sensor].length - 1));
            this.eventForNext.call(this, sensor);
            $(`.next[data-sensor="${sensor}"]`).hide();

        });
    }

    eventForNext(sensor) {
        const mthis = this;
        $(`.btn[data-sensor="${sensor}"]`).click(function(event) {
                //const target = $(event.target);
                const target = $(this);
                const sensor = target.data('sensor');
                const index = parseInt(target.data('goto'));
                console.log(sensor, index);
                if (index >= mthis.photos[sensor].length) {return 0}
                if (index <= -1) {return 0}
                const entry = mthis.photos[sensor][index];
                $(`img[data-sensor="${sensor}"]`).attr('src', entry.path);
                $(`.text-center[data-sensor="${sensor}"]`).html(entry.datetime);
                $(`.photobtn[data-sensor="${sensor}"]`).each((i, el) => {
                    if (i === 0) {
                        if (index - 1 >= 0) {
                            $(el).data('goto', index - 1);
                            $(el).show();
                        } else {
                            $(el).hide();
                        }
                    }
                    else {
                        if (index + 1 < mthis.photos[sensor].length) {
                            $(el).data('goto', index + 1);
                            $(el).show();
                        } else {
                            $(el).hide();
                        }
                    }
                });
            });
    }

    showLatest() {
        this.showLatestMeasurements();
        this.showLatestPhoto();
    }

    plot() {
        // data is an array to objects.
        // transposed is {"test:A":{"datetimes":["2020-12-12T10:46:16.358734"],"values":[100]}}"
        // note plurals...
        const transposed = this.data.reduce((accumulator, currentValue) => {
            if (accumulator[currentValue.sensor] === undefined) {
                accumulator[currentValue.sensor] = {'datetimes': [], 'values': []}
            }
            accumulator[currentValue.sensor].datetimes.push(currentValue.datetime);
            accumulator[currentValue.sensor].values.push(currentValue.value);
            return accumulator
        }, {});

        // const sensorLines = {"test:A": {color: '#ff7f0e'},
        //                     // old.
        //                     'Outside temperature': {color: '#ff7f0e', dash: 'dashdot'},
        //                     'Outside humidity': {color: '#1f77b4', dash: 'dashdot'},
        //                     'Humidity' : {color: '#1f77b4'},
        //                     'CO_2': {color: '#8c564b'},
        //                     'TVOC': {color: '#2ca02c'}
        // };
        // {color: '#ff7f0e', dash: 'dashdot'}
        const traces = Object.entries(transposed)
            .map(([sensor, {datetimes, values}], i) => ({
                    x: datetimes,
                    y: values,
                    name: sensor,
                    type: 'scatter',
                    line: this.getLineDetails(sensor),
                    mode: 'lines',
                    visible: 'legendonly',
                })
            );

        window.traces = traces;

        const nightshapes = this.nights.map(([dusk, dawn]) => {return {'type': 'rect', //pycharm screams if {{ }} form
                                                                  'xref': 'x',
                                                                  'yref': 'paper',
                                                                  'x0': dusk,
                                                                  'y0': 0,
                                                                  'x1': dawn,
                                                                  'y1': 1,
                                                                  'fillcolor': '#b3b3ff',  // midnightblue #191970 was too bright
                                                                  'opacity': 0.4,
                                                                  'line': {'width': 0},
                                                                  'layer': 'below'
                                                                  }});

        const twishapes = this.twilights.map(([a, b]) => {return {'type': 'rect',
                                                              'xref': 'x',
                                                              'yref': 'paper',
                                                              'x0': a,
                                                              'y0': 0,
                                                              'x1': b,
                                                              'y1': 1,
                                                              'fillcolor': '#6495ed',  // cornflowerblue
                                                              'opacity': 0.4,
                                                              'line': {'width': 0},
                                                              'layer': 'below'
                                                              }});

        const shapes = [...nightshapes, ...twishapes];

        var layout = {
            title: 'Measurements',
            //xaxis: {domain: [0.15, 0.7]},
            yaxis: {title: '1-100 unit', range: [0, 100], dtick: 5},
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
            shapes: shapes
        };

        Plotly.newPlot('graph', traces, layout);

    }
}

// </%text>
