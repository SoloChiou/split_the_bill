import Vue from "vue";
import Router from "vue-router";
import CreateGroup from "@/views/CreateGroup";
import MyGroups from "@/views/MyGroups";
import AddExpense from "@/views/AddExpense";
import NewGroup from "@/views/NewGroup";
import SettleTheBalance from "@/views/SettleTheBalance";
import AddUsers from "@/views/AddUsers";
import Reconciliation from "@/views/Reconciliation";
import UpdateExpense from "@/views/UpdateExpense";
import UpdateUsers from "@/views/UpdateUsers";
import UpdateGroup from "@/views/UpdateGroup";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/create_group",
      name: "CreateGroup",
      component: CreateGroup,
    },
    {
      path: "/group/:group_id/add_users",
      name: "AddUsers",
      component: AddUsers,
    },
    {
      path: "/my_groups",
      name: "MyGroups",
      component: MyGroups,
    },
    {
      path: "/group/:group_id",
      name: "NewGroup",
      component: NewGroup,
    },
    {
      path: "/group/:group_id/add_expense",
      name: "AddExpense",
      component: AddExpense,
    },
    {
      path: "/group/:group_id/settle_the_balance",
      name: "SettleTheBalance",
      component: SettleTheBalance,
    },
    {
      path: "/group/:group_id/expenses/settle_the_balance/reconciliation",
      name: "Reconciliation",
      component: Reconciliation,
    },
    {
      path: "/group/:group_id/expenses/:expense_id",
      name: "UpdateExpense",
      component: UpdateExpense,
    },
    {
      path: "/group/:group_id/update_users",
      name: "UpdateUsers",
      component: UpdateUsers,
    },
    {
      path: "/group/:group_id/update_group",
      name: "UpdateGroup",
      component: UpdateGroup,
    },
  ],
});
