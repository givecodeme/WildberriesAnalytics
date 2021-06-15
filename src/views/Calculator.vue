<template>
  <!-- md-sort="sales_sum" -->
  <!-- md-sort-order="desc" -->
  <md-table md-fixed-header v-model="products_calc" md-card>
    <md-table-toolbar>
      <h1 class="md-title">Products</h1>
      <p>
        <md-field>
          <label>Налоговая ставка</label>
          <md-input
            style="width: 100px"
            v-model="calc_tax"
            type="number"
            @input="update_tax"
          />
          <span class="md-suffix">%</span>
        </md-field>
      </p>
    </md-table-toolbar>

    <md-table-row>
      <md-table-cell md-label="Name">
        <md-field>
          <md-input
            v-model="calc_product.name"
            placeholder="Name"
            style="width: 20px"
          />
        </md-field>
      </md-table-cell>

      <md-table-cell md-label="Sebes">
        <md-field>
          <md-input v-model="calc_product.sebes" style="width: 0px" />
          <span class="md-suffix">р.</span>
        </md-field>
      </md-table-cell>

      <md-table-cell md-label="Delivery">
        <md-field>
          <md-input v-model="calc_product.delivery" style="width: 0px" />
          <span class="md-suffix">р.</span>
        </md-field>
      </md-table-cell>

      <md-table-cell md-label="Commission">
        <md-field>
          <md-input v-model="calc_product.commission" style="width: 0px" />
          <span class="md-suffix">%</span>
        </md-field>
      </md-table-cell>

      <md-table-cell md-label="Percent Sales">
        <md-field>
          <md-input
            v-model="calc_product.percent_sale"
            type="number"
            max="100"
            style="width: 0px"
          />
          <span class="md-suffix">%</span>
        </md-field>
      </md-table-cell>

      <md-table-cell md-numeric md-label="Dot Zero">
        {{ dot_zero }}
      </md-table-cell>

      <md-table-cell md-label="Price">
        <md-field>
          <md-input
            v-model="calc_product.price"
            type="number"
            style="width: 0px"
          />
          <span class="md-suffix">р.</span>
        </md-field>
      </md-table-cell>

      <md-table-cell md-numeric md-label="Cost">
        <span>
          <span id="tooltip-cost">
            {{ cost | format }}
          </span>
          <b-tooltip target="tooltip-cost" triggers="hover">
            tax - {{ (calc_product.price * 0.06) | format }} р.
            <br />
            comm - {{ (calc_product.price * 0.12) | format }}
            <br />
          </b-tooltip>
        </span>
      </md-table-cell>

      <md-table-cell md-numeric md-label="Income">
        {{ income | format }}
        <md-button class="md-raised md-primary" @click="addToCart()">
          Add
        </md-button>
      </md-table-cell>
    </md-table-row>
    <card-calculator
      v-for="(product, index) in products_calc"
      :key="index"
      :product="product"
      :calc_tax="calc_tax"
    />
  </md-table>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import CardCalculator from "../components/CardCalculator.vue";

export default {
  components: { CardCalculator },
  data() {
    return {
      calc_product: {
        name: "Cup",
        sebes: 100,
        commission: 12,
        delivery: 40,
        percent_sale: 80,
        price: 900,
        // prods: this.calc_products.unshift(this.calc_product),
      },
      calc_tax: localStorage.getItem("calc_tax") || 6,
    };
  },

  filters: {
    format: (val) => `${val} р.`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  methods: {
    ...mapActions(["ADD_TO_CART"]),
    update_tax() {
      localStorage.setItem("calc_tax", this.calc_tax);
    },
    addToCart() {
      this.ADD_TO_CART(this.calc_product);
      this.calc_product = {
        name: "Cup",
        sebes: 100,
        commission: 12,
        delivery: 40,
        percent_sale: 80,
        price: 900,
      };
    },
  },
  computed: {
    ...mapGetters(["products_calc"]),
    // prods() {
    //   return [this.calc_product].push(this.products_calc);
    // },
    dot_zero() {
      return (
        ((((100 - +this.calc_product.percent_sale) *
          (+this.calc_product.delivery + 33)) /
          100 +
          +this.calc_product.delivery +
          +this.calc_product.sebes) /
          (100 - +this.calc_tax - +this.calc_product.commission)) *
        100
      ).toFixed(0);
    },
    cost() {
      return (
        (+this.calc_product.price *
          (+this.calc_tax + +this.calc_product.commission)) /
          100 +
        ((100 - +this.calc_product.percent_sale) *
          (+this.calc_product.delivery + 33)) /
          100 +
        +this.calc_product.delivery
      ).toFixed(2);
    },
    income() {
      return (
        +this.calc_product.price -
        +this.cost -
        +this.calc_product.sebes
      ).toFixed(2);
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