(function ($) {
  'use strict';

  var fullHeight = function () {
    $('.js-fullheight').css('height', $(window).height());
    $(window).resize(function () {
      $('.js-fullheight').css('height', $(window).height());
    });
  };
  fullHeight();

  $('#sidebarCollapse').on('click', function () {
    $('#sidebar').toggleClass('active');
  });
})(jQuery);

function animatedForm() {
  const arrows = document.querySelectorAll('.fa-arrow-right');

  arrows.forEach((arrow) => {
    arrow.addEventListener('click', () => {
      const parent = arrow.parentElement;
      const nextForm = parent.nextElementSibling;

      nextQuestion(parent, nextForm, arrow);
    });
  });
}
function show() {
  const arrows = document.querySelector('.fa-arrow-right');
  arrows.classList.add('show');
}

function nextQuestion(parent, nextForm, arrow) {
  parent.classList.add('innactive');
  parent.classList.remove('active');
  nextForm.classList.add('active');
  arrow.parentNode.removeChild(arrow);
}

animatedForm();

const BASE_URL = window.location.origin + '/api';
// const base_url = window.location.origin + '/api';
// console.log(BASE_URL);
// console.log(base_url);

function generatePortfolios(portfolio) {
  let array = [];
  for (let [key, value] of Object.entries(portfolio)) {
    if (
      key != 'id' &&
      key != 'name' &&
      key != 'desc' &&
      key != 'fees' &&
      value != '0'
    ) {
      array.push([key, value]);
    }
  }
  let title = `KIKEN ${portfolio.name} ETF Allocation`;
  array.unshift(['ETF', 'Allocation']);

  google.load('visualization', '1', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(array);

    var options = {
      legend: {
        position: 'bottom',
        alignment: 'start',
        textStyle: { fontSize: 12 },
      },

      title: title,
      pieHole: 0.3,
      width: '100%',
      height: '100%',
      is3D: false,
      pieStartAngle: 0,
      animation: {
        duration: 1000,
        easing: 'in',
      },
    };
    var chart = new google.visualization.PieChart(
      document.getElementById('piechart')
    );
    google.visualization.events.addListener(chart, 'ready', function () {
      if (options.pieStartAngle < 10) {
        options.pieStartAngle++;
        setTimeout(function () {
          chart.draw(data, options);
        }, 1);
      }
    });
    chart.draw(data, options);
  }
  $(window).resize(function () {
    drawChart();
  });
}
// Start Generate Compared
function generateComparedPortfolios(res) {
  let array = [];
  for (let [key, value] of Object.entries(res)) {
    if (
      key != 'id' &&
      key != 'name' &&
      key != 'company' &&
      key != 'fees' &&
      value != '0'
    ) {
      array.push([key, value]);
    }
  }

  let title = `${res.company} - ${res.name} ETF Allocation`;

  array.unshift(['ETF', 'Allocation']);

  google.load('visualization', '1', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(array);

    var options = {
      legend: {
        position: 'bottom',
        alignment: 'start',
        textStyle: { fontSize: 12 },
      },
      title: title,
      pieHole: 0.3,
      width: '100%',
      height: '100%',
      pieStartAngle: 100,
      is3D: false,
      animation: {
        duration: 1000,
        easing: 'in',
      },
    };

    var chart = new google.visualization.PieChart(
      document.getElementById('piechart-compare')
    );
    google.visualization.events.addListener(chart, 'ready', function () {
      if (options.pieStartAngle < 110) {
        options.pieStartAngle++;
        setTimeout(function () {
          chart.draw(data, options);
        }, 1);
      }
    });
    chart.draw(data, options);
  }
  $(window).resize(function () {
    drawChart();
  });
}
// End Generate Compared

let profile = $('#profile').text();
async function showInitialPortfolios() {
  const response = await axios.get(`${BASE_URL}/portfolios/${profile}`);

  let allocation = response.data.portfolio;

  generatePortfolios(allocation);
}

$(showInitialPortfolios);

// Show table

async function showETFs() {
  const res_port = await axios.get(`${BASE_URL}/portfolios/${profile}`);

  let res = res_port.data.portfolio;
  //read key

  populate(res);
}

$(showETFs);

var updateSlider = document.getElementById('update');
var updateSliderValue = document.getElementById('value');

noUiSlider.create(updateSlider, {
  start: [100000],
  behaviour: 'tap',
  step: 10000,
  range: {
    min: [0],
    '50%': [100000, 50000],
    max: [5000000],
  },

  format: wNumb({
    decimals: 0,
  }),
});

