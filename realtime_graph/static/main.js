let ctx1 = document.querySelector("#myChart1")
let ctx2 = document.querySelector("#myChart2")
let ctx3 = document.querySelector("#myChart3")
const ctxs = [ctx3, ctx1, ctx2]
ctxs.forEach((ctx) => {
    const data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [{
            label: 'График говна',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };
    let graphData = {
        type: "line",
        data: data
    }
    let myChart = new Chart(ctx, graphData)


    let socket = new WebSocket("ws://localhost/ws/graph")

    let logsPlace = document.querySelector("#logs");

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Логируем полученные данные
        console.log("Received data:", data);

        // Проверяем наличие массива logs в данных
        if (data.logs && Array.isArray(data.logs)) {
            // Очистим контейнер перед добавлением новых логов
            logsPlace.innerHTML = '';

            data.logs.forEach((log) => {
                logsPlace.insertAdjacentHTML('beforeend', `<div>Value: ${log.value}, Day: ${log.day}</div>`);
            });
        } else {
            console.log("Logs not found in data.");
        }

        // Обновляем график и текст, как и раньше
        const newGraphData = graphData.data.datasets[0].data;
        newGraphData.shift();
        newGraphData.push(data.value);

        const newGraphDays = graphData.data.labels;
        newGraphDays.shift();
        newGraphDays.push(data.day);

        graphData.data.labels = newGraphDays;
        graphData.data.datasets[0].data = newGraphData;

        myChart.update();
        document.querySelector("#app").innerText = data.edits;
    };
})


