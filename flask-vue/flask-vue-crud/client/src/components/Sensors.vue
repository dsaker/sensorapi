<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Sensors</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.sensor-modal>
          Add Sensor
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Temperature</th>
              <th scope="col">Humidity</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="(sensor, index) in sensors" :key="index">
              <td>{{ sensor.name }}</td>
              <td>{{ sensor.temperature }}</td>
              <td>{{ sensor.humidity }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.sensor-update-modal
                          @click="editsensor(sensor)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeletesensor(sensor)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addSensorModal"
        id="sensor-modal"
        name="Add a new sensor"
        hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                      label="Name:"
                      label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addSensorForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-temperature-group"
                      label="Temperature:"
                      label-for="form-temperature-input">
          <b-form-input id="form-temperature-input"
                        type="text"
                        v-model="addSensorForm.temperature"
                        required
                        placeholder="Enter temperature">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-humidity-group"
                      label="Humidity:"
                      label-for="form-humidity-input">
          <b-form-input id="form-humidity-input"
                        type="text"
                        v-model="addSensorForm.humidity"
                        required
                        placeholder="Enter humidity">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      sensors: [],
      addSensorForm: {
        name: '',
        temperature: '',
        humidity: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        temperature: '',
        humidity: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getSensors() {
      const path = 'http://localhost:5000/sensors';
      axios.get(path)
        .then((res) => {
          this.sensors = res.data.sensors;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addSensor(payload) {
      const path = 'http://localhost:5000/sensors';
      axios.post(path, payload)
        .then(() => {
          this.getSensors();
          this.message = 'Sensor added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSensors();
        });
    },
    initForm() {
      this.addSensorForm.name = '';
      this.addSensorForm.temperature = '';
      this.addSensorForm.humidity = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.temperature = '';
      this.editForm.humidity = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSensorModal.hide();
      const payload = {
        name: this.addSensorForm.name,
        temperature: this.addSensorForm.temperature,
        humidity: this.addSensorForm.humidity,
      };
      this.addSensor(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addSensorModal.hide();
      this.initForm();
    },
    editSensor(sensor) {
      this.editForm = sensor;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSensorModal.hide();
      const payload = {
        name: this.editForm.name,
        temperature: this.editForm.temperature,
        humidity: this.editForm.humidity,
      };
      this.updateSensor(payload, this.editForm.id);
    },
    updateSensor(payload, sensorID) {
      const path = `http://localhost:5000/sensors/${sensorID}`;
      axios.put(path, payload)
        .then(() => {
          this.getSensors();
          this.message = 'Sensor updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSensors();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSensorModal.hide();
      this.initForm();
      this.getSensors(); // why?
    },
    removeSensor(sensorID) {
      const path = `http://localhost:5000/sensors/${sensorID}`;
      axios.delete(path)
        .then(() => {
          this.getSensors();
          this.message = 'Sensor removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSensors();
        });
    },
    onDeleteSensor(sensor) {
      this.removeSensor(sensor.id);
    },
  },
  created() {
    this.getSensors();
  },
};
</script>
