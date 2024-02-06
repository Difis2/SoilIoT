const userDisplay=document.getElementById('userDisplay');
const temperatureValue=document.getElementById('temperatureValue');
const soilHumidityValue=document.getElementById('soilHumidityValue');
const humidityValue=document.getElementById('humidityValue');


const fecthSqlData = async () =>{
fetch('http://localhost:5000/chartdata')
.then(response => response.json())
.then(data => {
  const dateParts = [];
  const timestamps = data.map(item => item.timestamp);
  for (const dateTimeString of timestamps) {
    const dateTime = new Date(dateTimeString);
    const datePart = `${dateTime.getMonth() + 1}/${dateTime.getDate()}`;
    dateParts.push(datePart);
  }
  const temperatures = data.map(item => item.temperature);
  const humidity = data.map(item => item.humidity);
  const soilHumidity = data.map(item => item.soil_humidity);
  const soilTemperature = data.map(item => item.soil_temperature);
  const n = data.map(item => item.n);
  const p = data.map(item => item.p);
  const k = data.map(item => item.k);
  const ctx1 = document.getElementById('temperatureChart').getContext('2d');
  const temperatureChart = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Temperature',
          data: temperatures,
          borderColor: 'yellow',
          fill: false,
        },
      ],
    },
  });
  
  const ctx2 = document.getElementById('humidityChart').getContext('2d');
  const humidityChart = new Chart(ctx2, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Humidity',
          data: humidity,
          borderColor: 'blue',
          fill: false,
        },
      ],
    },
  });
  
  const ctx3 = document.getElementById('soilHumidityChart').getContext('2d');
  const soilHumidityChart = new Chart(ctx3, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Soil Humidity',
          data: soilHumidity,
          borderColor: 'blue',
          fill: false,
        },
      ],
    },
  });
  const ctx4 = document.getElementById('soilTemperatureChart').getContext('2d');
  const soilTemperatureChart = new Chart(ctx4, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'soilTemperature',
          data: soilTemperature,
          borderColor: 'yellow',
          fill: false,
        },
      ],
    },
  });
  const ctx5 = document.getElementById('nChart').getContext('2d');
  const nChart = new Chart(ctx5, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Nitrogen',
          data: n,
          borderColor: 'green',
          fill: false,
        },
      ],
    },
  });
  const ctx6 = document.getElementById('pChart').getContext('2d');
  const pChart = new Chart(ctx6, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Phosphorus',
          data: p,
          borderColor: 'red',
          fill: false,
        },
      ],
    },
  });
  const ctx7 = document.getElementById('kChart').getContext('2d');
  const kChart = new Chart(ctx7, {
    type: 'line',
    data: {
      labels: dateParts,
      datasets: [
        {
          label: 'Potassium',
          data: k,
          borderColor: 'gray',
          fill: false,
        },
      ],
    },
  });
})
.catch(error => console.error('Error fetching chart data:', error));
}

const fetchMqttData = async () => {
    try {
        const response = await fetch('http://localhost:5000/mqttdata');
        if (!response.ok) {
            throw new Error('Failed to fetch MQTT data');
        }
        const data = await response.json();

        const temperature = data.temperature;
        const humidity = data.humidity;
        let soilHumidity = data.soil_humidity;
        const soilTemperature = data.soil_temperature;
        const n = data.n
        const p = data.p
        const k = data.k

        const nValue = n / (n + p + k) * 100
        const pValue = p / (n + p + k) * 100
        const kValue = k / (n + p + k) * 100


        document.getElementById('temperatureValue').innerText = temperature  + "ºC";
        document.getElementById('humidityValue').innerText = humidity  + "%";
        document.getElementById('soilHumidityValue').innerText = soilHumidity;
        document.getElementById('soilTemperatureValue').innerText = soilTemperature  + "ºC";
        document.getElementById('nValue').innerText = nValue === "NaN" ? nValue.toFixed(1) + "%" : 0 + "%";
        document.getElementById('pValue').innerText = pValue === "NaN" ? pValue.toFixed(1)  + "%" : 0 + "%";
        document.getElementById('kValue').innerText = kValue === "NaN" ? kValue.toFixed(1)  + "%" : 0 + "%";

        
        const airHumidityValue = 655;
        const watercupHumidityValue = 89;
        const intervals = (airHumidityValue-watercupHumidityValue)/3;
        let humidityText = "";
        let img;
        
        if(soilHumidity > watercupHumidityValue && soilHumidity < (watercupHumidityValue + intervals)){
          humidityText="Very Wet!"
          img="img/verywet.png"
        }
        else if(soilHumidity > (watercupHumidityValue + intervals) && soilHumidity < (airHumidityValue - intervals))
        {
          humidityText="It is Wet!";
          img="img/wet.png"
        }
        else if(soilHumidity < airHumidityValue && soilHumidity > (airHumidityValue - intervals))
        {
          humidityText="Time to Water!";
          img="img/dry.png"
        }


        document.getElementById('temperatureValue').innerText = temperature  + "ºC";
        document.getElementById('humidityValue').innerText = humidity  + "%";
        document.getElementById('soilHumidityValue').innerText = soilHumidity;
        document.getElementById('soilTemperatureValue').innerText = soilTemperature  + "ºC";
        document.getElementById('nValue').innerText = nValue === "NaN" ? nValue.toFixed(1) + "%" : 0 + "%";
        document.getElementById('pValue').innerText = pValue === "NaN" ? pValue.toFixed(1)  + "%" : 0 + "%";
        document.getElementById('kValue').innerText = kValue === "NaN" ? kValue.toFixed(1)  + "%" : 0 + "%";
        document.getElementById('humidityText').innerText = humidityText;
        document.getElementById('humidityImg').src = img;



        
    } catch (error) {
        console.error(error);
    }
};

const loggedInUser=localStorage.getItem('user');

userDisplay.textContent+=loggedInUser + '!';
fetchMqttData();
fecthSqlData();

document.addEventListener("DOMContentLoaded", function() {
  const contentContainer = document.getElementById("content-container");
  const navLinks = document.querySelectorAll(".navbar .navbar-nav .nav-link");

  navLinks.forEach(link => {
    link.addEventListener("click", function(event) {
      event.preventDefault();
      const targetSection = this.dataset.target;
      const selectedSection = document.getElementById(targetSection);

      document.querySelectorAll("section").forEach(section => {
        section.style.display = "none";
      });

      selectedSection.style.display = "block";
    });
  });
});

$(document).ready(function() {
  function showSection(section) {
    $(".nav-link").removeClass("active");
    $('[data-target="' + section + '"]').addClass("active");
    $("section").hide();
    $("#" + section).show();
  }

  showSection("section1");

  $(".nav-link").click(function(event) {
    event.preventDefault();
    var target = $(this).data("target");
    showSection(target);
  });
});

setTimeout(function () {
  window.dispatchEvent(new Event('resize'));
}, 3000);


if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function(position) {
    const lat = 38.917729;
    const lon = -8.675921;
    var map = L.map('map').setView([lat, lon], 17);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    }).addTo(map);
    var marker = L.marker([lat, lon]).addTo(map);

    var circle = L.circle([lat, lon], {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5,
      radius: 10
    }).addTo(map);
  });
} else {
  console.log("Geolocation is not supported by this browser.");
}
