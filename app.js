var SerialPort = require('serialport');
const parsers = SerialPort.parsers;
const parser = new parsers.Readline({
  delimiter: '\r\n',
});

var port = new SerialPort('COM8', {
  baudRate: 9600,
  dateBits: 8,
  parity: 'none',
  stopBits: 1,
  flowControl: false,
});

port.pipe(parser);

parser.on('data', function (data) {
  console.log(data);
});
