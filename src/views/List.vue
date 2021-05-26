<template>
  <div class="">
    <b-row>
      <b-col>
        <b-jumbotron header="Заказали">
          <p>На сумму: {{ orders | format }} р.</p>
          Кол-во: {{ orders_qnt }} шт.
        </b-jumbotron>
      </b-col>

      <b-col>
        <b-jumbotron header="Выкупили">
          <p>На сумму: {{ sales | format }} р.</p>
          Кол-во: {{ sales_qnt }} шт.
        </b-jumbotron>
      </b-col>
      <b-col>
        <b-jumbotron header="Расходы">
          {{ fees | format }} р.

          <p>Доставка на сумму: {{ deliveries | format }} р.</p>
          commissions: {{ commissions | format }} р.
        </b-jumbotron>
      </b-col>
    </b-row>
    <h1>Products</h1>
    <b-button
      variant="outline-success"
      @click="$router.push({ query: { date: 'today' } })"
      >ToDay</b-button
    >
    <b-button
      variant="outline-success"
      @click="$router.push({ query: { date: 'yesterday' } })"
      >yesterday</b-button
    >
    <b-button
      variant="outline-success"
      @click="$router.push({ query: { date: 'week' } })"
      >week</b-button
    >
    <b-button
      variant="outline-success"
      @click="$router.push({ query: { date: 'month' } })"
      >month</b-button
    >
    <b-button
      variant="outline-success"
      @click="$router.push({ query: { date: 'year' } })"
      >year</b-button
    >
    <b-container>
      <!-- <b-button @click="sortBy('orders_sum')">sort by orders</b-button>
      <b-button @click="sortBy('sales_sum')">sort by sales</b-button> -->
      <!-- <card
        v-for="(product, index) in products"
        :key="index"
        :product="product"
      /> -->

      <b-table
        id="table-transition-example"
        :fields="fields"
        :items="products"
        class="mt-3"
        primary-key="nmid"
      >
        <!-- <br />
          <span v-for="(stock, index) in data.item.stocks" :key="index">
            {{ stock.name }} - {{ stock.quantity }} шт.
            <br />
          </span> -->

        <template #cell(stocks_qnt)="data"> {{ data.value }} шт. </template>

        <template #cell(orders_sum)="data">
          {{ data.value | format }} р.
          <p>{{ data.item.orders_qnt }} шт.</p>
        </template>

        <template #cell(delivery_sum)="data">
          доставка - {{ data.value | format }} р.
          <br />
          комиссия - {{ data.item.com_sum | format }} р.
        </template>

        <template #cell(sales_sum)="data">
          {{ data.value | format }} р.
          <p>{{ data.item.sales_qnt }} шт.</p>
        </template>

        <template #cell(sebes)="data">
          <div class="">
            <sebes :prod_id="data.item.id" />
          </div>
        </template>

        <template #cell(image)="data">
          <img :src="data.value" height="100" />
          <br />
          <a :href="data.item.wb_url" target="_blank"> {{ data.item.nmid }}</a>
        </template>
      </b-table>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import Card from "@/components/Card.vue";
import Sebes from "../components/Sebes.vue";
// import Sebes from "@/components/Sebes.vue";
// import api from "@/services/api";
export default {
  components: { Card, Sebes },
  filters: {
    format: (val) => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  data() {
    return {
      products: [],
      date: this.$route.query.date || "",
      fields: [
        {
          key: "image",
          label: "Карточка",
        },
        // {
        //   key: "subject",
        //   label: "Категория",
        // },
        // {
        //   key: "nmid",
        //   label: "Person",
        //   // variant: "danger",
        // },
        {
          key: "stocks_qnt",
          label: "Наличие",
          sortable: true,
        },
        // {
        //   key: "per_sale",
        //   label: "Выкуп, %",
        //   sortable: true,
        // },
        {
          key: "orders_sum",
          label: "Заказано",
          sortable: true,
        },
        {
          key: "delivery_sum",
          label: "Расходы",
          sortable: true,
        },
        {
          key: "sales_sum",
          label: "Выкуплено",
          sortable: true,
        },
        {
          key: "sebes",
          // label: "Выкуплено",
          sortable: true,
        },
      ],
    };
  },
  watch: {
    "$route.query.date"(date) {
      axios
        .get("products/", {
          params: {
            date: date,
            ordering: "-sum_orders",
          },
        })
        .then((result) => {
          this.products = result.data;
        });
    },

    orderingByOrders(newVal) {
      if (newVal)
        this.products = this.products.sort(
          (a, b) => b.orders_sum - a.orders_sum
        );
      else
        this.products = this.products.sort(
          (a, b) => a.orders_sum - b.orders_sum
        );
    },
    orderingBySales(newVal) {
      if (newVal)
        this.products = this.products.sort((a, b) => b.sales_sum - a.sales_sum);
      else
        this.products = this.products.sort((a, b) => a.sales_sum - b.sales_sum);
    },
  },

  methods: {
    sortByOrders() {
      this.products = this.products.sort((a, b) => b.orders_sum - a.orders_sum);
    },

    Ordering() {
      // var column =
    },
    sortBy(val) {
      this.products = this.products.sort((a, b) => (a[val] > b[val] ? -1 : 1));
    },
    changeSebes(id) {
      axios.post(`products/${id}`, {
        Sebes: 123,
      });
    },
  },

  mounted() {
    axios
      .get("products/", {
        params: {
          date: this.date,
          ordering: "-sum_orders",
        },
      })
      .then((result) => {
        this.products = result.data;
      });
  },
  computed: {
    orders() {
      return this.products.reduce((sum, item) => sum + item.orders_sum, 0);
    },
    orders_qnt() {
      return this.products.reduce((sum, item) => sum + item.orders_qnt, 0);
    },
    sales() {
      return this.products.reduce((sum, item) => sum + item.sales_sum, 0);
    },
    sales_qnt() {
      return this.products.reduce((sum, item) => sum + item.sales_qnt, 0);
    },
    deliveries() {
      return this.products.reduce((sum, item) => sum + item.delivery_sum, 0);
    },
    commissions() {
      return this.products.reduce((sum, item) => sum + item.com_sum, 0);
    },
    fees() {
      return this.commissions + this.deliveries;
    },
  },
};
</script>

<style>
table#table-transition-example .flip-list-move {
  transition: transform 1s;
}
</style>