<template>
  <div class="container">
    <table>
      <thead>
      <tr>
        <th>类型</th>
        <th>号码</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item, index) in probabilityData" :key="index">
        <td>{{ Object.keys(item)[0] }}</td>
        <td>{{ Object.values(item)[0] }}</td>
        <td><button @click="showDetail(Object.keys(item)[0])">详情</button></td>
      </tr>
      </tbody>
    </table>
    <div v-if="isDialogVisible" class="backdrop" @click="isDialogVisible = false"></div>
    <div v-if="isDialogVisible" class="dialog">
      <div class="dialog-header">
        <span class="dialog-title">详情</span>
        <span class="dialog-close" @click="isDialogVisible = false">×</span>
      </div>
      <div class="dialog-content" ref="dialogContent">
        <div v-for="(items, key) in detailData" :key="key">
          <h4>{{ key }}</h4>
          <ul>
            <li v-for="item in items" :key="item.number">{{ item.number }}: {{ item.probability }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SimpleBar from 'simplebar';
import 'simplebar/dist/simplebar.css';
import { BASE_URL } from '../config';

export default {
  data() {
    return {
      probabilityData: [],
      detailData: {},
      isDialogVisible: false,
    };
  },
  mounted() {
    this.fetchprobabilityData();
  },
  methods: {
    async fetchprobabilityData() {
      try {
        const response = await axios.get(`${BASE_URL}/probability_numbers`);
        this.probabilityData = response.data.numbers;
      } catch (error) {
        console.error('Error fetching probability data:', error);
      }
    },
    async showDetail(type) {
      const typeMap = {
        '全量': 0,
        '50': 50,
        '100': 100,
        '200': 200,
        '300': 300,
        '400': 400,
        '500': 500,
      };
      const count = typeMap[type] || 0; // 默认全量
      try {
        const response = await axios.get(`${BASE_URL}/probability_detail`, { params: { count } });
        this.detailData = response.data.detail;
        this.isDialogVisible = true;
        this.$nextTick(() => {
          new SimpleBar(this.$refs.dialogContent);
        });
      } catch (error) {
        console.error('Error fetching detail data:', error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 0 10%; /* 按比例缩小留白 */
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto; /* 居中表格 */
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #d9ead3; /* Excel-like green */
}

button {
  padding: 6px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 20%; /* 调整宽度，可以根据需要调整 */
  max-height: 80%;
  overflow: hidden;
  z-index: 1001;
  padding: 1%; /* 调整padding，减少留白 */
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
}

.dialog-title {
  font-size: 1.2em;
  font-weight: bold;
}

.dialog-close {
  cursor: pointer;
  font-size: 1.5em;
}

.dialog-content {
  padding: 10px; /* 减少留白 */
  max-height: calc(70vh - 60px); /* Adjusted for header height */
  overflow-y: auto;
  text-align: left;
}

.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}
</style>
