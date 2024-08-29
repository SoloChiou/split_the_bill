<template>
  <div class="wrapper">
    <div class="header">
      <h1>編輯花費</h1>
      <div class="line"></div>
    </div>
    <div class="container">
      <p class="left-align">項目</p>
      <input class="input" v-model="localExpenseItem" />

      <p class="left-align">金額</p>
      <input class="input" v-model="localExpenseAmount" />

      <p class="left-align">付款人</p>
      <select class="input" v-model="localExpensePayer">
        <!-- data from getGroupUsers() -->
        <option v-for="user in users" :key="user.id" :value="user.name">
          <!-- 綁定的是value -->
          {{ user.name }}
        </option>
      </select>
      <p class="left-align">分款人</p>
      <select
        class="input"
        v-model="localSplitters"
        multiple
        :style="{ height: '100px' }"
      >
        <option v-for="user in users" :key="user.id" :value="user.name">
          {{ user.name }}
        </option>
      </select>
      <div class="button-container">
        <button type="button" class="button" @click="goBack">上一頁</button>
        <button type="submit" class="button" @click="updateExpense">
          更新花費
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateExpense",
  //   props from NewGroup.vue
  props: [
    "group_id",
    "expense_id",
    "expenseItem",
    "expenseAmount",
    "expensePayerID",
    "expensePayer",
  ],

  data() {
    return {
      localGroupID: this.$route.params.group_id,
      localExpenseID: this.$route.params.expense_id,
      localExpenseItem: this.$route.params.expenseItem,
      localExpenseAmount: this.$route.params.expenseAmount,
      localPayerID: this.$route.params.expensePayerID,
      localExpensePayer: this.$route.params.expensePayer,
      localSplitters: [],
      users: [],
    };
  },
  mounted() {
    this.getGroupUsers(this.localGroupID);
    this.getLocalSplitters(this.localExpenseID);
  },
  methods: {
    getGroupUsers() {
      // 取得付款人&分款人
      axios
        .get(`http://localhost:5000/group/${this.localGroupID}/users`)
        .then((res) => {
          this.users = res.data;
          console.log("gerGroupUsers", this.users);
        })
        .catch((err) => {
          console.log("getGroupUsers Error", err);
        });
    },
    getLocalSplitters() {
      axios
        .get(`http://localhost:5000/expenses/${this.localExpenseID}/splitters`)
        .then((res) => {
          this.localSplitters = res.data;
          console.log("getLocalSplitters Data:", this.localSplitters);
        });
    },
    goBack() {
      this.$router.go(-1);
    },
    updateExpense() {
      const payload = {
        item: this.localExpenseItem,
        amount: this.localExpenseAmount,
        payer_id: this.localPayerID,
        payer: this.localExpensePayer,
        splitters: this.localSplitters,
      };
      console.log("Payload: ", payload);
      axios
        .put(
          `http://localhost:5000/expenses/${this.localExpenseID}/update_expense`,
          payload
        )
        .then((res) => {
          console.log("updateExpense Data: ", res.data);
          this.$router.push({ name: "NewGroup" });
        });
    },
  },
};
</script>

<style scoped>
.container {
  width: 50%;
  margin: 0 auto;
}

.button {
  margin-top: 30px;
}

.left-align {
  margin-top: 15px;
  margin-bottom: 5px;
  text-align: left;
}

.input {
  width: 100%;
  height: 25px;
}
</style>
