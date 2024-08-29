<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <router-link to="/my_groups" class="router-link"> 我的群組</router-link>
      </div>
      <h1>分帳結餘</h1>
      <p>分帳邏輯: 最大欠款者先付給最大應收者</p>
      <div class="line"></div>
    </div>
    <div class="container">
      <div class="list-container">
        <ul class="ul">
          <!-- data from getTheSettlement() -->
          <li
            class="list"
            v-for="receiver in summary"
            :key="receiver.receiver_name"
          >
            <div class="list-rows">
              <div class="list-row1">
                <div class="list-item" id="receiver">
                  {{ receiver.receiver_name }}
                </div>
                <div class="list-item">應收</div>
              </div>
              <div
                class="list-row2"
                v-for="debtor in receiver.debtors"
                :key="debtor.debtor_id"
              >
                <div class="list-item" id="debtor">
                  {{ debtor.debtor_name }}
                </div>
                <div class="list-item" id="debtor-amount">
                  ${{ debtor.amount }}
                </div>
              </div>
              <div class="list-row3">
                <div class="list-item" id="total_receivable">
                  總計 ${{ receiver.total_receivable }}
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="button-container">
        <button type="button" class="button" @click="goBack">上一頁</button>
        <button type="button" class="button" @click="reconcile">驗算</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SettleTheBalance",
  // props form NewGroup
  props: ["group_id"],

  data() {
    return {
      // props from NewGroup
      localGroupID: this.$route.params.group_id,
      localExpenseID: this.$route.params.expense_id,
      summary: [],
    };
  },
  mounted() {
    this.getTheSettlement();
  },
  methods: {
    getTheSettlement() {
      axios
        .get(
          `http://localhost:5000/group/${this.localGroupID}/settle_the_balance`
        )
        .then((res) => {
          this.summary = res.data.summary;
          console.log("getTheSettlement Data:", res.data);
        })
        .catch((err) => {
          console.log("getTheSettlement Error", err);
        });
    },
    goBack() {
      this.$router.go(-1);
    },
    reconcile() {
      this.$router.push({
        name: "Reconciliation",
        group_id: this.localGroupID,
      });
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  /* box-sizing: border-box; */
  /* border: 1px solid #000; */
}

.list-container {
  width: 90%;
  margin-top: -10px;
  /* border: 1px solid #000; */
}

ul {
  padding: 0;
  margin: 0;
  /* width: 100%; */
  text-align: center;
  /* border: 1px solid #000; */
}

.list {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #d9edfc;
  border-radius: 5px;
  /* border: 1px solid #000; */
}

/* .list-item {border: 1px solid #000;} */

.list-rows {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.list-row1 {
  display: flex;
  flex-direction: row;
  padding: 5px 0;
  justify-content: space-between;
  font-size: 18px;
  font-weight: bold;
  /* border: 1px solid #000; */
}

.list-row2 {
  display: flex;
  flex-direction: row;
  padding: 5px 0;
  justify-content: space-between;
  font-size: 14px;
  /* border: 1px solid #000; */
}

.list-row3 {
  display: flex;
  flex-direction: row;
  padding: 5px 0;
  justify-content: flex-end;
  font-size: 20px;
  font-weight: bold;
  /* border: 1px solid #000; */
}

.button-container {
  width: 80%;
  /* border: 1px solid #000; */
}

.note-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  /* border: 1px solid #000; */
  padding: 0 10px;
}

.note-colum {
  display: flex;
  flex-direction: row;
  width: 33%;
  /* border: 1px solid #000; */
}

.note {
  flex: 1;
  /* border: 1px solid #000; */
}

.button.add-user {
  height: 30px;
  width: 30px;
  border-radius: 50%;
  margin-left: 20px;
  /* border: 1px solid #000; */
}

.left-align {
  margin-top: 15px;
  margin-bottom: 5px;
  text-align: left;
}

.input {
  width: 100%;
  height: 20px;
}
</style>
