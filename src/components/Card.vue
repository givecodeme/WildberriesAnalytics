<template>
  <md-table-row>
    <md-table-cell md-label="Card" md-numeric>
      <img :src="product.image" style="height: 75px" />
      <br />
      <a :href="product.wb_url" target="_blank">{{ product.id }}</a>
    </md-table-cell>

    <md-table-cell md-label="Orders" md-numeric md-sort-by="orders_sum">
      {{ product.orders_sum | format }}
      <br />
      {{ product.orders_qnt }} шт.
    </md-table-cell>

    <md-table-cell md-label="Stocks" md-numeric md-sort-by="stocks_qnt">
      <span :id="'stocks-' + product.id"> {{ product.stocks_qnt }} шт. </span>
      <b-tooltip
        v-if="product.stocks_qnt"
        :target="'stocks-' + product.id"
        triggers="hover"
      >
        <p v-for="(stock, index) in product.stocks" :key="index">
          {{ stock.name }} - {{ stock.quantity }} шт.
        </p>
      </b-tooltip>
    </md-table-cell>
    <md-table-cell md-label="Tax" md-numeric>
      <span :id="'cost-' + product.id">
        {{ cost | format }}
      </span>
      <br />
      <b-tooltip v-if="cost" :target="`cost-${product.id}`" triggers="hover">
        delivery - {{ product.delivery_sum | format }}
        <br />
        commission - {{ product.com_sum | format }}
      </b-tooltip>
    </md-table-cell>
    <md-table-cell md-label="Sales" md-numeric md-sort-by="sales_sum">
      {{ product.sales_sum | format }}
      <br />
      {{ product.sales_qnt }} шт.
    </md-table-cell>
    <md-table-cell style="width: 75px" md-label="Sebes" md-numeric>
      <!-- width="100" -->
      <!-- md-sort-by="sebes" -->
      <md-field>
        <md-input
          style="width: 75px"
          v-model="product.sebes"
          type="number"
          @change="updateSebes()"
        />
        <span class="md-suffix">р.</span>
      </md-field>
    </md-table-cell>

    <md-table-cell md-label="Доход" md-numeric md-sort-by="income">
      {{ income | format }}
    </md-table-cell>

    <md-table-cell md-label="ROI" md-numeric md-sort-by="roi">
      <h6>
        <b-badge
          :variant="roi > 100 ? 'success' : roi > 50 ? 'warning' : 'danger'"
          pill
        >
          <!-- <b-badge v-else-if="roi>50" variant="warning" pill>
        <b-badge v-else variant="danger" pill> -->
          <!-- <b-badge :variant="roi > 100 ? 'success' : 'warning'" pill> -->
          <!-- :class="roi > 100 ? 'text-success' : 'text-warning'" -->
          {{ roi }} %
        </b-badge>
      </h6>
    </md-table-cell>
  </md-table-row>
</template>

<script>
import api from "@/services/api";
export default {
  props: ["product", "tax"],
  // data() {
  //   return {
  //     // sebes: +this.product.sebes || null,
  //   };
  // },
  filters: {
    format: (val) => `${val} р.`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  updated() {
    this.$set(this.product, "income", this.income);
    this.$set(this.product, "roi", this.roi);
  },
  methods: {
    updateSebes() {
      api
        .patch(`product_update/${this.product.id}/`, {
          sebes: Number(this.product.sebes),
        })
        .then(() =>
          this.$bvToast.toast(`Product №${this.product.id} update`, {
            title: "Success",
            variant: "success",
            autoHideDelay: 3000,
          })
        );
    },
  },
  mounted() {
    this.$set(this.product, "income", this.income);
    this.$set(this.product, "roi", this.roi);
  },
  computed: {
    roi() {
      return this.product.sebes && this.product.sales_qnt
        ? +(
            (this.product.income /
              (this.product.sebes * this.product.sales_qnt)) *
            100
          ).toFixed(0)
        : 0;
    },
    income() {
      return this.product.sebes
        ? +(
            this.product.sales_sum -
            (this.product.sales_sum * this.tax) / 100 -
            this.product.sebes * this.product.sales_qnt -
            this.product.delivery_sum -
            this.product.com_sum
          ).toFixed(0)
        : 0;
    },
    cost() {
      return this.product.delivery_sum + this.product.com_sum;
    },
  },
};
</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  /* display: none; <- Crashes Chrome on hover */
  -webkit-appearance: none;
  margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}
</style>