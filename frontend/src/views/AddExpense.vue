<template>
  <div class="wrapper">
    <div class="header">
      <h1>新增花費</h1>
      <div class="line"></div>
    </div>
    <div class="container">
      <p class="left-align">項目</p>
      <input class="input" v-model="localItem" />
      <p class="left-align">金額</p>
      <input class="input" v-model="localAmount" />
      <p class="left-align">付款人</p>
      <select class="input" v-model="localPayer">
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
        :style="{ height: '80px' }"
      >
        <option v-for="user in users" :key="user.id" :value="user.name">
          {{ user.name }}
        </option>
      </select>
      <div class="button-container">
        <button type="button" class="button" @click="goBack">上一頁</button>

        <button type="submit" class="button" @click="addExpense">
          新增花費
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddExpense",
  // props from NewGroup
  props: ["group_id"],
  // 使用 data 屬性來存儲 props 的值，這樣避免直接修改 props, props 是只讀的，應該保持不變。
  data() {
    return {
      localID: "",
      localItem: "",
      localAmount: "",
      localPayer: "",
      localSplitters: [],
      // 從NewGroup的redirectToAddExpense()參數中獲取group_id
      localGroupID: this.$route.params.group_id,
      users: [],
    };
  },
  mounted() {
    console.log("addExpense get groupID:", this.localGroupID);
    this.getGroupUsers(this.localGroupID);
  },
  methods: {
    getGroupUsers() {
      // 取得付款人&分款人
      axios
        .get(`http://localhost:5000/group/${this.localGroupID}/users`)
        .then((res) => {
          this.users = res.data;
        })
        .catch((err) => {
          console.log("getGroupUsers Error", err);
        });
    },
    addExpense() {
      console.log("addExpense Submitting data:", {
        item: this.localItem,
        amount: this.localAmount,
        payer: this.localPayer,
        splitters: this.localSplitters,
        group_id: this.localGroupID,
      });
      axios
        .post(`http://localhost:5000/group/${this.localGroupID}/add_expense`, {
          item: this.localItem,
          amount: this.localAmount,
          payer: this.localPayer,
          splitters: this.localSplitters,
          group_id: this.localGroupID,
        })
        .then((res) => {
          console.log("Expense submitted", res.data);
          this.redirectToGroup();
        })
        .catch((err) => {
          console.log("addExpense Error", err);
        });
    },
    redirectToGroup() {
      // 新增花費後返回群組
      this.$router.push(`/group/${this.localGroupID}`);
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container {
  width: 50%;
}

.inline-block-container {
  position: relative;
  /* bottom: -300px; */
  width: 100%;
  text-align: center;
  z-index: 1000;
}

.button {
  margin-top: 30px;
}

.left-align {
  margin-top: 15px;
  margin-bottom: 5px;
  text-align: left;
}

.line {
  display: block;
  position: relative;
  width: 90%;
  height: 1px;
  margin: 0 auto;
  top: 0px;
  background: #71acdc;
  text-align: center;
}

.input {
  width: 100%;
  height: 25px;
}
</style>
