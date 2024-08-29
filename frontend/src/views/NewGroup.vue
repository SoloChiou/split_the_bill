<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <router-link to="/my_groups" class="router-link"> 我的群組</router-link>
        <p class="router-link" :style="{ display: 'inline-block' }">|</p>
        <router-link
          :to="{
            name: 'UpdateGroup',
            params: {
              group_id: this.localGroupID,
              groupName: this.localGroupName,
              groupNote: this.localGroupNote,
            },
          }"
          class="router-link"
          >編輯群組</router-link
        >
      </div>
      <h1>{{ localGroupName }}</h1>
      <div class="note-container">
        <div class="note-colum">
          <button
            type="button"
            class="button edit-users"
            @click="redirectToUsers(users)"
          ></button>
        </div>
        <div class="note-colum">
          <p class="note">{{ localGroupNote }}</p>
        </div>
        <div class="note-colum"></div>
      </div>
      <div class="line"></div>
    </div>
    <div class="container">
      <div class="list-container" v-if="expenses.length">
        <h3>花費列表</h3>
        <ul>
          <!-- data from getGroupExpenses() -->
          <li class="list" v-for="expense in expenses" :key="expense.id">
            <div
              class="list-rows"
              @click="
                redirectToExpense(
                  expense.id,
                  expense.item,
                  expense.amount,
                  expense.payer_id,
                  expense.payer
                )
              "
            >
              <!-- stop防止功能向上層連動 -->
              <button
                class="button delete-expense"
                @click.stop="deleteExpense(expense.id)"
              >
                x
              </button>
              <div class="list-row1">
                <div class="list-item">
                  {{ expense.item }}
                </div>
                <div class="list-item">${{ expense.amount }}</div>
              </div>
              <div class="list-row2">
                <div class="list-item">{{ expense.payer }} 付款</div>

                <div class="list-item">{{ expense.splitter_count }}人分</div>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="button-container">
        <button type="button" class="button" @click="redirectToAddExpense">
          新增花費
        </button>
        <button type="button" class="button" @click="settleTheBalance">
          分帳結餘
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NewGroup",
  // props from AddUsers
  props: ["group_id", "groupName", "groupNote"],

  // 使用 data 屬性來存儲 props 的值，這樣避免直接修改 props
  data() {
    return {
      localGroupID: this.$route.params.group_id,
      localGroupName: this.$route.params.groupName,
      localGroupNote: this.$route.params.groupNote,
      expenses: [],
      users: [],
    };
  },
  // 當頁面轉跳置此時, 要自動調用的數據或方法
  mounted() {
    this.getGroup(this.localGroupID);
    this.getGroupExpenses(this.localGroupID);
    this.getGroupUsers(this.localGroupID);
    console.log("NewGroup get Group ID:", this.localGroupID);
  },
  methods: {
    getGroup() {
      axios
        .get(`http://localhost:5000/group/${this.localGroupID}`)
        .then((res) => {
          console.log("Group data", res.data);
          this.localGroupName = res.data.groupName;
          this.localGroupNote = res.data.groupNote;
        })
        .catch((err) => {
          console.log("getGroup Error", err);
        });
    },
    redirectToAddExpense() {
      // 讓新增的花費綁定當前Group
      this.$router.push({
        name: "AddExpense",
        params: {
          group_id: this.localGroupID,
          // expense_id: this.
        },
      });
    },
    getGroupExpenses() {
      // 顯示花費列表
      axios
        .get(`http://localhost:5000/group/${this.localGroupID}/expenses`)
        .then((res) => {
          // res.data 是用來存儲從後端獲取的響應數據
          this.expenses = res.data;
          console.log("getGroupExpense Data:", this.expenses);
        })
        .catch((err) => {
          console.log("getGroupExpenses Error", err);
        });
    },
    settleTheBalance() {
      // 分帳結餘
      axios
        .post(
          `http://localhost:5000/group/${this.localGroupID}/settle_the_balance`
        )
        .then((res) => {
          console.log("Settle Data:", res.data);
          this.redirectToSettle();
        })
        .catch((err) => {
          console.log("settleTheBalance Error", err);
        });
    },
    redirectToSettle() {
      this.$router.push({
        name: "SettleTheBalance",
        params: {
          group_id: this.localGroupID,
        },
      });
    },
    getGroupUsers() {
      // 取得付款人&分款人
      axios
        .get(`http://localhost:5000/group/${this.localGroupID}/users`)
        .then((res) => {
          this.users = res.data;
          console.log("getGroupUsers:", this.users);
        })
        .catch((err) => {
          console.log("getGroupUsers Error", err);
        });
    },
    redirectToUsers(users) {
      console.log("redirectToUsers Data:", users);
      this.$router.push({
        name: "UpdateUsers",
        // path: `/group/${res.data.id}/add_users`,
        params: {
          group_id: this.localGroupID,
          users: users,
        },
      });
    },
    deleteExpense(expenseID) {
      axios
        .delete(
          `http://localhost:5000/group/${this.localGroupID}/expenses/${expenseID}`
        )
        .then(() => {
          // 直接更新前端的 expenses 列表
          // filter 走訪 expense, 若列表的expense_id與請求的expense_id不相等則保留
          this.expenses = this.expenses.filter(
            (expense) => expense.id !== expenseID
          );
        })
        .catch((err) => {
          console.log("deleteExpense Error");
        });
    },
    redirectToExpense(
      expenseID,
      expenseItem,
      expenseAmount,
      expensePayerID,
      expensePayer
    ) {
      // console.log("payerID:", expensePayerID);
      this.$router.push({
        name: "UpdateExpense",
        params: {
          group_id: this.localGroupID,
          expense_id: expenseID,
          expenseItem: expenseItem,
          expenseAmount: expenseAmount,
          expensePayerID: expensePayerID,
          expensePayer: expensePayer,
        },
      });
    },
  },
};
</script>

<style scoped>
/* .wrapper {  border: 1px solid #000;} */

/* .container { */
/* padding-top: 30px; */
/* border: 1px solid #000; */
/* } */

h3 {
  margin-top: 40px;
  margin-bottom: 10px;
}

.list-container {
  width: 90%;
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

.list-rows {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.list-row1 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: 18px;
  font-weight: bold;
}

.button.delete-expense {
  display: flex;
  /* 內文水平置中 */
  justify-content: center;
  /* 內文垂直置中 */
  align-items: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-top: -20px;
  margin-left: -20px;
  opacity: 0.5;
  font-size: 10px;
  color: #696969;
  background-color: transparent;
  /* border: 1px solid #000; */
}

.list-row2 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: 14px;
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

.button.edit-users {
  position: relative;
  height: 30px;
  width: 30px;
  border-radius: 50%;
  margin-left: 20px;
  overflow: hidden;
  background-image: url("../assets/img/group-users.png");
  /* 確保圖片大小適合 add-user尺寸 */
  background-size: 70%;
  background-position: center;
  background-repeat: no-repeat;
  fill: #fff;
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
