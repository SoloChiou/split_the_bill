<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <router-link to="/my_groups" class="router-link"> 我的群組</router-link>
        <p class="router-link" :style="{ display: 'inline-block' }">|</p>
        <router-link to="/create_group" class="router-link"
          >建立群組</router-link
        >
      </div>
      <h1>建立群組</h1>
      <div class="line"></div>
    </div>
    <div class="container">
      <p class="left-align">群組名稱</p>
      <input class="input" v-model="groupName" placeholder="必填*" />
      <p class="left-align">備註</p>
      <textarea
        class="input"
        v-model="note"
        placeholder="備註"
        :style="{ height: '100px' }"
      >
      </textarea>
      <button type="button" class="button" @click="createGroup">
        下一步 : 新增成員
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateGroup",
  data() {
    return {
      id: "",
      groupName: "",
      note: "",
    };
  },
  methods: {
    createGroup() {
      axios
        .post("http://localhost:5000/group", {
          groupName: this.groupName,
          note: this.note,
        })
        .then((res) => {
          console.log("Group data submitted:", res.data);
          this.$router.push({
            name: "AddUsers",
            // path: `/group/${res.data.id}/add_users`,
            params: {
              group_id: res.data.id,
              groupName: this.groupName,
              groupNote: this.note,
            },
          });
        })
        .catch((err) => {
          console.log("Error submitting data", err);
        });
    },
  },
};
</script>

<style scoped>
.container {
  width: 50%;
  /* margin: 0 auto; */
  /* padding-top: 0; */
  /* border: 1px solid #000; */
}

.left-align {
  /* margin-top: 15px; */
  margin-bottom: 5px;
  text-align: left;
  width: 100%;
  /* border: 1px solid #000; */
}

.input {
  width: 100%;
  height: 25px;
  margin-bottom: 30px;
  /* border: 1px solid #000; */
}
</style>
