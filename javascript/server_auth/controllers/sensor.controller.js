let Sensor = require('../models/post.model')
let errorHandler = require('../helpers/dbErrorHandler')
let fs = require('fs')

const create = (req, res) => {
  const sensor = new Sensor(req.body)
  try {
    await sensor.save()
    return res.status(200).json({
      message: "New sensor created",
      data: sensor
    })
  } catch (err) {
    return res.status(400).json({
      error: errorHandler.getErrorMessage(err)
    })
  }
}

const sensorByID = async (req, res, id) => {
  try{
    let sensor = await Sensor.findById(id)
    if (!sensor) {
      return res.status('400').json({
        error: "Sensor not found"
      })
    }
    else {
      return res.status(200).json({
        message: "Loading sensor data ...",
        data: sensor
      })
    }
  } catch(err){
    return res.status('400').json({
      error: errorHandler.getErrorMessage(err)
    })
  }
}

const list = async (req, res) => {
  try {
    let sensors = await Sensor.find()
    res.json(sensors)
  } catch (err) {
    return res.status(400).json({
      error: errorHandler.getErrorMessage(err)
    })
  }
}

const update = (req, res) => {
  let sensor = req.profile
  sensor.update = Date.now()
  try {
    await sensor.save()
    sensor.filename = undefined
    res.json(sensor)
  } catch(err){
    return res.status('400').json({
      error: errorHandler.getErrorMessage(err)
    })
  }
}  

const remove = async (req, res) => {
  try{
    let sensor = req.profile
    let deletedSensor = await sensor.remove()
    res.json(deletedSensor)
  }catch(err){
    return res.status(400).json({
      error: errorHandler.getErrorMessage(err)
    })
  }
}

module.exports = {
  list,
  create,
  remove,
  update,
  sensorByID
}