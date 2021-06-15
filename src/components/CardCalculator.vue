<template>
  <md-table-row>
    <md-table-cell md-label="Name">
      <!-- md-numeric -->
      <md-field>
        <md-input
          v-model="product.name"
          placeholder="Name"
          style="width: 20px"
        />

        <!-- style="width: 75px" -->
      </md-field>
    </md-table-cell>

    <md-table-cell md-label="Sebes">
      <!-- md-numeric -->
      <md-field>
        <md-input v-model="product.sebes" style="width: 0px" />
        <span class="md-suffix">р.</span>

        <!-- style="width: 75px" -->
      </md-field>
    </md-table-cell>
    <md-table-cell md-label="Delivery">
      <!-- md-numeric -->
      <md-field>
        <md-input v-model="product.delivery" style="width: 0px" />
        <span class="md-suffix">р.</span>
      </md-field>
    </md-table-cell>
    <md-table-cell md-label="Commission">
      <md-field>
        <md-input v-model="product.commission" style="width: 0px" />
        <span class="md-suffix">%</span>
      </md-field>
    </md-table-cell>
    <md-table-cell md-label="Percent Sales">
      <md-field>
        <md-input
          v-model="product.percent_sale"
          type="number"
          max="100"
          style="width: 0px"
        />
        <span class="md-suffix">%</span>
      </md-field>
    </md-table-cell>

    <md-table-cell md-numeric md-label="Dot Zero">
      {{ dot_zero | format }}
    </md-table-cell>
    <md-table-cell md-label="Price">
      <md-field>
        <md-input v-model="product.price" type="number" style="width: 0px" />
        <span class="md-suffix">р.</span>
      </md-field>
    </md-table-cell>
    <md-table-cell md-numeric md-label="Cost">
      <span>
        <span id="tooltip-cost">
          {{ cost | format }}
        </span>
        <b-tooltip target="tooltip-cost" triggers="hover">
          tax - {{ (product.price * 0.06) | format }} р.
          <br />
          comm - {{ (product.price * 0.12) | format }}
          <br />
        </b-tooltip>
      </span>
    </md-table-cell>
    <md-table-cell md-numeric md-label="Income">
      {{ income | format }}
    </md-table-cell>
    <md-table-cell md-numeric md-label="ROI">
      <h6>
        <b-badge
          :variant="roi > 100 ? 'success' : roi > 50 ? 'warning' : 'danger'"
          pill
        >
          {{ roi }} %</b-badge
        >
      </h6>
    </md-table-cell>
  </md-table-row>
</template>

<script>
export default {
  props: ["product", "calc_tax"],
  data() {
    return {
      //   calc_tax: localStorage.getItem("calc_tax") || 6,
    };
  },

  filters: {
    format: (val) => `${val} р.`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  computed: {
    dot_zero() {
      return (
        ((((100 - +this.product.percent_sale) * (+this.product.delivery + 33)) /
          100 +
          +this.product.delivery +
          +this.product.sebes) /
          (100 - +this.calc_tax - +this.product.commission)) *
        100
      ).toFixed(0);
    },
    cost() {
      return +(
        (+this.product.price * (+this.calc_tax + +this.product.commission)) /
          100 +
        ((100 - +this.product.percent_sale) * (+this.product.delivery + 33)) /
          100 +
        +this.product.delivery
      ).toFixed(2);
    },
    income() {
      return (+this.product.price - +this.cost - +this.product.sebes).toFixed(
        2
      );
    },
    roi() {
      return ((this.income / this.product.sebes - 1) * 100).toFixed(0);
    },
  },
};
</script>

<style>
</style>