<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <router-link to="/my_groups" class="router-link"> 我的群組</router-link>
      </div>
      <h1>驗算</h1>
      <p>對分帳有疑慮嗎? 這邊驗算給你看!</p>
      <div class="line"></div>
    </div>
    <div class="container">
      <div class="steps">
        <div class="step-container">
          <h3>1. 每人債務統計表</h3>
          <div>
            <table class="expense-table">
              <thead>
                <tr>
                  <th class="item-header">項目\成員</th>
                  <!-- v-for="(value, key)" -->
                  <!-- 標題欄: 成員名稱 -->
                  <th
                    v-for="(expenses, userName) in expensesByUser"
                    :key="userName"
                  >
                    {{ userName }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <!-- 項目欄 -->
                <tr v-for="item in items" :key="item.expense_id">
                  <td class="item-header">
                    {{ item.expense_item }}
                  </td>
                  <td
                    class="amount"
                    v-for="(expenses, userName) in expensesByUser"
                    :key="userName"
                  >
                    <!-- 使用者的每筆花費填入條件篩選: 符合item-header的id -->
                    <div
                      v-for="expense in expenses"
                      :key="expense.expense_id"
                      class="amount-per-user"
                    >
                      <span v-if="expense.expense_id === item.expense_id">{{
                        expense.expense
                      }}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="item-header total">總計</td>
                  <td
                    class="total-per-user"
                    v-for="(totalExpenses, userName) in totalExpensesByUser"
                    :key="userName"
                  >
                    {{ totalExpenses }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="step-container">
          <h3>2. 清算</h3>
          <p class="step2-content">最大欠款者先付給最大應收者, 依此類推</p>
          <ul>
            <!-- `${step.receiver_id} - ${step.debtor_id}`動態綁定key, 因為每個step的應收者欠款者id不同 -->
            <ol type="1">
              <li
                class="list"
                v-for="step in settlementSteps"
                :key="`${step.receiver_id} - ${step.debtor_id}`"
              >
                {{ step.receiver_name }} 跟 {{ step.debtor_name }} 收 $
                {{ step.amount }}
              </li>
            </ol>
          </ul>
        </div>
        <div class="button-container">
          <button type="button" class="button" @click="goBack">上一頁</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Reconciliation",
  // props from SettleTheBalance
  props: ["group_id"],

  data() {
    return {
      localGroupID: this.$route.params.group_id,
      expensesByUser: {},
      totalExpensesByUser: {},
      items: [],
      settlementSteps: [],
    };
  },
  mounted() {
    this.reconciliation();
    this.getSettlementSteps();
  },
  methods: {
    reconciliation() {
      axios
        .get(
          `http://localhost:5000/group/${this.localGroupID}/expenses/settle_the_balance/reconciliation`
        )
        .then((res) => {
          this.expensesByUser = res.data.expenses_by_user;
          this.totalExpensesByUser = res.data.total_expenses_by_user;
          this.items = res.data.items;
          console.log(
            "reconciliation Data(expensesByUser):",
            this.expensesByUser
          );
          console.log(
            "reconciliation Data:(totalExpensesByUser)",
            this.totalExpensesByUser
          );
          console.log("reconciliation Data:(items)", this.items);
        })
        .catch((err) => {
          console.log("reconciliation Error", err);
        });
    },
    goBack() {
      this.$router.go(-1);
    },
    getSettlementSteps() {
      axios
        .get(
          `http://localhost:5000/group/${this.localGroupID}/settle_the_balance`
        )
        .then((res) => {
          this.settlementSteps = res.data.settlement_steps;
          console.log("settlementSteps:", this.settlementSteps);
        });
    },
  },
};
</script>

<style scoped>
/* .container { */
/* position: relative; */
/* border: 1px solid #000; */
/* } */

.steps {
  width: 90%;
  /* margin-top: -10px; */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* border: 1px solid #000; */
}

.step-container {
  width: 100%;
  margin-bottom: 20px;
  /* border: 1px solid #000; */
}

h3 {
  text-align: left;
  margin-top: 10px;
  margin-bottom: 10px;
  /* border: 1px solid #000; */
}

.step2-content {
  text-align: left;
  margin-top: 0;
}

.expense-table {
  width: 100%;
  /* 合併表格邊框 */
  border-collapse: collapse;
  /* border: 1px solid #000; */
}

.expense-table th,
.expense-table td {
  border: 1px solid #d3d3d3;
  padding: 8px;
}

.item-header {
  text-align: left;
}

.item-header.total {
  font-weight: bold;
  background-color: #e5f3ff;
}

.amount-per-user {
  text-align: right;
}

.total-per-user {
  font-weight: bold;
  text-align: right;
  background-color: #e5f3ff;
}

.button-container {
  position: fixed;
  bottom: 0;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  width: 100%;
  padding: 20px 0;
  background-color: #fff;
  /* border: 1px solid #000; */
}

ul {
  /* 解決li靠單邊問題 */
  padding: 0;
  /* border: 1px solid #000; */
}

.list {
  text-align: left;
  /* border: 1px solid #000; */
}
</style>
