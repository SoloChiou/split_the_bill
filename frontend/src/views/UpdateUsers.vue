<template>
  <div class="wrapper">
    <div class="header">
      <h1>編輯成員</h1>
      <p>有帳款成員不可刪除</p>
      <div class="line"></div>
    </div>
    <div class="container">
      <div v-for="(user, index) in localUsers" :key="index" class="input-rows">
        <button class="button delete-user" @click="deleteUser(user.id)">
          x
        </button>
        <input class="input" v-model="user.name" placeholder="成員名稱" />
      </div>
      <div>
        <button type="button" class="button" @click="addUserColumn">
          新增成員
        </button>
      </div>
      <div class="button-container">
        <button type="button" class="button" @click="goBack">上一頁</button>
        <button type="button" class="button" @click="updateUsers">
          儲存更新
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateUsers",
  // props from NewGroup
  // 上一層傳遞的參數屬性
  props: ["users"],
  data() {
    return {
      localGroupID: this.$route.params.group_id,
      localUsers: this.$route.params.users || "[]",
    };
  },
  mounted() {
    console.log("Local Users:", this.localUsers);
  },
  methods: {
    // 生成空白欄位, name為v-mode指定的屬性
    addUserColumn() {
      this.localUsers.push({ name: "" });
    },
    deleteUser(userID) {
      axios
        .delete(`http://localhost:5000/group/${this.localGroupID}/${userID}`)
        .then(() => {
          this.localUsers = this.localUsers.filter(
            (user) => user.id !== userID
          );
        })
        .catch((err) => {
          console.log("deleteUser Error", err);
        });
    },
    updateUsers() {
      const payload = { users: this.localUsers };
      console.log("Payload: ", payload);
      axios
        .put(
          `http://localhost:5000/group/${this.localGroupID}/update_users`,
          payload
        )
        .then((res) => {
          console.log("Payload:", payload);
          this.$router.push(`/group/${this.localGroupID}`);
        })
        .catch((err) => {
          console.log("updateUsers Error", err);
        });
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
/* .container { */
/* border: 1px solid #000; */
/* } */

.header {
  background-color: transparent;
}

.button {
  margin-top: 30px;
}

.button.delete-user {
  display: flex;
  /* 內文水平置中 */
  justify-content: center;
  /* 內文垂直置中 */
  align-items: center;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  opacity: 0.5;
  font-size: 10px;
  color: #696969;
  background-color: transparent;
  /* border: 1px solid #000; */
}

/* .button-container { */
/* margin-left: -173px; */
/* border: 1px solid #000; */
/* } */

.input-rows {
  display: flex;
  align-items: center;

  /* 補正 delete-user的margin-right: 10px; */
  margin-right: 10px;
  /* border: 1px solid #000; */
}

.input {
  margin-top: 25px;
  width: 100%;
  height: 25px;
}
</style>
