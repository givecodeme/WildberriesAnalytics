<template>
  <div class="">
    <b-row>
      <b-col>
        <b-jumbotron bg-variant="warning" header="Заказали">
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
      <b-col>
        <b-jumbotron header="Доходы">
          {{ incomes | format }} р.
        </b-jumbotron>
      </b-col>
    </b-row>
    <!-- <h1>Products</h1> -->
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
    <b-container fluid  >

      <!-- <b-button @click="sortBy('orders_sum')">sort by orders</b-button>
      <b-button @click="sortBy('sales_sum')">sort by sales</b-button> -->
      <!-- <card
        v-for="(product, index) in products"
        :key="index"
        :product="product"
      /> -->
    <md-table
     v-model="products"
      md-sort="sales_sum"
       md-sort-order="desc"
        md-card 
      md-fixed-header
    >
      <md-table-toolbar>
        <h1 class="md-title">Products</h1>
        <p>
          
          <md-field
          >
            <label>Налоговая ставка</label>
            <md-input
            style="width:100px"
          v-model="tax"
          @input="updateTax"
          />
            <span class="md-suffix">%</span>

          </md-field>
        </p>
      </md-table-toolbar>

      <card
      :tax="tax"
      v-show="!loading"
      v-for="product in products"
      :key="product.id"
      :product="product"
      />


  <!-- <md-table-row slot="md-table-row" slot-scope="{ item }">

    <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{
      item.id
    }}</md-table-cell>

    <md-table-cell md-label="Name" md-sort-by="name">{{
      item.image
    }}</md-table-cell>
    <md-table-cell md-label="Orders" md-sort-by="orders_sum">{{
      item.orders_sum
    }}</md-table-cell>
    <md-table-cell md-label="Sales" md-sort-by="sales_sum">{{
      item.sales_sum
    }}</md-table-cell>
  </md-table-row> -->
<!-- :item="{item}" -->
      <!-- <md-table-row slot="md-table-row" slot-scope="{ item }" > -->
            <!-- <md-table md-card>

        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Name" md-sort-by="image">{{ item.image }}</md-table-cell> -->
      <!-- </md-table-row> -->
      <!-- </md-table> -->
    </md-table>
          <md-progress-spinner v-show="loading" md-mode="indeterminate"></md-progress-spinner>

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

        <template #cell(tax)="data">
          {{ data.value | format }} р.

          <!-- доставка - {{ data.item.delivery_sum | format }} р.
          <br />
          комиссия - {{ data.item.com_sum | format }} р. -->
        </template>

        <template #cell(sales_sum)="data">
          {{ data.value | format }} р.
          <p>{{ data.item.sales_qnt }} шт.</p>
        </template>

        <template #cell(sebes)="data">
          <div class="">
            <sebes :prod_id="data.item.id" :prop_sebes="data.value" />
          </div>
        </template>

        <template #cell(image)="data">
          <img :src="data.value" height="100" />
          <br />
          <a :href="data.item.wb_url" target="_blank"> {{ data.item.id }}</a>
        </template>

        <template #cell(income)="data">
          {{ data.value | format }}
          <span v-if="Number.isInteger(data.value)">р.</span>
        </template>

        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/services/api";
import Sebes from "../components/Sebes.vue";
import Dohod from "../components/Dohod.vue";
import Card from "../components/Card.vue";
// import Sebes from "@/components/Sebes.vue";
// import api from "@/services/api";
export default {
  components: { Card, Sebes, Dohod },
  filters: {
    format: (val) => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  data() {
    return {
      products: [],
      tax: localStorage.getItem("tax") || 6,
      loading: true,
      date: this.$route.query.date || null,
      isBusy: true,
      transProps: {
        // Transition name
        name: "flip-list",
      },
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
          key: "tax",
          label: "Расходы",
          sortable: true,
          formatter: (value, key, item) => item.delivery_sum + item.com_sum,
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
        {
          key: "income",
          label: "Доход",
          sortable: true,
          formatter: (value, key, item) => {
            if (item.sebes) {
              return (
                item.sales_sum -
                item.delivery_sum -
                item.com_sum -
                item.sebes * item.sales_qnt -
                item.sales_sum * 0.06
              ).toFixed(0);
            } else return "Input sebes";
          },
          sortByFormatted: true,

          // this.sales - this.tax - this.sales * 0.06 - this.sebes
          // `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
        },
      ],
    };
  },
  watch: {
    "$route.query.date"(date) {
      this.isBusy = !this.isBusy;
      this.loading = !this.loading;

      axios
        .get("products/", {
          params: {
            date: date,
          },

          headers: {
            Authorization: localStorage.getItem("token"),
          },
        })
        .then((result) => {
          this.products = result.data.sort((a, b) => b.sales_sum - a.sales_sum);
          this.isBusy = !this.isBusy;
          this.loading = !this.loading;
        });
    },

    // orderingByOrders(newVal) {
    //   if (newVal)
    //     this.products = this.products.sort(
    //       (a, b) => b.orders_sum - a.orders_sum
    //     );
    //   else
    //     this.products = this.products.sort(
    //       (a, b) => a.orders_sum - b.orders_sum
    //     );
    // },
    // orderingBySales(newVal) {
    //   if (newVal)
    //     this.products = this.products.sort((a, b) => b.sales_sum - a.sales_sum);
    //   else
    //     this.products = this.products.sort((a, b) => a.sales_sum - b.sales_sum);
    // },
  },

  methods: {
    updateTax() {
      localStorage.setItem("tax", this.tax);
    },
  },
  mounted() {
    api
      .get("products/", {
        params: {
          date: this.date,
          // ordering: "-sum_orders",
        },
      })
      .then((result) => {
        this.products = result.data.sort((a, b) => b.sales_sum - a.sales_sum);
        this.isBusy = !this.isBusy;
        this.loading = !this.loading;
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
    incomes() {
      return this.products.reduce((sum, item) => sum + +item.income, 0);
    },
  },
};
</script>

<style >
table#table-transition-example .flip-list-move {
  transition: transform 0.5s;
}
</style>