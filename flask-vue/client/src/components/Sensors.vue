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
              <th scope="col">High Temp Alert</th>
              <th scope="col">Low Temp Alert</th>
              <th scope="col">High Humidity Alert</th>
              <th scope="col">Low Humidity Alert</th>
              <th scope="col">Temp Alert On</th>
              <th scope="col">Humidity Alert on</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="(sensor, index) in sensors" :key="index">
              <td>{{ sensor.name }}</td>
              <td>{{ sensor.HTAlert }}</td>
              <td>{{ sensor.LTAlert }}</td>
              <td>{{ sensor.HHAlert }}</td>
              <td>{{ sensor.LHAlert }}</td>
              <td>
                <span v-if='sensor.TempAlertOn'>On</span>
                <span v-else>Off</span>
              </td>
              <td>
                <span v-if='sensor.HumAlertOn'>On</span>
                <span v-else>Off</span>
              </td>
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
        <b-form-group id="form-HTAlert-group"
                      label="High Temperature Alert:"
                      label-for="form-HTAlert-input">
          <b-form-input id="form-HTAlert-input"
                        type="range"
                        min = "0"
                        max= "100"
                        v-model="addSensorForm.HTAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  addSensorForm.HTAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-LTAlert-group"
                      label="Low Temperature Alert:"
                      label-for="form-LTAlert-input">
          <b-form-input id="form-LTAlert-input"
                        type="range"
                        min = "0"
                        max= "100"
                        v-model="addSensorForm.LTAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  addSensorForm.LTAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-HHAlert-group"
                      label="High Humidity Alert Set:"
                      label-for="form-HHAlert-input">
          <b-form-input id="form-HHAlert-input"
                        type="range"
                        min = "0"
                        max = "100"
                        v-model="addSensorForm.HHAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  addSensorForm.HHAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-LHAlert-group"
                      label="Low Humidity Alert:"
                      label-for="form-LHAlert-input">
          <b-form-input id="form-LHAlert-input"
                        type="range"
                        min = "0"
                        max ="100"
                        v-model="addSensorForm.LHAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  addSensorForm.LHAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-TempAlertOn-group">
          <b-form-checkbox-group v-model="addSensorForm.TempAlertOn" id="form-checks">
            <b-form-checkbox value="true">On?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group id="form-HumAlertOn-group">
          <b-form-checkbox-group v-model="addSensorForm.HumAlertOn" id="form-checks">
            <b-form-checkbox value="true">On?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
        <b-modal ref="editSensorModal"
        id="sensor-update-modal"
        name="Update"
        hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-HTAlert-edit-group"
                      label="High Temperature Alert:"
                      label-for="form-HTAlert-edit-input">
          <b-form-input id="form-HTAlert-edit-input"
                        type="range"
                        min = "0"
                        max ="100"
                        v-model="editForm.HTAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  editForm.HTAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-LTAlert-edit-group"
                      label="Low Temperature Alert:"
                      label-for="form-LTAlert-edit-input">
          <b-form-input id="form-LTAlert-edit-input"
                        type="range"
                        min = "0"
                        max="100" step="0.5"
                        v-model="editForm.LTAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  editForm.LTAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-HHAlert-edit-group"
                      label="High Humidity Alert Set:"
                      label-for="form-HHAlert-edit-input">
          <b-form-input id="form-HHAlert-edit-input"
                        type="range"
                        min = "0"
                        max="100" step="0.5"
                        v-model="editForm.HHAlert"
                        required>
          </b-form-input>
          <div class="mt-2">Value: {{  editForm.HHAlert  }}</div>
        </b-form-group>
        <b-form-group id="form-LHAlert-edit-group"
                      label="Low Humidity Alert:"
                      label-for="form-LHAlert-edit-input">
          <b-form-input id="form-LHAlert-edit-input"
                        type="range"
                        min = "0"
                        max="100" step="0.5"
                        v-model="editForm.LHAlert"
                        required>
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-TempAlertOn-edit-group">
          <b-form-checkbox-group v-model="editForm.TempAlertOn" id="form-checks">
            <b-form-checkbox value="true">On?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group id="form-HumAlertOn-edit-group">
          <b-form-checkbox-group v-model="editForm.HumAlertOn" id="form-checks">
            <b-form-checkbox value="true">On?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
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
      this.addSensorForm.HTAlert = 90;
      this.addSensorForm.LTAlert = 50;
      this.addSensorForm.HHAlert = 80;
      this.addSensorForm.LHAlert = 30;
      this.addSensorForm.TempAlertOn = [];
      this.addSensorForm.HumAlertOn = [];
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.HTAlert = 90;
      this.editForm.LTAlert = 50;
      this.editForm.HHAlert = 80;
      this.editForm.LHAlert = 30;
      this.editForm.TempAlertOn = [];
      this.editForm.HumAlertOn = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSensorModal.hide();
      let TempAlertOn = false;
      if (this.addSensorForm.TempAlertOn[0]) TempAlertOn = true;
      let HumAlertOn = false;
      if (this.addSensorForm.HumAlertOn[0]) HumAlertOn = true;
      const payload = {
        name: this.addSensorForm.name,
        HTAlert: this.addSensorForm.HTAlert,
        LTAlert: this.addSensorForm.LTAlert,
        HHAlert: this.addSensorForm.HHAlert,
        LHAlert: this.addSensorForm.LHAlert,
        TempAlertOn,
        HumAlertOn,
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
      let TempAlertOn = false;
      if (this.addSensorForm.TempAlertOn[0]) TempAlertOn = true;
      let HumAlertOn = false;
      if (this.addSensorForm.HumAlertOn[0]) HumAlertOn = true;
      const payload = {
        name: this.editForm.name,
        HTAlert: this.editForm.HTAlert,
        LTAlert: this.editForm.LTAlert,
        HHAlert: this.editForm.HHAlert,
        LHAlert: this.editForm.LHAlert,
        TempAlertOn,
        HumAlertOn,
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
