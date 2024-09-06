<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <div class="header-function">
          <router-link to="/my_groups" class="router-link">
            我的群組</router-link
          >
          <p class="router-link" :style="{ display: 'inline-block' }">|</p>
          <router-link to="/create_group" class="router-link"
            >建立群組</router-link
          >
        </div>
      </div>
      <h1>新增成員</h1>
      <div class="line"></div>
    </div>
    <div class="container">
      <div v-for="(user, index) in users" :key="index">
        <input class="input" v-model="user.name" placeholder="成員名稱" />
      </div>
      <br />
      <button type="button" class="button" @click="addUserColumn">
        新增成員
      </button>
      <div>
        <button type="button" class="button" @click="addUsers">儲存</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AddUsers",
  // props from CreateGroup
  // 上一層傳遞的參數屬性
  props: ["group_id", "groupName", "groupNote"],
  data() {
    return {
      // name輸入框動態存入users列表
      users: [{ name: "" }],
      // 從CreateGroup的createGroup()參數中獲取group_id
      localGroupID: this.$route.params.group_id,
      localGroupName: this.$route.params.groupName,
      localGroupNote: this.$route.params.groupNote,
    };
  },
  mounted() {
    console.log("AddUsers get localGroupID:", this.localGroupID);
    console.log("AddUsers get localGroupName:", this.localGroupName);
    console.log("AddUsers get localGroupNote:", this.localGroupNote);
  },
  methods: {
    // 生成空白欄位
    addUserColumn() {
      this.users.push({ name: "" });
    },
    addUsers() {
      console.log("Saving users:", this.users);
      this.users.forEach((user) => {
        axios
          .post(`http://localhost:5000/group/${this.localGroupID}/add_users`, {
            name: user.name,
            group_id: this.localGroupID,
          })
          .then((res) => {
            console.log("User added:", res.data);
          })
          .catch((err) => {
            console.log("Error adding user", err);
          });
      });
      this.$router.push({
        name: "NewGroup",
        // path: `/group/${this.localGroupID}`,
        params: {
          group_id: this.localGroupID,
          groupName: this.localGroupName,
          groupNote: this.localGroupNote,
        },
      });
    },
  },
};
</script>

<style scoped>
.wrapper {
  position: relative;
  /* border: 1px solid #000; */
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  /* padding-top: 50px; */
  /* border: 1px solid #000; */
}

.header {
  background-color: transparent;
}

.button {
  margin: 10px;
  padding: 5px 10px;
  font-size: 16px;
  background-color: #71acdc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.left-align {
  margin-top: 15px;
  margin-bottom: 5px;
  text-align: left;
}

.input {
  margin-top: 25px;
  width: 100%;
  height: 25px;
}
</style>
