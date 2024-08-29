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
      <h1>我的群組</h1>
      <p>群組列表</p>
      <div class="line"></div>
    </div>
    <div class="container">
      <ul>
        <li class="list" v-for="group in allGroups" :key="group.id">
          <div class="list-rows" @click="redirectToGroup(group.id)">
            <button
              class="button delete-group"
              @click.stop="deleteGroup(group.id)"
            >
              x
            </button>
            {{ group.name }}
          </div>
        </li>
      </ul>
      <div class="list-container"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyGroups",
  props: ["group_id"],

  data() {
    return {
      allGroups: [],
    };
  },
  mounted() {
    this.getAllGroups();
  },
  methods: {
    getAllGroups() {
      axios
        .get("http://localhost:5000/my_groups")
        .then((res) => {
          this.allGroups = res.data;
          console.log("getAllGroups Data", this.allGroups);
        })
        .catch((err) => {
          console.log("getAllGroups Error", err);
        });
    },
    redirectToGroup(groupID) {
      this.$router.push(`/group/${groupID}`);
    },
    deleteGroup(groupID) {
      axios
        .delete(`http://localhost:5000/my_groups/${groupID}`)
        .then(() => {
          this.allGroups = this.allGroups.filter(
            (group) => group.id !== groupID
          );
        })
        .catch((err) => console.log("deleteGroup Error", err));
    },
  },
};
</script>

<style scoped>
/* .container { */
/* border: 1px solid #000; */
/* } */

ul {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  flex-wrap: wrap; /*若超出容器寬度就換行 */
  padding: 0;
  margin: 0;
  /* border: 1px solid #000; */
}

.list {
  display: flex;
  align-items: center; /*垂直置中 */
  justify-content: center; /*水平置中*/
  width: 40%;
  height: 80px;
  margin: 20px;
  font-weight: bold;
  background-color: #d9edfc;
  border-radius: 15px;
  /* border: 1px solid #000; */
}

.list-rows {
  position: relative;
  width: 100%;
  padding: 10px;
  cursor: pointer;
  /* border: 1px solid #000; */
}

.button.delete-group {
  position: absolute;
  top: -25px;
  left: 5px;
  display: flex;
  align-items: center; /*垂直置中 */
  justify-content: center; /*水平置中*/
  width: 20px;
  height: 20px;
  opacity: 0.5;
  font-size: 10px;
  color: #696969;
  background-color: transparent;
  /* border: 1px solid #000; */
}
</style>
