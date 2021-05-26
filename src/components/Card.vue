<template>
  <b-card
    :img-src="product.image"
    img-alt="Card image"
    img-left
    img-height="120"
    class="mb-3"
  >
    <b-card-text>
      <b-row>
        <b-col>
          Арт.
          <a :href="product.wb_url" target="_blank">
            {{ product.nmid }}
          </a>
          <br />
          Наличие:
          <div v-for="(stock, index) in product.stocks" :key="index">
            {{ stock.name }} - {{ stock.quantity }} шт.
          </div>
          <div v-if="!product.stocks.length">0 шт.</div>
        </b-col>
        <!-- <b-col>
        Возвраты:
        <div class="" v-for="(order, index) in product.orders" :key="index">
          <div v-if="order.is_cancel" class="">
            {{ order.quantity }} - {{ order.price }}
          </div>
        </div>
        <br />
</b-col> -->
        <b-col
          >Orders:
          <br />
          {{ product.orders_sum }} р.
          <br />
          {{ product.orders_qnt }} шт.
        </b-col>
        <b-col>
          Sales:
          <br />
          {{ product.sales_sum }} р.

          <br />
          {{ product.sales_qnt }} шт.
        </b-col>
        <b-col>
          Delivery:
          <br />
          {{ product.delivery_sum }} р.
        </b-col>
        <b-col>
          Commission:
          <br />
          {{ product.com_sum }} р.
        </b-col>
      </b-row>
    </b-card-text>
  </b-card>
</template>

<script>
// import axios from "axios";

export default {
  props: {
    product: Object,
  },
};
</script>