function populate(res) {
  $('#fees').empty();
  let array = [];
  for (let [key, value] of Object.entries(res)) {
    if (
      key != 'id' &&
      key != 'fees' &&
      key != 'name' &&
      key != 'desc' &&
      value != '0'
    ) {
      array.push(key);
    }
    if (key == 'desc') {
      $('#desc').append(`<p>${value}</p>`);
      console.log(value);
    }
    if (key == 'fees') {
      $('#fees').append(`
      
      <h4 class="float-left">Average Portfolio Fee: </h4>
      <h4 class="float-right" style="color:#00c5c8;"> ${(value * 100).toFixed(
        2
      )}%</h4>
      
      `);

      updateSlider.noUiSlider.on('update', function (values, handle) {
        $('#fee-dollars').empty();
        let newvalue = (updateSliderValue.innerHTML = values[handle]);

        $('#fee-dollars').append(`
        <h4 class="text-center"><span style="color: #00c5c8;">KIKEN</span> Portfolio</h4>
      <h5 class="text-center">$${value * parseInt(newvalue, 10)}</h5>
      `);
      });
    }
  }
  let users = [];
  let promises = [];
  for (i = 0; i < array.length; i++) {
    promises.push(
      axios
        .get(`${BASE_URL}/etfs/` + array[i].toUpperCase())
        .then((response) => {
          // do something with response
          users.push(response.data.etf);
        })
    );
  }
  let table = document.getElementById('portfolios');
  Promise.all(promises).then(() => {
    for (i = 0; i < users.length; i++) {
      $('#portfolios').append(
        `<tr><td>${users[i].symbol}</td><td>${users[i].name}</td><td>${
          users[i].category
        }</td><td>${(users[i].expense_ratio * 100).toFixed(2)}%</td></tr>`
      );
    }
  });
}

function populateCompared(res) {
  $('#compare-fee-dollars').empty();
  $('#compare-fees').empty();
  let array = [];

  for (let [key, value] of Object.entries(res)) {
    if (
      key != 'id' &&
      key != 'name' &&
      key != 'company' &&
      key != 'desc' &&
      key != 'fees' &&
      value != '0'
    ) {
      array.push(key);
    }

    if (key == 'fees') {
      $('#compare-fees').append(`
      
      <h4 class="float-left ">Average Portfolio Fee: </h4>
     <h4 class="float-right " style="color:#00c5c8;"> ${(value * 100).toFixed(
       2
     )}%</h4>
      `);
      updateSlider.noUiSlider.on('update', function (values, handle) {
        $('#compare-fee-dollars').empty();
        let newvalue = (updateSliderValue.innerHTML = values[handle]);

        $('#compare-fee-dollars').append(`
        <h4 class="text-center">Compared Portfolio</h4>
      <h5 class="text-center">$${value * parseInt(newvalue, 10)}</h5>
      `);
      });
    }
  }

  let users = [];
  let promises = [];
  for (i = 0; i < array.length; i++) {
    promises.push(
      axios
        .get(`${BASE_URL}/etfs/` + array[i].toUpperCase())
        .then((response) => {
          // do something with response
          users.push(response.data.etf);
        })
    );
  }
  // let table = document.getElementById('portfolios');
  Promise.all(promises).then(() => {
    $('#compair-portfolios').empty();
    for (i = 0; i < users.length; i++) {
      $('#compair-portfolios').append(
        `<tr><td>${users[i].symbol}</td><td>${users[i].name}</td><td>${
          users[i].category
        }</td><td>${(users[i].expense_ratio * 100).toFixed(2)}%</td></tr>`
      );
    }
    $('#compair-portfolios')[0].children;
  });
}

Formio.createForm(document.getElementById('formio'), {
  components: [
    {
      type: 'select',
      label: 'Compare Allocation Model',
      key: 'portfolio',
      placeholder: 'Select your model',
      dataSrc: 'url',
      data: {
        url: `${BASE_URL}/models`,
      },
      valueProperty: 'id',
      template: '<span>{{item.company}} - {{ item.name}}</span>',
      selectValues: 'models',
    },

    {
      type: 'button',
      action: 'submit',
      label: 'Compare',
      theme: 'primary',
      size: 'lg',
      block: false,
      disableOnInvalid: true,
    },
  ],
}).then(function (form) {
  form.on('submit', function (submission) {
    let model = submission.data.portfolio;

    async function showComparedPortfolios() {
      const response = await axios.get(`${BASE_URL}/models/${model}`);

      let allocation = response.data.models[0];

      generateComparedPortfolios(allocation);
    }

    $(showComparedPortfolios);

    // Show Compared Tables

    async function showComparedETFs() {
      const res_port = await axios.get(`${BASE_URL}/models/${model}`);

      let res = res_port.data.models[0];

      populateCompared(res);
    }

    $(showComparedETFs);
  });
});
