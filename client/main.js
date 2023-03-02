const socket = new WebSocket("ws://localhost:8080");

const times = [];
const values = [];
const VALUES_MAX_LENGTH = 10;


socket.addEventListener("open", function (event) {
    console.log("ws open");
});

socket.addEventListener("message", function (event) {
    console.log("received ", event.data);
    data = JSON.parse(event.data);
    const value = data["v"];
    const time = new Date(data["t"] * 1000).toISOString();

    // keep 10 most recent values
    if (values.length >= VALUES_MAX_LENGTH) {
        values.shift();
        times.shift();
    }
    values.push(value);
    times.push(time);

    // update view
    for (const i in values) {
        document.querySelector("#value-"+i).innerHTML = values[i];
        document.querySelector("#time-"+i).innerHTML = times[i];
    }
});

socket.addEventListener("close", function (event) {
    console.log("ws closed");
});

const sendMessage = function (message) {
    if (socket.readyState === 1) {
        console.log("send message", message);
        socket.send(JSON.stringify(message));
    }
}
