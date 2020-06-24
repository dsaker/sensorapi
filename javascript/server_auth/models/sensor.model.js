let mongoose = require('mongoose')

const SensorSchema = new mongoose.Schema({
  name: {
    type: String,
    trim: true,
    required: 'Name is required'
  },
  filename: {
    type: String,
    trim: true,
    required: 'Filename is required'
  },
  created: {
    type: Date,
    default: Date.now
  },
  Geolocation: {
    type: {
      type: String,
      enum: ['Point'],
    },
    coordinates: {
      type: [Number]
    }
  },
  updated: Date,
  highTempAlert: Number,
  lowTempAlert: Number,
  HighHumidityAlert: Number,
  LowHumidityAlert: Number
})

module.exports =  mongoose.model('Sensor', SensorSchema)