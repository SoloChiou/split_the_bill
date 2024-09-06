<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-function">
        <router-link to="/my_groups" class="router-link"> 我的群組</router-link>
      </div>
      <h1>編輯群組</h1>
      <div class="line"></div>
    </div>
    <div class="container">
      <p class="left-align">群組名稱</p>
      <input class="input" v-model="localGroupName" placeholder="必填*" />
      <p class="left-align">備註</p>
      <textarea
        class="input"
        v-model="localGroupNote"
        placeholder="備註"
        :style="{ height: '100px' }"
      >
      </textarea>
      <div class="button-container">
        <button type="button" class="button" @click="goBack">上一頁</button>
        <button type="button" class="button" @click="updateGroup">儲存</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UpdateGroup",
  props: ["group_id", "groupName", "groupNote"],

  data() {
    return {
      // data from NewGroup router-link
      localGroupID: this.$route.params.group_id,
      localGroupName: this.$route.params.groupName,
      localGroupNote: this.$route.params.groupNote,
    };
  },
  mounted() {
    console.log(
      "UpdateGroup Data",
      this.localGroupID,
      this.localGroupName,
      this.localGroupNote
    );
  },
  methods: {
    updateGroup() {
      const payload = {
        id: this.localGroupID,
        name: this.localGroupName,
        note: this.localGroupNote,
      };
      axios
        .put(
          `http://localhost:5000/group/${this.localGroupID}/update_group`,
          payload
        )
        .then((res) => {
          console.log("updateGroup Data", res.data);
          this.$router.push(`/group/${this.localGroupID}`);
        });
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
}
</style>
